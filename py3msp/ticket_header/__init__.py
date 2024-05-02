from typing import Any
from threading import Lock
import hashlib
import binascii
import pyamf

class Authorization:
    """
    Class for authorizing requests requiring the TicketHeader attribute.

    This class manages the generation of a TicketHeader attribute for authorization purposes.
    """

    def __init__(self, parent: Any) -> None:
        """
        Initialize the Authorization object.

        Args:
            parent (Any): The parent object containing necessary attributes.
        """
        self.parent: Any = parent
        self.local_bytes: bytes = b''
        self.marking_id: int = 0
        self.lock: Lock = Lock()

    def increment_marking_id(self) -> None:
        """
        Increment the marking ID attribute by 1 in a thread-safe manner.
        """
        with self.lock:
            self.marking_id += 1

    def get_local_bytes(self) -> None:
        """
        Update local_bytes with the current marking ID encoded in UTF-8.
        """
        self.increment_marking_id()
        self.local_bytes = str(self.marking_id).encode('utf-8')

    def calculate_md5(self) -> str:
        """
        Calculate the MD5 hash of the local bytes.

        Returns:
            str: The hexadecimal representation of the MD5 hash.
        """
        return hashlib.md5(self.local_bytes).hexdigest()

    def convert_to_hex(self) -> str:
        """
        Convert the local bytes to a hexadecimal string representation.

        Returns:
            str: The hexadecimal representation of the local bytes.
        """
        return binascii.hexlify(self.local_bytes).decode()

    def generate_ticket_header(self) -> Any:
        """
        Generate the TicketHeader attribute as an ASObject.

        Returns:
            Any: An ASObject containing the TicketHeader and anyAttribute.
        """
        self.get_local_bytes()
        ticket_header_value = self.parent.ticket + self.calculate_md5() + self.convert_to_hex()
        return pyamf.ASObject({"Ticket": ticket_header_value, "anyAttribute": None})