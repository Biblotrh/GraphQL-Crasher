from py3msp import AsyncClient
from py3msp.entities import AMFResult

def login_ticket(ticket: str, instance: AsyncClient) -> None:
    """
    Logs in using the provided ticket for authentication.

    This function sets the ticket attribute of the provided instance.

    Args:
        ticket (str): The ticket used for authentication.
        instance (AsyncClient): An instance of the AsyncClient.

    Returns:
        None
    """
    instance.ticket = ticket

