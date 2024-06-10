import datetime as dt
import statistics
import typing as tp

from homework07.research.vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """

    def get_ages(
        _friends: tp.List[tp.Dict[str, tp.Any]]
    ) -> tp.Generator[int, None, None]:
        for friend in _friends:
            birthdate = friend.get("bdate")

            if not birthdate or birthdate.count(".") < 2:
                continue
            birthdate = dt.datetime.strptime(birthdate, "%d.%m.%Y")
            yield (dt.datetime.now() - birthdate).days // 365

    friends = tp.cast(
        tp.List[tp.Dict[str, tp.Any]],
        get_friends(user_id=user_id, fields=["bdate"]).items,
    )
    if not friends:
        return None

    ages = list(get_ages(friends))
    if not ages:
        return None
    return statistics.mean(ages)
