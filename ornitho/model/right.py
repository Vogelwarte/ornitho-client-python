from typing import List, Union

from ornitho import APIRequester


class Right:
    ENDPOINT: str = "observers/rights"

    def __init__(self, id_: int, name: str, restrictions: str) -> None:
        """Detail constructor
        :param id: ID
        :param name: Name
        :param comment: Comment
        :type id: int
        :type name: str
        :type comment: str
        """
        self.id_: int = id_
        self.name: str = name
        # self.comment: str = comment
        # self.right_id: int = right_id
        self.restrictions: str = restrictions

    def __str__(self) -> str:
        return f"{self.id_}-{self.name}-{self.comment}-{self.right_id}"

    @classmethod
    def retrieve_for_observer(cls, id_observer: Union[int, str]) -> List["Right"]:
        with APIRequester() as requester:
            url = f"{cls.ENDPOINT}/{id_observer}"
            response, pk = requester.request_raw(
                method="get",
                url=url,
            )
        return (
            [
            cls(id_=int(right["id"]), name=right["name"], restrictions=right["restrictions"])
                for right in response["data"]["rights"]
            ]
            if "rights" in response["data"]
            else []
        )

    # gha, 14.03.2023
    @classmethod
    def retrieve_proto_for_observer(cls, id_observer: Union[int, str]) -> List["Right"]:
        with APIRequester() as requester:
            # url = f"{cls.ENDPOINT}/{id_observer}"
            # url = f"{cls.ENDPOINT}?id_observer={id_observer}"
            url = f"{cls.ENDPOINT}"

            params = {"id_observer": id_observer}

            response, pk = requester.request_raw(
                method="get",
                url=url,
                params=params,
            )

        # print(response["data"]["rights"])
        #
        # prot_list = []
        # for right in response["data"]["rights"]:
        #     if right["id"] == '59':
        #         for right_prot in right["restrictions"]["59"]["protocols"]:
        #             prot_list.append(int(right_prot))
        # return prot_list

        return (
            [
                cls(id_=int(right["id"]), name=right["name"], restrictions=right["restrictions"])
                for right in response["data"]["rights"]
            ]
            if "rights" in response["data"]
            else []
        )



    @classmethod
    def delete_right_old(cls,
        right_id: int,
    ) -> str:

        with APIRequester() as requester:
            url = cls.ENDPOINT
            response, pk = requester.request(
                method="delete",
                url=url,
                params = {'id_right': right_id}
            )

        return response

    @classmethod
    def delete_right(cls,
        right_id: int,
    ) -> str:

        with APIRequester() as requester:
            url = f"{cls.ENDPOINT}/{right_id}"
            response, pk = requester.request(
                method="delete",
                url=url,
            )

        return response

    @classmethod
    def add_right(cls,
        body: dict
    ) -> str:
        with APIRequester() as requester:
            url = cls.ENDPOINT
            response, pk = requester.request(
                method="post",
                url=url,
                #body={'id_site': 1560, 'id_observer': 9062},
                body=body,
            )

        return response