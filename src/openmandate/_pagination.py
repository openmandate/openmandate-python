from __future__ import annotations

from typing import Generic, Iterator, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class SyncPage(Generic[T]):
    """A page of results from a list endpoint.

    Supports iteration over items in the current page and auto-pagination
    across all pages when used with a page-fetcher callback.

    Usage:
        # Iterate over a single page
        page = client.mandates.list(limit=10)
        for mandate in page:
            print(mandate.id)

        # Auto-paginate across all pages
        for mandate in client.mandates.list(status="active"):
            print(mandate.id)
    """

    items: list[T]
    next_token: str | None

    _fetch_next: "_PageFetcher[T] | None"

    def __init__(
        self,
        items: list[T],
        next_token: str | None,
        fetch_next: "_PageFetcher[T] | None" = None,
    ) -> None:
        self.items = items
        self.next_token = next_token
        self._fetch_next = fetch_next

    def __iter__(self) -> Iterator[T]:
        """Iterate over all items across all pages (auto-pagination)."""
        page: SyncPage[T] | None = self
        while page is not None:
            yield from page.items
            if page.next_token is not None and page._fetch_next is not None:
                page = page._fetch_next(page.next_token)
            else:
                page = None

    def __len__(self) -> int:
        """Return the number of items in the current page only."""
        return len(self.items)

    def has_next_page(self) -> bool:
        """Whether there is a next page of results."""
        return self.next_token is not None


class AsyncPage(Generic[T]):
    """An async page of results from a list endpoint.

    Supports async iteration over items in the current page and auto-pagination
    across all pages when used with a page-fetcher callback.

    Usage:
        # Auto-paginate across all pages
        async for mandate in await client.mandates.list(status="active"):
            print(mandate.id)
    """

    items: list[T]
    next_token: str | None

    _fetch_next: "_AsyncPageFetcher[T] | None"

    def __init__(
        self,
        items: list[T],
        next_token: str | None,
        fetch_next: "_AsyncPageFetcher[T] | None" = None,
    ) -> None:
        self.items = items
        self.next_token = next_token
        self._fetch_next = fetch_next

    async def __aiter__(self):  # type: ignore[override]
        """Async iterate over all items across all pages (auto-pagination)."""
        page: AsyncPage[T] | None = self
        while page is not None:
            for item in page.items:
                yield item
            if page.next_token is not None and page._fetch_next is not None:
                page = await page._fetch_next(page.next_token)
            else:
                page = None

    def __len__(self) -> int:
        """Return the number of items in the current page only."""
        return len(self.items)

    def has_next_page(self) -> bool:
        """Whether there is a next page of results."""
        return self.next_token is not None


from typing import Callable, Awaitable  # noqa: E402

_PageFetcher = Callable[[str], SyncPage[T]]
_AsyncPageFetcher = Callable[[str], Awaitable[AsyncPage[T]]]
