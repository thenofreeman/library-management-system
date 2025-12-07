from typing import Optional

from . import query

def get_metadata_value(key: str) -> Optional[str]:
    sql = """
        SELECT value FROM metadata
        WHERE key = ?
    """

    result = query.get_one_or_none(sql, [key])

    if not result:
        return None

    return str(result)

def set_metadata_value(key: str, value: str) -> bool:
    sql = """
    INSERT OR REPLACE INTO metadata (
        key,
        value
    ) VALUES (
        ?,
        ?
    )
    """

    params = [key, value]

    return query.try_execute_one(sql, params)
