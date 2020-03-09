from abc import ABC
from typing import Any, Dict, List, Union

from ornitho.api_exception import APIException
from ornitho.api_requester import APIRequester


class BaseModel(ABC):
    """Abstract base class for all models"""

    ENDPOINT: str

    def __init__(self, id_: Union[int, str]):
        """ Base model constructor
        :param id_: Unique identifier
        :type id_: Union[int, str]
        """
        super(BaseModel, self).__init__()
        self._id: Union[int, str] = id_
        self._raw_data: Dict[str, Any] = dict()
        self._previous: Dict[str, Any] = dict()

    @property
    def id_(self) -> Union[int, str]:
        """ Unique identifier """
        return self._id

    @classmethod
    def get(cls, id_: Union[int, str]):
        """ Retrieve Object from Biolovision with given ID
        :param id_: Unique identifier
        :type id_: Union[int, str]
        :return: Instance, retrieved from Biolovision with given ID
        :rtype: BaseModel
        """
        instance = cls(id_)
        instance.refresh()
        return instance

    @staticmethod
    def request(
        method: str,
        url: str,
        params: Dict[str, Any] = None,
        body: Dict[str, Any] = None,
    ) -> List[Any]:
        """ Send request to Biolovision and returns response
        :param method: HTTP Method (e.g. 'GET', 'POST', ...)
        :param url: Url to request
        :param params: Additional URL parameters.
        :param body: Request body
        :type method: str
        :type url: str
        :type params: Dict[str, Any]
        :type body: Dict[str, Any]
        :return: Response map from Biolovision
        :rtype: Dict[str, str]
        """
        with APIRequester() as requester:
            response, pagination_key = requester.request(
                method=method, url=url, params=params, body=body
            )
        # noinspection PyTypeChecker
        return response

    @classmethod
    def create_from(cls, data: Dict[str, Any]) -> "BaseModel":
        identifier: Union[int, str]
        if "@id" in data:
            identifier = int(data["@id"]) if data["@id"].isdigit() else data["@id"]
        else:
            identifier = int(data["id"]) if data["id"].isdigit() else data["id"]
        obj = cls(identifier)
        obj._raw_data = data
        return obj

    def refresh(self) -> "BaseModel":
        """ Refresh local model
        Call the api and refresh fields from response
        :return: Refreshed Object
        :rtype: BaseModel
        :raise APIException: No or more than one objects retrieved
        """
        data = self.request(method="GET", url=self.instance_url())
        if len(data) != 1:
            raise APIException(f"Get {len(data)} objects for {self.instance_url()}")
        self._previous = self._raw_data
        self._raw_data = data[0]
        return self

    def instance_url(self) -> str:
        """ Returns url for this instance
        :return: Instance's url
        :rtype: str
        """
        return f"{self.ENDPOINT}/{self.id_}"
