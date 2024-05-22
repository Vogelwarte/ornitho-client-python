from datetime import datetime
from typing import List, Optional
from typing import Any, Dict, List, Optional, Union

from ornitho.model.abstract import ListableModel
from ornitho.model.abstract.base_model import check_refresh, BaseModel
from ornitho.model.right import Right


class ObserverAccess(BaseModel):
    ENDPOINT: str = ""
    name: str = ""
    surname: str = ""
    id_access: int = 0

    def __init__(self, id_) -> None:
        """Observer constructor
        :param id_: ID, which is used to get the observer from Biolovison – None if a new observation will be created
        :type id_: int
        """
        super().__init__(id_)






    @classmethod
    def create_from_site(cls, data: Dict[str, Any]):
        identifier: int = int(data["id"])
        obj = cls(identifier)
        obj.surname  = data["surname"] if "surname" in data else None
        obj.name = data["name"] if "name" in data else None
        obj.id_access = data["id_access"] if "id_access" in data else None
        return obj