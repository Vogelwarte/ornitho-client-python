from enum import Enum
from typing import List, Optional

from ornitho.api_requester import APIRequester
from ornitho.model.abstract.base_model import BaseModel, check_raw_data, check_refresh
from ornitho.model.abstract.listable_model import ListableModel
from ornitho.model import Site
from ornitho.model.observer import Observer
from ornitho.model.place import Place


class SiteProtocol(Site, ListableModel):
    ENDPOINT: str = "protocol/sites"

    def __init__(self, id_: int) -> None:
        """Site constructor
        :param id_: ID, which is used to get the site from Biolovison
        :type id_: int
        """
        super(SiteProtocol, self).__init__(id_)

    @property  # type: ignore
    @check_refresh
    def id(self) -> int:
        return int(self.id_universal[2:])

    @property  # type: ignore
    @check_refresh
    def id_universal(self) -> str:
        return self._raw_data["id_universal"]

    @property  # type: ignore
    @check_refresh
    def custom_name(self) -> str:
        return self._raw_data["custom_name"]

    @property  # type: ignore
    @check_refresh
    def local_name(self) -> Optional[str]:
        return self._raw_data["local_name"] if "local_name" in self._raw_data else None


    @property  # type: ignore
    @check_refresh
    def reference_locality(self) -> str:
        return self._raw_data["reference_locality"]


