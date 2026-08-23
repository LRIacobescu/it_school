import math
import re


TEXT_HINTS = ["id", "zip", "postal", "code", "class", "phone", "year"]
CURRENCY_HINTS = ["land", "impts", "total", "amount", "price", "value", "cost", "tax", "balance"]


def parse_number(value):
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        if isinstance(value, float) and math.isnan(value):
            return None
        return float(value)

    text = str(value).strip()
    if not text:
        return None

    negative = text.startswith("(") and text.endswith(")")
    text = text.strip("()")
    text = text.replace(",", "")
    text = text.replace("$", "").replace("€", "").replace("£", "")
    text = text.replace("%", "").strip()

    if not re.fullmatch(r"[-+]?\d+(?:\.\d+)?", text):
        return None

    number = float(text)
    return -number if negative else number


def infer_column_metadata(rows, column_order=None):
    if not rows:
        return []

    columns = list(column_order or [])
    for row in rows:
        for key in row.keys():
            if key not in columns:
                columns.append(key)

    metadata = []

    for column in columns:
        values = []
        for row in rows:
            value = row.get(column)
            if value not in (None, ""):
                values.append(value)

        lower_name = column.lower()
        force_text = any(hint in lower_name for hint in TEXT_HINTS)
        numeric_values = [parse_number(value) for value in values]
        parseable = [value for value in numeric_values if value is not None]
        numeric_ratio = len(parseable) / len(values) if values else 0

        has_currency_symbol = any(
            isinstance(value, str) and any(symbol in value for symbol in ["$", "€", "£"])
            for value in values[:200]
        )
        is_currency_name = any(hint in lower_name for hint in CURRENCY_HINTS)

        if values and not force_text and numeric_ratio >= 0.9:
            column_type = "currency" if has_currency_symbol or is_currency_name else "number"
            metadata.append({
                "name": column,
                "type": column_type,
                "min": min(parseable),
                "max": max(parseable),
                "values": [],
            })
        else:
            unique = sorted(
                {str(value) for value in values if str(value).strip()},
                key=lambda value: value.casefold(),
            )
            metadata.append({
                "name": column,
                "type": "text",
                "min": None,
                "max": None,
                "values": unique,
            })

    return metadata


def apply_filters(rows, filters, metadata, search_text=""):
    metadata_map = {item["name"]: item for item in metadata}
    result = []
    search_text = (search_text or "").strip().casefold()

    for row in rows:
        if search_text:
            haystack = " ".join(str(value) for value in row.values() if value is not None).casefold()
            if search_text not in haystack:
                continue

        keep = True
        for column, spec in (filters or {}).items():
            if column not in metadata_map:
                continue

            column_type = metadata_map[column]["type"]
            value = row.get(column)

            if column_type == "text":
                selected = spec.get("values") or []
                if selected and str(value or "") not in selected:
                    keep = False
                    break
            else:
                minimum = spec.get("min")
                maximum = spec.get("max")
                if minimum in (None, "") and maximum in (None, ""):
                    continue

                numeric_value = parse_number(value)
                if numeric_value is None:
                    keep = False
                    break

                if minimum not in (None, "") and numeric_value < float(minimum):
                    keep = False
                    break
                if maximum not in (None, "") and numeric_value > float(maximum):
                    keep = False
                    break

        if keep:
            result.append(row)

    return result
