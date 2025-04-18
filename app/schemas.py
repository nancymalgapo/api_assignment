from typing import Any

from pydantic import BaseModel


class Output(BaseModel):
    message: str | None = None
    results: Any | None = None
