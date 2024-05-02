import aiohttp, atexit, asyncio
from py3msp.entities import MSP2ItemTemplate
from py3msp.construct import close_session

class NebulaAsyncClient:
    """
    Asynchronous client for interacting with the Nebula API.

    Args:
        parent (AsyncClient): The parent AsyncClient instance.
    """

    def __init__(self, parent) -> None:
        """
        Initializes the NebulaAsyncClient.

        Args:
            parent (AsyncClient): The parent AsyncClient instance.
        """
        self._parent = parent
        self.headers = {'Authorization': f'Bearer {self._parent.access_token}'}
        atexit.register(self.close_session)

    def close_session(self):
        """
        Close the aiohttp session when the program exits.
        """
        if getattr(self, '_session', None) is not None:
            asyncio.run(close_session(self._parent._session))


    async def get_item_from_item_templates(self, objId: int) -> MSP2ItemTemplate:
        """
        Retrieves an MSP2ItemTemplate object from the API.

        Args:
            objId (int): Object ID.

        Returns:
            MSP2ItemTemplate: MSP2ItemTemplate object.
        """
        url = f"https://eu.mspapis.com/curatedcontentitemtemplates/v2/item-templates/{objId}"
        async with self._parent._session.get(url, headers=self.headers) as response:
            try:
                data = await response.json()
                item_template_data = {key: data.get(key) for key in MSP2ItemTemplate.__init__.__code__.co_varnames if key in data}
                return MSP2ItemTemplate(**item_template_data)
            except Exception as e:
                return MSP2ItemTemplate()
            
    async def send_comment_async(self, entity_id: str, text: str) -> bool:
        """
        Sends a comment asynchronously to the specified entity.

        Args:
            entity_id (str): The ID of the entity to which the comment is being posted.
            text (str): The text content of the comment.

        Returns:
            bool: True if the comment is successfully sent, False otherwise.
        """
        json_data = {
            'query': 'mutation SendComment($entityType: EntityType!, $threadId: ID!, $text: String!, $author: ID!){\r\n\t\t\t\t\tpostComment(input: {entityType: $entityType, threadId: $threadId, text: $text, author: $author })\r\n\t\t\t\t\t{\r\n\t\t\t\t\t\tsuccess\r\n\t\t\t\t\t\terror\r\n\t\t\t\t\t\tcomment\r\n\t\t\t\t\t\t{\r\n                          commentId \r\n                          created\r\n                          author\r\n                          text\r\n\t\t\t\t\t}}}',
            'variables': '{"entityType":"UGC","threadId":"'+str(entity_id)+'","text":"'+text+'","author":"'+self._parent.profileId+'"}',
        }
        async with self._parent._session.post("https://eu.mspapis.com/edgecomments/graphql/graphql", json=json_data, headers=self.headers) as response:
            return "commentId" in await response.text()
        
    