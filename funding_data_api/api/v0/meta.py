"""Meta endpoints for assets, sections, and quotes."""

from fastapi import APIRouter

from funding_data_api.dto.base import BaseResponse
from funding_data_api.dto.meta import AssetNames, QuoteNames, SectionNames
from funding_data_api.queries.meta import GetAssetsDep, GetQuotesDep, GetSectionsDep

router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("/assets")
async def get_assets(assets: GetAssetsDep) -> BaseResponse[AssetNames]:
    """Get all asset names that exist in contracts.

    Returns assets sorted by market_cap_rank (ascending), then alphabetically
    for assets without market_cap_rank.
    """
    return BaseResponse(data=AssetNames(names=assets))


@router.get("/sections")
async def get_sections(sections: GetSectionsDep) -> BaseResponse[SectionNames]:
    """Get all section names ordered alphabetically."""
    return BaseResponse(data=SectionNames(names=sections))


@router.get("/quotes")
async def get_quotes(quotes: GetQuotesDep) -> BaseResponse[QuoteNames]:
    """Get all quote names ordered alphabetically."""
    return BaseResponse(data=QuoteNames(names=quotes))
