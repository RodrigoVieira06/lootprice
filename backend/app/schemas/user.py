from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel


class UserRead(SQLModel):
    id: UUID
    email: str
    display_name: str | None = None
    avatar_url: str | None = None
    role: str
    is_active: bool
    last_login_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
