from typing import Optional
from datetime import date

from pydantic import BaseModel, Field, field_serializer, model_validator

class BookSearchResult(BaseModel):
    isbn: str = Field(alias='Isbn')
    title: str = Field(alias='Title')
    authors: list[str] = Field(alias='Authors')
    status: bool = Field(alias='Status')
    borrower_id: Optional[int] = Field(default=None, alias='Card_id')

    @model_validator(mode='before')
    @classmethod
    def process_authors(cls, data):
        author_names = data.get('Author_names', '')

        if isinstance(author_names, str):
            names = [n.strip() for n in author_names.split(',') if n.strip()]

            data['Authors'] = names

            data.pop('Author_names', None)

        return data

    @property
    def status_display(self) -> str:
        return self.serialize_status(self.status)

    @property
    def id(self) -> str:
        return self.isbn

    @field_serializer('status')
    def serialize_status(self, status: bool) -> str:
        return "Available" if status else "Unavailable"

    @field_serializer('authors')
    def serialize_authors(self, authors: list[str]) -> str:
        return " & ".join(authors)

class BorrowerSearchResult(BaseModel):
    model_config = { 'frozen': True }
    id: int = Field(alias='Card_id')
    name: str = Field(alias='Bname')
    active_loan_count: int = Field(alias='N_Active_loans')
    total_unpaid_fines: int = Field(alias='Outstanding_fines') # in cents

    @field_serializer('total_unpaid_fines')
    def serialize_fines(self, amt: int) -> str:
        return f"${amt / 100:,.2f}"

    @property
    def amt_dollars(self) -> str:
        return self.serialize_fines(self.total_unpaid_fines)

class FineSearchResult(BaseModel):
    loan_id: int = Field(alias='Loan_id')
    isbn: str = Field(alias='Isbn')
    borrower_id: int = Field(alias='Card_id')
    amt: int = Field(alias='Fine_amt') # in cents
    paid: bool = Field(alias='Paid')
    date_out: date = Field(alias='Date_out')
    due_date: date = Field(alias='Due_date')
    date_in: Optional[date] = Field(alias='Date_in')
