from datetime import UTC, datetime, time
from math import ceil

from flask import request


def success_response(data, message, status_code=200, pagination=None):
    payload = {"data": data, "message": message}

    if pagination is not None:
        payload["pagination"] = pagination

    return payload, status_code


def pagination_args(default_per_page=10, max_per_page=100):
    try:
        page = int(request.args.get("page", 1))
    except (TypeError, ValueError):
        page = 1

    try:
        per_page = int(request.args.get("per_page", default_per_page))
    except (TypeError, ValueError):
        per_page = default_per_page

    return max(page, 1), min(max(per_page, 1), max_per_page)


def paginated_response(query, serializer, message):
    page, per_page = pagination_args()
    total = query.count()
    pages = ceil(total / per_page) if total else 0
    records = query.limit(per_page).offset((page - 1) * per_page).all()

    return success_response(
        [serializer(record) for record in records],
        message,
        pagination={
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": pages,
        },
    )


def parse_iso_date(value):
    if not value:
        return None

    return datetime.strptime(value, "%Y-%m-%d").date()


def start_of_day(value):
    return datetime.combine(value, time.min, tzinfo=UTC)


def end_of_day(value):
    return datetime.combine(value, time.max, tzinfo=UTC)
