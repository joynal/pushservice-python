import collections
import itertools


def dict_to_sql(query: str, data: dict):
    return query.format(', '.join('%({})s'.format(key) for key in data))


# code borrowed from https://github.com/MagicStack/asyncpg/issues/9#issuecomment-600659015
def pyformat_to_sql(query: str, named_args: dict[str, any]) -> tuple[str, list[any]]:
    positional_generator = itertools.count(1)
    positional_map = collections.defaultdict(lambda: '${}'.format(next(positional_generator)))
    formatted_query = query % positional_map
    positional_items = sorted(
        positional_map.items(),
        key=lambda item: int(item[1].replace('$', '')),
    )
    positional_args = [named_args[named_arg] for named_arg, _ in positional_items]
    return formatted_query, positional_args


def pyformat_to_sql_many(query: str, named_args: list[dict[str, any]]) -> tuple[str, list[any]]:
    arg_items = []
    positional_generator = itertools.count(1)
    positional_map = collections.defaultdict(lambda: '${}'.format(next(positional_generator)))
    formatted_query = query % positional_map

    for arg_item in named_args:
        positional_items = sorted(
            positional_map.items(),
            key=lambda item: int(item[1].replace('$', '')),
        )
        positional_args = [arg_item[named_arg] for named_arg, _ in positional_items]
        arg_items.append(positional_args)

    return formatted_query, arg_items
