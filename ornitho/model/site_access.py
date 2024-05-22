from enum import Enum
from typing import List, Optional
from typing import Any, Dict, List, Optional, Tuple, Union
from ornitho import APIException

from ornitho.api_requester import APIRequester
from ornitho.model.abstract.base_model import BaseModel, check_raw_data, check_refresh
from ornitho.model.observer import Observer
from ornitho.model.observer_access import ObserverAccess
from ornitho.model.place import Place



class SiteAccess(BaseModel):
    ENDPOINT: str = "protocol/access"

    def __init__(self, id_: int) -> None:
        """Site constructor
        :param id_: ID, which is used to get the site from Biolovison
        :type id_: int
        """
        super(SiteAccess, self).__init__(id_)

    @property  # type: ignore
    @check_refresh
    def square_number(self) -> str:
        return self._raw_data["square_number"]

    @property  # type: ignore
    @check_refresh
    def id_original_place(self) -> str:
        return self._raw_data["id_original_place"]

    @property  # type: ignore
    @check_refresh
    def local_site_code(self) -> Optional[str]:
        return self._raw_data["local_site_code"] if "local_site_code" in self._raw_data else None

    @property  # type: ignore
    @check_refresh
    def advanced(self) -> Optional[str]:
        return self._raw_data["advanced"] if "advanced" in self._raw_data else None

    # @classmethod
    # def create_from_ornitho_json(cls, data: Dict[str, Any]) -> "ObserverAccess":
    #     if len(data["observers"]) > 1:
    #         raise APIException(
    #             f"More than one observer in sightings json found!\n{data['observers']}"
    #         )
    #     identifier: Optional[int] = (
    #         int(data["observers"][0]["id_sighting"])
    #         if "observers" in data and "id_sighting" in data["observers"][0]
    #         else None
    #     )
    #     obj = cls(identifier)
    #     obj._raw_data = data
    #     return obj
    #
    #
    # @property  # type: ignore
    # @check_refresh
    # def observers(self) -> List[ObserverAccess]:
    #     observers = []
    #     if "observers" in self._raw_data:
    #         observers = [
    #             Observer(id_=int(observer_id))
    #             for observer_id in self._raw_data["observers"]
    #         ]
    #     return observers


