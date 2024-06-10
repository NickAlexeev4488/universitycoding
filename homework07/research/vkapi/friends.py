import dataclasses
import math
import time
import typing as tp

from homework07.research.vkapi import config
from homework07.research.vkapi.session import Session
from homework07.research.vkapi.exceptions import APIError

default_session = Session(config.VK_CONFIG["domain"])
QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int,
    count: int = 5000,
    offset: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    params = {
        "user_id": user_id,
        "count": count,
        "offset": offset,
        "fields": fields,
        "v": config.VK_CONFIG["version"],
        "access_token": config.VK_CONFIG["access_token"],
    }
    response = default_session.get(url="friends.get", params=params)
    data = response.json().get("response")
    if not data:
        raise APIError(response.json())
    return FriendsResponse(count=data["count"], items=data["items"])


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    if target_uids is not None and len(target_uids) > 100:
        mutual_friends: tp.List[MutualFriends] = []
        for i in range(math.ceil(len(target_uids) / 100)):
            offset = i * 100
            mutual_friends.extend(
                tp.cast(
                    list[MutualFriends],
                    get_mutual(
                        source_uid=source_uid,
                        target_uid=None,
                        target_uids=target_uids[offset: offset + 100],
                        order=order,
                        count=count,
                        offset=offset,
                        progress=progress,
                    ),
                )
            )
            time.sleep(
                0.34
            )
        return mutual_friends

    params = {
        "v": config.VK_CONFIG["version"],
        "access_token": config.VK_CONFIG["access_token"],
        "need_common_count": "0",
        "source_uid": source_uid,
        "target_uid": target_uid,
        "target_uids": ",".join(map(str, target_uids)) if target_uids else None,
        "order": order,
        "count": count,
        "offset": offset,
    }
    params = {k: v for k, v in params.items() if v is not None}
    response = default_session.get("friends.getMutual", params=params)
    data = response.json().get("response")
    if not data:
        raise APIError(response.json())
    return data
