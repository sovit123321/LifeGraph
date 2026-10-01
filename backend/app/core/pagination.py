from fastapi import Query


def pagination_params(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    return {
        "page": page,
        "page_size": page_size,
    }