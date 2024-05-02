import asyncio
import json
import aiohttp
import websockets
import atexit
from py3msp.construct import close_session

class MspSocketUser:
    """
    Represents a user connecting to MSP (MovieStarPlanet) WebSocket server.
    """

    def __init__(self):
        """
        Initializes the MspSocketUser.
        """
        self.websocket = None
        self.connected = False
        self.ping_id = 0
        self.session = aiohttp.ClientSession()
        atexit.register(self.close_session)

    def close_session(self):
        """
        Close the aiohttp session when the program exits.
        """
        if getattr(self, 'session', None) is not None:
            asyncio.run(close_session(self.session))

    async def connect(self, server: str):
        """
        Connects to the MSP WebSocket server.

        Args:
            server (str): The server location (e.g., "US").
        """
        self.websocket_path = await self.get_web_socket_url(server)
        uri = f"ws://{self.websocket_path.replace('-', '.')}:{10843}/{self.websocket_path.replace('.', '-')}/?transport=websocket"
        self.websocket = await websockets.connect(uri)
        self.connected = True
        asyncio.create_task(self.send_ping())

    async def send_ping(self):
        """
        Sends a ping message to the server every 5 seconds.
        """
        await asyncio.sleep(5)
        ping_message = {"pingId": self.ping_id, "messageType": 500}
        await self.websocket.send(f"42[\"500\",{json.dumps(ping_message)}]")
        self.ping_id += 1

    async def wait_is_connected(self):
        """
        Waits until the websocket connection is established.
        """
        while self.websocket is None or not self.websocket.open:
            await asyncio.sleep(0.1)

    async def on_message(self, message: str):
        """
        Handles incoming messages from the server.

        Args:
            message (str): The incoming message.
        """
        if message.startswith("42"):
            message_parsed = json.loads(message[2:])
            if message_parsed[1].get("messageType") == 11 and message_parsed[1]["messageContent"].get("success"):
                if hasattr(self, "on_connected"):
                    self.on_connected()

    async def send_authentication(self, server: str, access_token: str, profile_id: str):
        """
        Sends authentication message to the server.

        Args:
            server (str): The server location (e.g., "US").
            access_token (str): The access token for authentication.
            profile_id (str): The profile ID of the user.
        """
        await self.wait_is_connected()
        auth_message = {
            "messageContent": {
                "country": server.upper(),
                "version": 1,
                "access_token": access_token,
                "applicationId": "APPLICATION_WEB",
                "username": profile_id
            },
            "senderProfileId": None,
            "messageType": 10
        }
        await self.websocket.send('42["10",{}]'.format(json.dumps(auth_message)))

    async def get_web_socket_url(self, server: str) -> str:
        """
        Fetches the WebSocket URL from the server.

        Args:
            server (str): The server location (e.g., "US").

        Returns:
            str: The WebSocket URL.
        """
        url = "https://presence.mspapis.com/getServer"
        if server == "US":
            url = "https://presence-us.mspapis.com/getServer"
        async with self.session.get(url) as response:
            return await response.text()