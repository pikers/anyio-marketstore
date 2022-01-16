
from conftest import random_str, generate_tbk, generate_ms_array

async def test_server_version(ms_client):
    assert (
        await ms_client.server_version() == 
        '3862e9973da36cfc6004b88172c08f09269aaf01'
    )

async def test_write_list_symbols(ms_client):
    sym = random_str()
    tbk = generate_tbk(sym=sym)
    data = generate_ms_array(1, 2)
    reply = await ms_client.write(
        data, tbk, True)

    syms = await ms_client.list_symbols()
    assert sym in syms
