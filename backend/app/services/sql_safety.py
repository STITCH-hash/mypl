import re


FORBIDDEN_KEYWORDS = {
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create",
    "replace",
    "merge",
}


def is_safe_select(sql: str) -> bool:
    """MVP safety check: allow a single SELECT statement only."""
    normalized = sql.strip().lower()
    if not normalized.startswith("select"):
        return False
    if ";" in normalized.rstrip(";"):
        return False
    tokens = set(re.findall(r"[a-z_]+", normalized))
    return not tokens.intersection(FORBIDDEN_KEYWORDS)
