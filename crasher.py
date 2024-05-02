from rich import print as rprint
from rich.prompt import Prompt
from py3msp import AsyncClient
from py3msp.entities import LoginResult
from helpok import query, variables
import os, asyncio, json, aiohttp
from aiohttp import ClientTimeout

async def loop_send_requests(jwt) -> None:
    while True:
        try:
            async with aiohttp.ClientSession(timeout=ClientTimeout(total=2)) as session:
                async with session.post('https://eu.mspapis.com/edgeugc/graphql', headers={'authorization': f'Bearer {jwt}'}, json={'query': query, 'variables': variables}) as response:
                    if response.status == 503 or response.status == 502:
                        rprint("[red] Service is down!")
                    else:
                        rprint('[gray] Loaded 3500 UGCS')
        except:
            pass

async def main() -> None:
    os.system(command="cls")
    moviestarplanet: AsyncClient = AsyncClient(verify_ssl=False, timeout=5)
    logged_in: bool = False
    while not logged_in:
        login: LoginResult = await moviestarplanet.login_async(username="msp_random_username", password="account_password", server="fr", websocket=False)
        logged_in = login.loginStatus.isLoggedIn

    tasks = []
    for _ in range(30):
        tasks.append(loop_send_requests(jwt=moviestarplanet.access_token))
    await asyncio.gather(*tasks)
    await asyncio.sleep(1111)

asyncio.run(main=main())
