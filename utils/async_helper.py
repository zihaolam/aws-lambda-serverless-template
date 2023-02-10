from asyncio import get_event_loop, gather
from typing import Callable, List


def run_async(*funcs: List[Callable]) -> list:
    loop = get_event_loop()
    return loop.run_until_complete(gather(*funcs))
