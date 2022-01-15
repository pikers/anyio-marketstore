import purerpc
from . import marketstore_pb2 as proto_dot_marketstore__pb2


class MarketstoreServicer(purerpc.Servicer):
    async def Query(self, input_message):
        raise NotImplementedError()

    async def Create(self, input_message):
        raise NotImplementedError()

    async def Write(self, input_message):
        raise NotImplementedError()

    async def Destroy(self, input_message):
        raise NotImplementedError()

    async def ListSymbols(self, input_message):
        raise NotImplementedError()

    async def ServerVersion(self, input_message):
        raise NotImplementedError()

    @property
    def service(self) -> purerpc.Service:
        service_obj = purerpc.Service(
            "proto.Marketstore"
        )
        service_obj.add_method(
            "Query",
            self.Query,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                proto_dot_marketstore__pb2.MultiQueryRequest,
                proto_dot_marketstore__pb2.MultiQueryResponse,
            )
        )
        service_obj.add_method(
            "Create",
            self.Create,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                proto_dot_marketstore__pb2.MultiCreateRequest,
                proto_dot_marketstore__pb2.MultiServerResponse,
            )
        )
        service_obj.add_method(
            "Write",
            self.Write,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                proto_dot_marketstore__pb2.MultiWriteRequest,
                proto_dot_marketstore__pb2.MultiServerResponse,
            )
        )
        service_obj.add_method(
            "Destroy",
            self.Destroy,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                proto_dot_marketstore__pb2.MultiKeyRequest,
                proto_dot_marketstore__pb2.MultiServerResponse,
            )
        )
        service_obj.add_method(
            "ListSymbols",
            self.ListSymbols,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                proto_dot_marketstore__pb2.ListSymbolsRequest,
                proto_dot_marketstore__pb2.ListSymbolsResponse,
            )
        )
        service_obj.add_method(
            "ServerVersion",
            self.ServerVersion,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                proto_dot_marketstore__pb2.ServerVersionRequest,
                proto_dot_marketstore__pb2.ServerVersionResponse,
            )
        )
        return service_obj


class MarketstoreStub:
    def __init__(self, channel):
        self._client = purerpc.Client(
            "proto.Marketstore",
            channel
        )
        self.Query = self._client.get_method_stub(
            "Query",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                proto_dot_marketstore__pb2.MultiQueryRequest,
                proto_dot_marketstore__pb2.MultiQueryResponse,
            )
        )
        self.Create = self._client.get_method_stub(
            "Create",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                proto_dot_marketstore__pb2.MultiCreateRequest,
                proto_dot_marketstore__pb2.MultiServerResponse,
            )
        )
        self.Write = self._client.get_method_stub(
            "Write",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                proto_dot_marketstore__pb2.MultiWriteRequest,
                proto_dot_marketstore__pb2.MultiServerResponse,
            )
        )
        self.Destroy = self._client.get_method_stub(
            "Destroy",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                proto_dot_marketstore__pb2.MultiKeyRequest,
                proto_dot_marketstore__pb2.MultiServerResponse,
            )
        )
        self.ListSymbols = self._client.get_method_stub(
            "ListSymbols",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                proto_dot_marketstore__pb2.ListSymbolsRequest,
                proto_dot_marketstore__pb2.ListSymbolsResponse,
            )
        )
        self.ServerVersion = self._client.get_method_stub(
            "ServerVersion",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                proto_dot_marketstore__pb2.ServerVersionRequest,
                proto_dot_marketstore__pb2.ServerVersionResponse,
            )
        )
