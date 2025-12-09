from typing import Optional
from datetime import date

import database as db

def get_current_date() -> Optional[date]:
    d = db.get_value('current_date')

    if not d:
        return None

    return date.fromisoformat(d)

def set_current_date(value: date) -> bool:
    return db.set_value('current_date', value.isoformat())

def reset_time() -> bool:
    today = date.today()

    set_current_date(today)
    db.set_fines_updated(today)
    db.update_fines()

    return True
