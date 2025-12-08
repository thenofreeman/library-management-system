from typing import Optional

from ui.screens import SearchScreen
from ui.modals import BorrowerDetailModal

from models import BorrowerSearchResult

import database as db

class BorrowerSearchScreen(SearchScreen):

    def __init__(self):
        def borrower_search(query: str, filters: Optional[dict]) -> list[BorrowerSearchResult]:
            return db.search_borrowers(query)

        super().__init__(
            title="Borrower Search",
            columns=[
                ("Card ID", 12),
                ("Name", 50),
                ("Checkouts", 8),
                ("Fines", 8),
            ],
            search_fn=borrower_search,
            detail_modal=BorrowerDetailModal,
            placeholder="Search Name or ID...",
            filters={
                'columns': [('Card ID', True), ('Name', True)],
            }
        )

    def get_detail_data(self, row_data: tuple) -> dict:
        card_id, name, n_checkouts, total_fines = row_data

        return {
            "card_id": card_id,
            "name": name,
            "n_checkouts": n_checkouts,
            "total_fines": total_fines,
        }
