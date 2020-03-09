import re
from typing import Union

from ornitho import APIException
from ornitho.api_requester import APIRequester
from ornitho.model.abstract import ListableModel


class FieldOption(ListableModel):
    ENDPOINT: str = ""

    @classmethod
    def get(cls, id_: Union[int, str]):
        """ Retrieve Object from Biolovision with given ID
        :param id_: Unique identifier
        :type id_: str
        :return: Instance, retrieved from Biolovision with given ID
        :rtype: BaseModel
        """
        with APIRequester() as requester:
            if isinstance(id_, str) and re.match(r"(.*)_(.*)", id_):
                url = f"fields/{id_.split('_')[0]}"
            else:
                raise APIException("ID must be string matching (.*)_(.*)")
            response, pagination_key = requester.request(
                method="GET", url=url, params={"short_version": False}
            )
            for option in response:
                field_option = cls.create_from(option)
                if field_option.id_ == id_:
                    return field_option
            raise APIException(f"Can't find field option with ID {id_}")

    def refresh(self):
        raise NotImplementedError

    @property
    def name(self) -> str:
        return self._raw_data["name"]

    @property
    def text(self) -> str:
        return self._raw_data["text"]

    @property
    def value(self) -> int:
        return int(self._raw_data["value"])

    @property
    def order_id(self) -> int:
        return int(self._raw_data["order_id"])
