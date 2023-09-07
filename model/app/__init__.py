from pydantic import BaseModel


class EmailAddress(BaseModel):
    name: str
    address: str


class EmailMessage(BaseModel):
    from_address: EmailAddress
    to_addresses: list[EmailAddress]
    subject: str
    body: str
