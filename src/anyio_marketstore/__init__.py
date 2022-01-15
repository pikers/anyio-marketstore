
from contextlib import asynccontextmanager

import purerpc

from .proto.marketstore_grpc import MarketstoreStub


@asynccontextmanager
async def open_marketstore_grpc(
    host: str = 'localhost',
    port: int = 5995
):
    async with purerpc.insecure_channel(host, port) as channel:
        yield MarketstoreStub(channel)
