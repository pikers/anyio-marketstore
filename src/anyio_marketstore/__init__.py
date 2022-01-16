from enum import Enum
from typing import List, Union, Tuple
from contextlib import asynccontextmanager

import numpy as np
import purerpc

from .proto import (
    MarketstoreStub,
    ServerVersionRequest,
    MultiWriteRequest,
    WriteRequest,
    NumpyMultiDataset,
    NumpyDataset,
    ListSymbolsRequest,
    MultiServerResponse
)


class ListSymbolsFormat(Enum):
    """
    format of the list_symbols response.
    """
    # symbol names only. (e.g. ["AAPL", "AMZN", ...])
    SYMBOL = "symbol"
    # {symbol}/{timeframe}/{attribute_group} format. (e.g. ["AAPL/1Min/TICK", "AMZN/1Sec/OHLCV",...])
    TBK = "tbk"


class MarketstoreClient:

    def __init__(
        self,
        stub: MarketstoreStub
    ):
        self.stub = stub

    async def server_version(self) -> str:
        reply = await self.stub.ServerVersion(ServerVersionRequest())
        return reply.version

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

@asynccontextmanager
async def open_marketstore_client(
    host: str = 'localhost',
    port: int = 5995
):
    async with purerpc.insecure_channel(host, port) as channel:
        client = MarketstoreClient(
            MarketstoreStub(channel))
        yield client
