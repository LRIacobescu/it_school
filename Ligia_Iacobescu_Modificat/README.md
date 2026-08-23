# PDF Data Explorer

Aplicatie web FastAPI pentru upload, filtrare si export de date din PDF.

## Ce foloseste proiectul

- FastAPI pentru backend;
- PostgreSQL pentru db;
- SQLAlchemy pentru lucrul cu db ul;
- PyMuPDF pentru citirea PDF urilor;
- Jinja2 pentru paginile HTML;
- ReportLab pentru exportul rezultatelor filtrate in PDF.

## 1. Creeaza mediul virtual

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

## 2. Instaleaza librariile

```bash
python -m pip install -r requirements.txt
```

## 3. Configureaza PostgreSQL

Copiaza `.env.example` intr un fisier nou numit `.env`.

Exemplu:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pdf_data_explorer
DB_USER=postgres
DB_PASS=parola_ta
MAX_UPLOAD_SIZE_MB=50
```

Daca user ul tau PostgreSQL nu are drept sa creeze db uri, creeaza manual db ul `pdf_data_explorer` din pgAdmin si sari peste partea de creare automata.

## 4. Creeaza db ul si tabelele

```bash
python -m database.setup_db
```

Comanda verifica daca db ul exista. Daca nu exista il creeaza, apoi creeaza tabelele proiectului.

## 5. Porneste aplicatia

```bash
python -m uvicorn app.main:app --reload
```

Deschide:

```text
http://127.0.0.1:8000
```

## Cum sunt salvate datele

Fiecare PDF incarcat este salvat in `uploaded_documents`.

Randurile extrase sunt salvate in `document_rows`. Coloanele unui PDF pot fi diferite fata de alt PDF, asa ca valorile randului sunt pastrate ca JSON in PostgreSQL.

Modelul vechi `pdf_data` a ramas in proiect pentru compatibilitate cu scripturile initiale.

## Export PDF

Dupa ce aplici filtrele, butonul `Export PDF` exporta toate randurile care corespund filtrelor active, nu doar pagina curenta din tabel.
