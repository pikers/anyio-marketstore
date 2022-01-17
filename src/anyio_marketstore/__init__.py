from typing import List, Union, Tuple
from contextlib import asynccontextmanager

import numpy as np
import purerpc

from .proto import (
    MarketstoreStub,
    ServerVersionRequest,
    MultiCreateRequest,
    CreateRequest,
    DataShape,
    MultiWriteRequest,
    WriteRequest,
    NumpyMultiDataset,
    NumpyDataset,
    ListSymbolsRequest,
    QueryRequest,
    MultiQueryRequest,
    MultiKeyRequest,
    KeyRequest,
    MultiServerResponse
)
from .params import ListSymbolsFormat, Params, isiterable
from .results import QueryReply


class MarketstoreClient:

    def __init__(
        self,
        stub: MarketstoreStub
    ):
        self.stub = stub

    async def server_version(self) -> str:
        reply = await self.stub.ServerVersion(ServerVersionRequest())
        return reply.version

    async def create(
        self,
        tbk: str,
        dtype: List[Tuple[str, str]],
        isvariablelength: bool = False
    ) -> MultiServerResponse:
        req = MultiCreateRequest(requests=[
            CreateRequest(
                key="{}:Symbol/Timeframe/AttributeGroup".format(tbk),
                data_shapes=[DataShape(name=name, type=typ) for name, typ in dtype],
                row_type="variable" if isvariablelength else "fixed",
            )
        ])

        return await self.stub.Create(req)

    async def write(
        self,
        recarray: np.array,
        tbk: str,
        isvariablelength: bool = False
    ) -> MultiServerResponse:
        types = [
            recarray.dtype[name].str.replace('<', '').replace('|', '')
            for name in recarray.dtype.names
        ]
        names = recarray.dtype.names
        data = [
            bytes(memoryview(recarray[name]))
            for name in recarray.dtype.names
        ]
        length = len(recarray)
        start_index = {tbk: 0}
        lengths = {tbk: len(recarray)}

        req = MultiWriteRequest(requests=[
            WriteRequest(
                data=NumpyMultiDataset(
                    data=NumpyDataset(
                        column_types=types,
                        column_names=names,
                        column_data=data,
                        length=length,
                        # data_shapes = [],
                    ),
                    start_index=start_index,
                    lengths=lengths,
                ),
                is_variable_length=isvariablelength,
            )
        ])

        return await self.stub.Write(req)

    async def list_symbols(
        self,
        fmt: ListSymbolsFormat = ListSymbolsFormat.SYMBOL
    ) -> List[str]:

        if fmt == ListSymbolsFormat.TBK:
            req_format = ListSymbolsRequest.Format.TIME_BUCKET_KEY
        else:
            req_format = ListSymbolsRequest.Format.SYMBOL

        resp = await self.stub.ListSymbols(
            ListSymbolsRequest(format=req_format))

        if resp is None:
            return []

        return resp.results

    def build_query(self, params: Union[Params, List[Params]]) -> MultiQueryRequest:
        reqs = MultiQueryRequest(requests=[])
        if not isiterable(params):
            params = [params]
        for param in params:
            req = QueryRequest(
                destination=param.tbk,
            )

            if param.key_category is not None:
                req.key_category = param.key_category
            if param.start is not None:
                req.epoch_start = int(param.start.value / (10 ** 9))

                # support nanosec
                start_nanosec = int(param.start.value % (10 ** 9))
                if start_nanosec != 0:
                    req.epoch_start_nanos = start_nanosec

            if param.end is not None:
                req.epoch_end = int(param.end.value / (10 ** 9))

                # support nanosec
                end_nanosec = int(param.end.value % (10 ** 9))
                if end_nanosec != 0:
                    req.epoch_end_nanos = end_nanosec

            if param.end is not None:
                req.epoch_end = int(param.end.value / (10 ** 9))
            if param.limit is not None:
                req.limit_record_count = int(param.limit)
            if param.limit_from_start is not None:
                req.limit_from_start = bool(param.limit_from_start)
            if param.functions is not None:
                req.functions.extend(param.functions)
            reqs.requests.append(req)
        return reqs

    async def query(self, params: Union[Params, List[Params]]) -> QueryReply:
        if not isiterable(params):
            params = [params]
        reqs = self.build_query(params)

        reply = await self.stub.Query(reqs)

        return QueryReply.from_grpc_response(reply)

    async def destroy(self, tbk: str) -> MultiServerResponse:
        '''
        Delete a bucket
        :param tbk: Time Bucket Key Name (i.e. "TEST/1Min/Tick" )
        '''

        req = MultiKeyRequest(requests=[KeyRequest(key=tbk)])
        return await self.stub.Destroy(req)

@asynccontextmanager
async def open_marketstore_client(
    host: str = 'localhost',
    port: int = 5995
):
    async with purerpc.insecure_channel(host, port) as channel:
        client = MarketstoreClient(
            MarketstoreStub(channel))
        yield client
