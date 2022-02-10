import collections
import itertools
from typing import TypeVar

T = TypeVar("T")


def dict_to_sql(query: str, data: dict):
    return query.format(", ".join(f"{key}=%({key})s" for key in data))


def pyformat_to_sql(query: str, named_args: dict[str, T]) -> tuple[str, list[T]]:
    positional_generator = itertools.count(1)
    positional_map: collections.defaultdict = collections.defaultdict(
        lambda: f"${next(positional_generator)}"
    )
    formatted_query = query % positional_map
    positional_items = sorted(
        positional_map.items(),
        key=lambda item: int(item[1].replace("$", "")),
    )
    positional_args = [named_args[named_arg] for named_arg, _ in positional_items]
    return formatted_query, positional_args


def pyformat_to_sql_many(
    query: str, named_args: list[dict[str, T]]
) -> tuple[str, list[list[T]]]:
    arg_items = []
    positional_generator = itertools.count(1)
    positional_map: collections.defaultdict = collections.defaultdict(
        lambda: f"${next(positional_generator)}"
    )
    formatted_query = query % positional_map

    for arg_item in named_args:
        positional_items = sorted(
            positional_map.items(),
            key=lambda item: int(item[1].replace("$", "")),
        )
        positional_args = [arg_item[named_arg] for named_arg, _ in positional_items]
        arg_items.append(positional_args)

    return formatted_query, arg_items
