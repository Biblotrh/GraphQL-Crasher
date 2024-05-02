import aiohttp, asyncio
from py3msp.checksum import calculate_checksum
from py3msp.entities import *
from py3msp.enums import *
from py3msp.construct  import *
from py3msp.construct import _fix_proxy
from typing import *
from aiohttp import ClientSession, ClientResponse

async def send_amf3_request(instance, server: Union[MspServer, str], method: str, params: Union[dict, list], proxy: Optional[str]=None, ensure_https: Optional[bool]=True, retry_attempts: Optional[int]=0, retry_delay: Optional[int]=0) -> AMFResult:
    proxy = proxy_to_be_used(instance, proxy)
    url = match_(f"https://ws-{server}.mspapis.com/Gateway.aspx?method={method}", ensure_https)

    request, envelope = get_request_and_envelope(method=method, params=params)
    encoded_request = remoting.encode(envelope).getvalue()

    for _ in range(retry_attempts + 1 if retry_attempts == 0 else retry_attempts):
        result = await _send_request(instance, instance._session, url, encoded_request, proxy)
        if result.status_code in {200, 400}: return result
        await asyncio.sleep(retry_delay)

    return await _send_request(instance, instance._session, url, encoded_request, proxy)


async def _send_request(instance, session: ClientSession, url: str, encoded_request: bytes, proxy: Optional[str], raise_timeout: Optional[bool]=False) -> AMFResult:
    """
    Sends an HTTP POST request asynchronously using aiohttp.

    Args:
        session (ClientSession): The aiohttp session to use for the request.
        url (str): The URL to send the request to.
        encoded_request (bytes): The encoded request data.
        proxy (Optional[str]): The proxy to use for the request.

    Returns:
        AMFResult: The result of the request.
    """
    try:
        async with session.post(url, data=encoded_request, proxy=_fix_proxy(proxy), headers=instance._headers) as response:
            return await _parse_response(response)
    except asyncio.TimeoutError:
        if raise_timeout: raise asyncio.TimeoutError(f"Server timeout to {url}")
        return AMFResult(None, -5)
    except aiohttp.ClientConnectorError as e:
        return AMFResult(None, e.status if isinstance(e, aiohttp.ClientResponseError) and 400 <= e.status < 500 else 503)
    except Exception: return AMFResult(None, -1)

async def _parse_response(response: ClientResponse):
    """
    Parses the HTTP response from the server.

    Args:
        response (ClientResponse): The response from the server.

    Returns:
        AMFResult: The parsed result of the response.
    """
    return AMFResult(bytes_data=await response.read(), status_code=response.status)

