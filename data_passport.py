import hashlib
from datetime import datetime, timezone

from pydantic import BaseModel, Field


class DataPassport(BaseModel):
    chunk_id: str
    content: str
    source_document: str
    clearance_level: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    cryptographic_hash: str = ""


def generate_signature(content: str, source: str, clearance_level: str) -> str:
    payload = f"{content}|{source}|{clearance_level}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def process_and_sign_data(chunk_id: str, content: str, source_document: str, clearance_level: str) -> DataPassport:
    passport = DataPassport(
        chunk_id=chunk_id,
        content=content,
        source_document=source_document,
        clearance_level=clearance_level,
    )
    passport.cryptographic_hash = generate_signature(
        passport.content, passport.source_document, passport.clearance_level
    )
    return passport


if __name__ == "__main__":
    fake_documents = [
        ("Project Falcon will launch in Q2 2027 with a $50M budget.", "board_minutes_2026.txt"),
        ("The Merger with Acme Corp is under review by Legal and Finance.", "deal_memo_internal.pdf"),
        ("Employee Sarah Chen is being promoted to Senior Engineer effective January.", "hr_update_emails.eml"),
    ]

    for i, (content, source) in enumerate(fake_documents, start=1):
        passport = DataPassport(
            chunk_id=f"chunk_{i:03d}",
            content=content,
            source_document=source,
            clearance_level="EXECUTIVE_ONLY",
        )
        passport.cryptographic_hash = generate_signature(
            passport.content, passport.source_document, passport.clearance_level
        )
        print(f"chunk_id:            {passport.chunk_id}")
        print(f"content:             {passport.content}")
        print(f"source_document:     {passport.source_document}")
        print(f"clearance_level:     {passport.clearance_level}")
        print(f"timestamp:           {passport.timestamp}")
        print(f"cryptographic_hash:  {passport.cryptographic_hash}")
        print("-" * 60)
