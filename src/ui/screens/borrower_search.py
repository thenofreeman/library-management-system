from typing import Optional

from ui.screens import SearchScreen
from ui.modals import BorrowerDetailModal

from database.dtypes import Borrower

import database as db

class BorrowerSearchScreen(SearchScreen):

    def __init__(self):
        def borrower_search(query: str, filters: Optional[dict]) -> Optional[list[Borrower]]:
            return db.search_borrowers(query)

        super().__init__(
            title="Borrower Search",
            columns=[
                ("Card ID", 12),
                ("Name", 50),
                ("Checkouts", 8),
            ],
            search_fn=borrower_search,
            detail_modal=BorrowerDetailModal,
            placeholder="Search Name or ID...",
            filters={
                'columns': [('Card ID', True), ('Name', True)],
            }
        )
