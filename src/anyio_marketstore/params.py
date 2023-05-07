from typing import Union, List, Any
import pendulum
import numpy as np
from enum import Enum


def get_timestamp(value: Union[float, int, str]) -> pendulum.DateTime:

    if value is None:
        return None

    if isinstance(value, (float, float, int, np.integer)):
        return pendulum.from_timestamp(value)

    return pendulum.parse(value)


def isiterable(something: Any) -> bool:
    """
    check if something is a list, tuple or set
    :param something: any object
    :return: bool. true if something is a list, tuple or set
    """
    return isinstance(something, (list, tuple, set))


class ListSymbolsFormat(Enum):
    """
    format of the list_symbols response.
    """
    # symbol names only. (e.g. ["AAPL", "AMZN", ...])
    SYMBOL = "symbol"
    # {symbol}/{timeframe}/{attribute_group} format.
    # (e.g. ["AAPL/1Min/TICK", "AMZN/1Sec/OHLCV",...])
    TBK = "tbk"


class Params(object):

    def __init__(
        self,
        symbols: Union[List[str], str],
        timeframe: str,
        attrgroup: str,
        start: Union[int, str] = None,
        end: Union[int, str] = None,
        limit: int = None,
        limit_from_start: bool = None,
        columns: List[str] = None,
        functions: List[str] = None
    ):
        if not isiterable(symbols):
            symbols = [symbols]

        # tbk elements
        self.symbols = symbols
        self.timeframe = timeframe
        self.attrgroup = attrgroup

        self.key_category = None  # server default
        self.start = get_timestamp(start)
        self.end = get_timestamp(end)
        self.limit = limit
        self.limit_from_start = limit_from_start
        self.columns = columns
        self.functions = functions
        self._mk_tbk()

    def _mk_tbk(self) -> str:
        self.tbk = (
            ','.join(self.symbols) +
            "/" + self.timeframe +
            "/" + self.attrgroup
        )
        return self.tbk

    def set(
        self,
        key: str,
        val: Any,

    ) -> None:
        if not hasattr(self, key):
            raise AttributeError()

        if key in ('timeframe', 'symbols', 'attrgroup'):
            setattr(self, key, val)
            self._mk_tbk()

        elif key in ('start', 'end'):
            setattr(self, key, get_timestamp(val))

        else:
            setattr(self, key, val)

    def __repr__(self) -> str:
        content = ('tbk={}, start={}, end={}, '.format(
            self.tbk, self.start, self.end,
        ) +
                   'limit={}, '.format(self.limit) +
                   'limit_from_start={}, '.format(self.limit_from_start) +
                   'columns={}'.format(self.columns))
        return 'Params({})'.format(content)
