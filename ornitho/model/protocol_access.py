from datetime import date, datetime
from typing import List, Optional, Tuple, Union
from typing import Any, Dict, List, Optional, Union

from ornitho.model.abstract import ListableModel, SearchableModel
from ornitho.model.abstract.base_model import BaseModel, check_raw_data, check_refresh
from ornitho.model.entity import Entity
from ornitho.model.observation import Observation
from ornitho.model.observer_access import ObserverAccess


from abc import ABC
from datetime import date
from typing import List, Optional, Tuple, Type, TypeVar, Union

from ornitho.api_requester import APIRequester
from ornitho.model.abstract import BaseModel

# Create a generic variable that can be 'ListableModel', or any subclass.
T = TypeVar("T", bound="ListableModel")

class ProtocolAccess(ListableModel, SearchableModel):
    ENDPOINT: str = "protocol/access"

    def __init__(self, id_: int) -> None:
        """Protocol constructor
        :param id_: ID, which is used to get the protocol from Biolovison
        :type id_: int
        """
        super(ProtocolAccess, self).__init__(id_)
        self._sites_observer: Optional[List[ObserverAccess]] = None

    @property
    def square_number(self) -> str:
        return self._raw_data["square_number"]

    @property
    def id_original_place(self) -> int:
        return self._raw_data["id_original_place"]

    @property
    def local_site_code(self) -> str:
        return self._raw_data["local_site_code"]




    @property  # type: ignore
    @check_raw_data("observers")
    def sites_observer(self) -> Optional[List[ObserverAccess]]:
        if self._sites_observer is None:
            if "observers" in self._raw_data:
                self._sites_observer = [
                    ObserverAccess.create_from_site(raw_observers)
                    for raw_observers in self._raw_data["observers"]
                ]
        return self._sites_observer



    @classmethod
    def add_sites_observer(
        cls: Type[T],
        body: dict,
        request_all: Optional[bool] = False,
        pagination_key: Optional[str] = None,
        short_version: bool = False,
        retries: int = 0,
        **kwargs: Union[str, int, float, bool, date]
    ) -> str:
        """Retrieves a (paged) list of instances from Biolovison
        If the list is chunked, a pagination key ist returned
        :param request_all: Indicates, if all instances should be retrieved (may result in many API calls)
        :param pagination_key: Pagination key, which can be used to retrieve the next page
        :param short_version: Indicates, if a short version with foreign keys should be returned by the API.
        :param retries: Indicates how many retries should be performed
        :param kwargs: Additional filter values
        :type request_all: bool
        :type pagination_key: Optional[str]
        :type short_version: bool
        :type retries: int
        :type kwargs: Union[str, int, float, bool, date]
        :return: Tuple of instances and pagination key
        :rtype: Tuple[List[T], Optional[str]]
        """
        with APIRequester() as requester:
            url = cls.ENDPOINT
            response, pk = requester.request(
                method="post",
                url=url,
                #body={'id_site': 1560, 'id_observer': 9062},
                body=body,
            )

        return response

    @classmethod
    def delete_sites_observer(
        cls: Type[T],
        id_access: int,
        request_all: Optional[bool] = False,
        pagination_key: Optional[str] = None,
        short_version: bool = False,
        retries: int = 0,
        **kwargs: Union[str, int, float, bool, date]
    ) -> str:
        """Retrieves a (paged) list of instances from Biolovison
        If the list is chunked, a pagination key ist returned
        :param request_all: Indicates, if all instances should be retrieved (may result in many API calls)
        :param pagination_key: Pagination key, which can be used to retrieve the next page
        :param short_version: Indicates, if a short version with foreign keys should be returned by the API.
        :param retries: Indicates how many retries should be performed
        :param kwargs: Additional filter values
        :type request_all: bool
        :type pagination_key: Optional[str]
        :type short_version: bool
        :type retries: int
        :type kwargs: Union[str, int, float, bool, date]
        :return: Tuple of instances and pagination key
        :rtype: Tuple[List[T], Optional[str]]
        """
        with APIRequester() as requester:
            url = cls.ENDPOINT
            response, pk = requester.request(
                method="delete",
                url=url + "/" + str(id_access)
            )

        return response

    @classmethod
    def add_place(
        cls: Type[T],
        body: str,
        request_all: Optional[bool] = False,
        pagination_key: Optional[str] = None,
        short_version: bool = False,
        retries: int = 0,
        **kwargs: Union[str, int, float, bool, date]
    ) -> str:
        """Retrieves a (paged) list of instances from Biolovison
        If the list is chunked, a pagination key ist returned
        :param request_all: Indicates, if all instances should be retrieved (may result in many API calls)
        :param pagination_key: Pagination key, which can be used to retrieve the next page
        :param short_version: Indicates, if a short version with foreign keys should be returned by the API.
        :param retries: Indicates how many retries should be performed
        :param kwargs: Additional filter values
        :type request_all: bool
        :type pagination_key: Optional[str]
        :type short_version: bool
        :type retries: int
        :type kwargs: Union[str, int, float, bool, date]
        :return: Tuple of instances and pagination key
        :rtype: Tuple[List[T], Optional[str]]
        """
        with APIRequester() as requester:
            url = "places"
            response, pk = requester.request(
                method="post",
                url=url,
                #body={'id_site': 1560, 'id_observer': 9062},
                body=body.encode(encoding='utf-8'),
            )

        return response

    @classmethod
    def update_route(
        cls: Type[T],
        body: str,
        place_id: int,
        request_all: Optional[bool] = False,
        pagination_key: Optional[str] = None,
        short_version: bool = False,
        retries: int = 0,
        **kwargs: Union[str, int, float, bool, date]
    ) -> str:
        """Retrieves a (paged) list of instances from Biolovison
        If the list is chunked, a pagination key ist returned
        :param request_all: Indicates, if all instances should be retrieved (may result in many API calls)
        :param pagination_key: Pagination key, which can be used to retrieve the next page
        :param short_version: Indicates, if a short version with foreign keys should be returned by the API.
        :param retries: Indicates how many retries should be performed
        :param kwargs: Additional filter values
        :type request_all: bool
        :type pagination_key: Optional[str]
        :type short_version: bool
        :type retries: int
        :type kwargs: Union[str, int, float, bool, date]
        :return: Tuple of instances and pagination key
        :rtype: Tuple[List[T], Optional[str]]
        """
        with APIRequester() as requester:
            url = "places/" + str(place_id)
            response, pk = requester.request(
                method="put",
                url=url,
                #body={'id_site': 1560, 'id_observer': 9062},
                body=body.encode(encoding='utf-8'),
            )


        return response


    @property
    def test(self) -> str:
        #return self.raw_data_trim_field_ids()
        url = f"{self.ENDPOINT}"
        #params = {"id_protocol": self.id_}

        #response = self.request(method="GET", url=url)
        #return str(self.create_from_ornitho_json(response[0]))
        #return str(response[0])
        return self._raw_data


        #sites_object = self.request(method="get", url=url, params=None)[0]
        #sites_object = self.request[0]
        #return str(sites_object)

    @property
    def sites(self) -> str:
        """Get sites linked to the protocol
        :return: List of sites
        :rtype: List[Site]
        """
        if not self._sites:
            url = f"{self.ENDPOINT}"
            params = {"id_site": 1560}




            sites_object = self.request(method="get", url=url, params=params)[0]
            #self._sites = [Site(id_=site_id) for site_id in sites_object.keys()]
        #return self._sites
        return sites_object





