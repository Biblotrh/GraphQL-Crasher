import aiohttp, base64, pyamf
from secrets import token_hex
from aiohttp import TCPConnector, ClientTimeout
from typing import Optional, Any, Union
from pyamf import remoting, AMF3
from pyamf.remoting import Request, Envelope, HeaderCollection
from py3msp.checksum import calculate_checksum

def get_session(
        verify_ssl: Optional[bool] = True, timeout: Optional[int] = 5) -> aiohttp.ClientSession:
    """
    Create and return an aiohttp ClientSession object with specified SSL verification and timeout.

    Parameters:
        verify_ssl (Optional[bool]): Whether to verify SSL certificates. Defaults to True.
        timeout (Optional[int]): Total timeout value in seconds for the session. Defaults to 5.

    Returns:
        aiohttp.ClientSession: An aiohttp ClientSession object configured with provided parameters.
    """
    connector = TCPConnector(ssl=verify_ssl, limit=999999)
    return aiohttp.ClientSession(connector=connector, timeout=ClientTimeout(total=timeout))

async def close_session(session: aiohttp.ClientSession) -> None:
    await session.close()

def _fix_proxy(proxy: str) -> str | None:
    """
    Fixes the proxy format to ensure it starts with 'http://' if not None.

    Args:
        proxy (str): The proxy string to fix.

    Returns:
        str | None: The fixed proxy string or None if proxy is None.
    """
    return proxy if proxy is None or proxy.startswith("http") else f'http://{proxy}'

def proxy_to_be_used(instance: Any, proxy: str) -> str:
    """
    Determine the proxy to be used, prioritizing instance.proxy over the provided proxy.

    Args:
        instance (Any): The instance containing the proxy attribute.
        proxy (str): The provided proxy string.

    Returns:
        str: The proxy string to be used.
    """
    # Use instance.proxy if it's not None, otherwise use the provided proxy
    return instance._proxy if instance._proxy is not None else proxy

def match_(url: str, ensure_https: bool):
    """
    Replaces 'http://' with 'https://' in the given URL if ensure_https is True.
    
    Parameters:
        url (str): The URL to be modified.
        ensure_https (bool): If True, the URL will be modified to use 'https://' instead of 'http://'.
        
    Returns:
        str: The modified URL if ensure_https is True, otherwise returns the original URL.
    """
    if ensure_https:
        return str(url).replace('http://', 'https://')
    return str(url).replace('https://', 'http://')
    

def get_request_and_envelope(method: str, params: Union[dict, list]) -> tuple[Request, Envelope]:
    """
    Creates a request and an envelope for remoting.

    Args:
        method (str): The method to be called.
        params (dict or list): Parameters to be sent with the request.

    Returns:
        Request: The remoting request object.
        Envelope: The envelope for the remoting request.
    """
    req = Request(target=method, body=params)
    
    envelope = Envelope(AMF3)
    envelope.headers = HeaderCollection({
        ("sessionID", False, get_session_id()),
        ("needClassName", False, False),
        ("id", False, calculate_checksum(arguments=params))
    })
    envelope['/1'] = req
    return req, envelope

def get_session_id() -> str:
    """
    Generates a random session id.

    Returns:
        str: A randomly generated session id.
    """
    return base64.b64encode(token_hex(23).encode()).decode()