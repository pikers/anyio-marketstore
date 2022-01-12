
import purerpc

from .proto.marketstore_pb2_grpc import MarketstoreStub


async def open_marketstore_grpc(
    host: str = 'localhost',
    port: int = 5993
):
    async with purepc.insecure_channel(host, port) as channel:
        yield MarketstoreStub(channel)
