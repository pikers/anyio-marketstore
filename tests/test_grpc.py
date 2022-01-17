
from conftest import random_str, generate_tbk, generate_ms_array

from anyio_marketstore.params import Params


async def test_server_version(ms_client):
    assert (
        len(await ms_client.server_version()) == 
        len('3862e9973da36cfc6004b88172c08f09269aaf01')
    )

async def test_write_and_query(ms_client):
    sym = random_str()
    tf = '1Sec'
    attr_group = 'TEST'
    tbk = generate_tbk(sym=sym, timeframe='1Sec', attr_group=attr_group)

    data = generate_ms_array(1, 2)
    reply = await ms_client.write(
        data, tbk, True)

    params = Params(sym, tf, attr_group)
    reply = await ms_client.query(params)
    
    assert len(reply.results) == 1

    result = reply.results[0].result

    assert tbk in result

    result = result[tbk]

    assert data == result.array 

async def test_create_list_symbols_and_delete(ms_client):

    sym = random_str()
    tbk = generate_tbk(sym=sym)

    dtype = [('Epoch', 'i8'), ('Ask', 'f4')]

    reply = await ms_client.create(tbk, dtype)

    while len(reply.responses) > 0:
        assert reply.responses.pop().error == ''

    assert sym in await ms_client.list_symbols()

    reply = await ms_client.destroy(tbk)

    while len(reply.responses) > 0:
        assert reply.responses.pop().error == ''

    assert sym not in await ms_client.list_symbols()
