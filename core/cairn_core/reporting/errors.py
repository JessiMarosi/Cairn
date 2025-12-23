from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReportError(Exception):
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"
