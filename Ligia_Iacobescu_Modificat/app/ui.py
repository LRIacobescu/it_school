import io
import os
import re
import uuid
from fastapi import APIRouter, Body, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from extractor.table_extractor import PDFTableExtractor
from database.repository import DatabaseRepository
from services.data_service import apply_filters, infer_column_metadata
from services.pdf_export_service import build_filtered_pdf
from config.settings import settings

router = APIRouter()
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


def get_recent_documents():
    repo = DatabaseRepository()
    try:
        return repo.list_documents(limit=8)
    finally:
        repo.close()


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="upload.html",
        context={"documents": get_recent_documents(), "error": None},
    )


@router.post("/upload", response_class=HTMLResponse)
async def upload_pdf(request: Request, file: UploadFile):
    filename = file.filename or "document.pdf"
    extension = os.path.splitext(filename)[1].lower()

    if extension != ".pdf":
        return templates.TemplateResponse(
            request=request,
            name="upload.html",
            context={
                "documents": get_recent_documents(),
                "error": "Fisierul trebuie sa fie PDF.",
            },
            status_code=400,
        )

    stored_filename = str(uuid.uuid4()) + ".pdf"
    destination = os.path.join(settings.UPLOAD_DIR, stored_filename)
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    total_bytes = 0

    try:
        with open(destination, "wb") as output:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                total_bytes += len(chunk)
                if total_bytes > max_bytes:
                    raise ValueError(
                        "PDF ul depaseste limita de " + str(settings.MAX_UPLOAD_SIZE_MB) + " MB."
                    )
                output.write(chunk)

        extractor = PDFTableExtractor(destination)
        extracted = extractor.extract()
        rows = extracted["rows"]
        metadata = infer_column_metadata(rows, extracted["columns"])

        repo = DatabaseRepository()
        try:
            document_id = repo.save_document(
                original_filename=filename,
                stored_filename=stored_filename,
                rows=rows,
                column_metadata=metadata,
                extraction_mode=extracted["mode"],
            )
        finally:
            repo.close()

        return RedirectResponse(url="/documents/" + str(document_id), status_code=303)

    except Exception as exc:
        if os.path.exists(destination):
            os.remove(destination)

        return templates.TemplateResponse(
            request=request,
            name="upload.html",
            context={
                "documents": get_recent_documents(),
                "error": str(exc),
            },
            status_code=400,
        )
    finally:
        await file.close()


@router.get("/documents/{document_id}", response_class=HTMLResponse)
def document_page(request: Request, document_id: int):
    repo = DatabaseRepository()
    try:
        document = repo.get_document(document_id)
        if not document:
            return HTMLResponse("<h1>Document not found</h1>", status_code=404)

        return templates.TemplateResponse(
            request=request,
            name="document.html",
            context={"document": document, "metadata": document.column_metadata},
        )
    finally:
        repo.close()


@router.post("/api/documents/{document_id}/filter")
def filter_document(document_id: int, payload: dict = Body(default={})):
    repo = DatabaseRepository()
    try:
        document = repo.get_document(document_id)
        if not document:
            return JSONResponse({"detail": "Document not found"}, status_code=404)

        rows = repo.get_document_rows(document_id)
        filtered = apply_filters(
            rows,
            payload.get("filters") or {},
            document.column_metadata,
            payload.get("search") or "",
        )

        sort_by = payload.get("sort_by")
        sort_dir = payload.get("sort_dir", "asc")

        def safe_value(v):
            if v is None:
                return float("-inf")  # pune valorile lipsă la început
            try:
                return float(v)  # dacă e numeric → sortare numerică
            except:
                return str(v).lower()  # dacă nu e numeric → sortare text

        if sort_by:
            reverse = sort_dir == "desc"
            filtered.sort(key=lambda r: safe_value(r.get(sort_by)), reverse=reverse)

        try:
            page = max(1, int(payload.get("page", 1)))
        except (TypeError, ValueError):
            page = 1

        try:
            page_size = int(payload.get("page_size", 50))
        except (TypeError, ValueError):
            page_size = 50
        page_size = max(10, min(page_size, 200))

        total = len(filtered)
        total_pages = max(1, (total + page_size - 1) // page_size)
        if page > total_pages:
            page = total_pages

        start = (page - 1) * page_size
        end = start + page_size

        return {
            "rows": filtered[start:end],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }
    finally:
        repo.close()

@router.post("/api/documents/{document_id}/export/pdf")
def export_filtered_pdf(document_id: int, payload: dict = Body(default={})):
    """Exporta toate randurile care corespund filtrelor active, nu doar pagina vizibila."""
    repo = DatabaseRepository()
    try:
        document = repo.get_document(document_id)
        if not document:
            return JSONResponse({"detail": "Document not found"}, status_code=404)

        rows = repo.get_document_rows(document_id)
        filters = payload.get("filters") or {}
        search_text = payload.get("search") or ""
        filtered = apply_filters(rows, filters, document.column_metadata, search_text)

        pdf_bytes = build_filtered_pdf(
            document_name=document.original_filename,
            rows=filtered,
            metadata=document.column_metadata,
            filters=filters,
            search_text=search_text,
        )

        base_name = os.path.splitext(document.original_filename)[0]
        safe_name = re.sub(r"[^a-zA-Z0-9._-]+", "_", base_name).strip("._") or "document"
        export_name = safe_name + "_filtered.pdf"

        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": 'attachment; filename="' + export_name + '"',
                "X-Result-Count": str(len(filtered)),
            },
        )
    finally:
        repo.close()

