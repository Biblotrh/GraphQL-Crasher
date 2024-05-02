from typing import Optional, Any
import aiohttp, asyncio
from py3msp.construct import get_session, close_session
from py3msp.conditions import requires_login
from py3msp.ticket_header import Authorization
from py3msp.enums import MspServer, MspRequestError
from py3msp.entities import *
from py3msp.commands import send_amf3_request
from py3msp.helpers import return_login_response
from py3msp import mspsocket
from py3msp.nebula import NebulaAsyncClient
import pyamf, atexit

class AsyncClient:
    """
    Asynchronous client for interacting with a remote service.

    Attributes:
        _session (aiohttp.ClientSession): An aiohttp ClientSession object for handling HTTP requests.
        _authorization (Authorization): An Authorization object for managing authentication.
        _https (bool): Whether to use HTTPS. Defaults to True.
        _retry_attempts (int): Number of retry attempts for failed requests. Defaults to 3.
        _retry_delay (int): Delay between retry attempts in seconds. Defaults to 0.
        _proxy (str): Proxy URL if applicable.
        _headers (dict): Default headers for HTTP requests.
    """

    def __init__(
        self,
        verify_ssl: Optional[bool] = True,
        timeout: Optional[int] = 5,
        https: Optional[bool] = True,
        retry_attempts: Optional[int] = 3,
        retry_delay: Optional[int] = 0,
        proxy: Optional[str] = None
    ) -> None:
        """
        Initialize the AsyncClient with the specified settings.

        Parameters:
            verify_ssl (Optional[bool]): Whether to verify SSL certificates. Defaults to True.
            timeout (Optional[int]): Total timeout value in seconds for the session. Defaults to 5.
            https (Optional[bool]): Whether to use HTTPS. Defaults to True.
            retry_attempts (Optional[int]): Number of retry attempts for failed requests. Defaults to 3.
            retry_delay (Optional[int]): Delay between retry attempts in seconds. Defaults to 0.
            proxy (Optional[str]): Proxy URL if applicable.
        """
        self._session: aiohttp.ClientSession = get_session(verify_ssl=verify_ssl, timeout=timeout)
        self._authorization: Authorization = Authorization(parent=self)
        self._https = https
        self._retry_attempts = retry_attempts
        self._retry_delay = retry_delay
        self._proxy = proxy
        self._headers = {
            'User-Agent': 'mspwebservice-f9',
            'Referer': 'app:/cache/t1.bin/[[DYNAMIC]]/2',
            'Content-Type': 'application/x-amf'
        }
        self._websocket = mspsocket.MspSocketUser()
        atexit.register(self.close_session)

    def close_session(self):
        """
        Close the aiohttp session when the program exits.
        """
        if getattr(self, '_session', None) is not None:
            asyncio.run(close_session(self._session))
    
    @requires_login
    def ticket_header(self) -> pyamf.ASObject:
        """Returns the updated `TicketHeader` attribute as an ASObject."""
        return self._authorization.generate_ticket_header()
    
    async def send_command_async(self, server: Union[MspServer, str], method: str, params: Union[dict, list], proxy: Optional[str] = None) -> AMFResult:
        """
        Sends a command asynchronously.

        Args:
            self: The instance.
            server (MspServer or str): The server to send the command to.
            method (str): The method to call.
            params (dict or list): Parameters for the method.
            proxy (str, optional): The proxy to use, if any. Defaults to None.

        Returns:
            AMFResult: The result of the command.
        """
        return await send_amf3_request(
            instance=self,
            server=server,
            method=method,
            params=params,
            proxy=proxy,
            ensure_https=self._https,
            retry_attempts=self._retry_attempts,
            retry_delay=self._retry_delay
        )
    
    async def login_async(self, username: str, password: str, server: Union[MspServer, str], proxy: Optional[str] = None, websocket: bool = True) -> LoginResult:
        """
        Asynchronous function for logging in with the provided username, password, server, and optional proxy.

        Args:
            username (str): The username for logging in.
            password (str): The password for logging in.
            server (MspServer): The MovieStarPlanet server.
            proxy (Optional[str]): The proxy to use for the request.
            websocket (bool): Flag indicating whether to connect to websocket after successful login.

        Returns:
            LoginResult: The result of the login operation.
        """
        login = return_login_response(await self.send_command_async(server=server, method='MovieStarPlanet.WebService.User.AMFUserServiceWeb.Login', params=[username, password, [], None, None, "MSP1-Standalone:XXXXXX"], proxy=proxy))
        if login.loginStatus.status in {'ThirdPartyCreated', 'Success'} and login.loginStatus is not None:
            self.ticket, self.actor_id, self.server, self.username, self.logged_in = login.loginStatus.ticket, login.loginStatus.ActorId, server, username, True
            self.access_token, self.profileId = login.loginStatus.nebulaLoginStatus['accessToken'], login.loginStatus.nebulaLoginStatus['profileId']
            self.nebula = NebulaAsyncClient(parent=self)

            if websocket:
                await self._websocket.connect(server=server)
                await self._websocket.send_authentication(server=server, access_token=self.access_token, profile_id=self.profileId)

        return login





