"""DTOs for meta endpoints."""

from pydantic import BaseModel


class AssetNames(BaseModel):
    names: list[str]


class SectionNames(BaseModel):
    names: list[str]


class QuoteNames(BaseModel):
    names: list[str]
