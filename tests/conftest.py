
import time
import random

from string import ascii_lowercase as letters
from typing import Optional

import numpy as np
import pytest

from anyio_marketstore import open_marketstore_client


@pytest.fixture
async def ms_client():
    async with open_marketstore_client() as client:
        yield client

def random_str():
    return ''.join(random.choice(letters) for _ in range(4))

def generate_tbk(
    sym: Optional[str] = None,
    timeframe: str = '1Sec',
    attr_group: Optional[str] = None
) -> str:

    if not sym:
        sym = random_str() 
    if not attr_group:
        attr_group = random_str()

    return f'{sym}/{timeframe}/{attr_group}'

_quote_dt = [
    ('Epoch', 'i8'),
    ('Nanoseconds', 'i4'),
    ('Price', 'f8'),
    ('Size', 'f8')
]
def generate_ms_array(
    price: float,
    size: float,
    timestamp: Optional[float] = None
) -> np.array:
    """Return marketstore writeable structarray.
    """
    if not timestamp:
        timestamp = time.time_ns()
        
    secs, ns = timestamp / 10**9, timestamp % 10**9

    # pack into List[Tuple[str, Any]]
    array_input = [secs, ns, price, size]

    return np.array([tuple(array_input)], dtype=_quote_dt)
