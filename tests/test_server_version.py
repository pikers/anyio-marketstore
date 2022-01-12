
from trio_marketstore import open_marketstore_grpc

from trio_marketstore.proto.marketstore_pb2 import ServerVersionRequest


async def test_server_version():
    async with open_marketstore_grpc() as stub:
        reply = await stub.ServerVersion(
            ServerVersionRequest())

        assert reply.version == '1f627561ca90aab7ac047a492cec24c5fe3e60dc'  
