from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()
emails: list[str] = []


class Email(BaseModel):
    email: EmailStr


@app.post("/waitlist")
def join(payload: Email) -> dict[str, bool]:
    emails.append(payload.email)
    return {"ok": True}
