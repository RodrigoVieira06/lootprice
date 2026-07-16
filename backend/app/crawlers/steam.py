import logging
from collections.abc import AsyncGenerator, Iterable
from decimal import Decimal
from typing import Any

import httpx

from app.crawlers.base import BaseCrawler, RawGameData

logger = logging.getLogger(__name__)


class SteamCrawler(BaseCrawler):
    """Coleta preços da busca pública da Steam para o catálogo brasileiro."""

    store_slug = "steam"
    default_endpoint = "https://store.steampowered.com/api/storesearch/"

    def __init__(
        self,
        search_terms: Iterable[str],
        client: httpx.AsyncClient | None = None,
        *,
        country_code: str = "br",
        language: str = "portuguese",
        endpoint: str = default_endpoint,
    ) -> None:
        self.search_terms = tuple(search_terms)
        self._client = client
        self.country_code = country_code
        self.language = language
        self.endpoint = endpoint

    async def fetch(self) -> AsyncGenerator[RawGameData, None]:
        owns_client = self._client is None
        client = self._client or httpx.AsyncClient(timeout=15.0)

        try:
            for term in self.search_terms:
                try:
                    response = await client.get(
                        self.endpoint,
                        params={
                            "term": term,
                            "cc": self.country_code,
                            "l": self.language,
                        },
                    )
                    response.raise_for_status()
                    payload = response.json()
                except (httpx.HTTPError, ValueError) as exc:
                    logger.exception("Falha ao consultar Steam para %r: %s", term, exc)
                    continue

                for item in self._items_from_payload(payload):
                    raw_data = self._parse_item(item)
                    if raw_data is not None:
                        yield raw_data
        finally:
            if owns_client:
                await client.aclose()

    @staticmethod
    def _items_from_payload(payload: Any) -> list[dict[str, Any]]:
        if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
            logger.warning("Resposta da Steam sem lista de itens")
            return []

        return [item for item in payload["items"] if isinstance(item, dict)]

    def _parse_item(self, item: dict[str, Any]) -> RawGameData | None:
        app_id = item.get("id")
        title = item.get("name")
        price = item.get("price_overview")

        if not app_id or not isinstance(title, str) or not title.strip():
            logger.warning("Item Steam ignorado por ausência de id ou nome: %r", item)
            return None
        if not isinstance(price, dict) or not isinstance(price.get("final"), int):
            logger.info("Produto Steam sem preço disponível: %s", app_id)
            return None

        try:
            price_brl = self._cents_to_brl(price["final"])
            original_price = price.get("initial")
            original_price_brl = (
                self._cents_to_brl(original_price)
                if isinstance(original_price, int)
                else None
            )
            return RawGameData(
                title=title.strip(),
                external_id=str(app_id),
                store_url=f"https://store.steampowered.com/app/{app_id}/",
                price_brl=price_brl,
                original_price_brl=original_price_brl,
                is_available=True,
                store_slug=self.store_slug,
            )
        except (TypeError, ValueError) as exc:
            logger.warning("Item Steam inválido (%s): %s", app_id, exc)
            return None

    @staticmethod
    def _cents_to_brl(value: int) -> Decimal:
        if value < 0:
            raise ValueError("preço não pode ser negativo")
        return (Decimal(value) / Decimal(100)).quantize(Decimal("0.01"))
