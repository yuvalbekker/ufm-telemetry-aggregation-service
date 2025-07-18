from enum import Enum
from typing import Any, Dict, Optional

from fastapi import Query


class OrderEnum(str, Enum):
    asc = "asc"
    desc = "desc"

    def get_db_value(self) -> Optional[str]:
        enum_to_db_value = {
            OrderEnum.asc: "ASC",
            OrderEnum.desc: "DESC",
        }
        return enum_to_db_value.get(self)


def common_parameters(
    limit: Optional[int] = Query(
        100, ge=1, le=100, description="The max number of items to return."
    ),
    offset: Optional[int] = Query(
        None,
        description="The number of items to skip before starting to collect the result set.",
    ),
) -> Optional[Dict[str, Any]]:

    return {"limit": limit, "offset": offset}
