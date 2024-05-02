from pyamf import amf3
from typing import Union, List
from datetime import date, datetime
import hashlib, pyamf
from py3msp.entities import HashSaltPreset

def calculate_checksum(arguments: Union[int, str, bool, bytes, List[Union[int, str, bool, bytes]], dict, date, datetime, pyamf.ASObject, pyamf.TypedObject], hash_set: HashSaltPreset = HashSaltPreset()) -> str:
    """
    Calculate the checksum for the given arguments.

    Args:
        arguments (Union[int, str, bool, bytes, List[Union[int, str, bool, bytes]], dict, date, datetime, amf3.ASObject, amf3.TypedObject]): The arguments to calculate the checksum for.
        hash_set (HashSaltPreset): The hash set containing salt and no ticket value.

    Returns:
        str: The calculated checksum.
    """
    checked_objects = {}
    no_ticket_value = hash_set.no_ticket_value
    salt = hash_set.salt

    def from_object(obj: Union[None, int, str, bool, amf3.ByteArray, datetime.date, datetime, List[Union[int, str, bool, bytes]], dict, pyamf.ASObject, pyamf.TypedObject]) -> str:
        """
        Convert an object to a string representation.

        Args:
            obj (Union[None, int, str, bool, amf3.ByteArray, datetime.date, datetime, List[Union[int, str, bool, bytes]], dict, amf3.ASObject, amf3.TypedObject]): The object to convert.

        Returns:
            str: The string representation of the object.
        """
        if obj is None:
            return ""

        if isinstance(obj, (int, str, bool)):
            return str(obj)

        if isinstance(obj, amf3.ByteArray):
            return from_byte_array(obj)

        if isinstance(obj, (date, datetime)):
            return str(obj.year) + str(obj.month - 1) + str(obj.day)

        if isinstance(obj, (list, dict)) and "Ticket" not in obj:
            return from_array(obj)

        return ""

    def from_byte_array(bytes):
        """
        Convert a ByteArray to a string representation.

        Args:
            bytes: The ByteArray object.

        Returns:
            str: The string representation of the ByteArray.
        """
        if len(bytes) <= 20:
            return bytes.getvalue().hex()

        num = len(bytes) // 20
        array = bytearray(20)
        for i in range(20):
            bytes.seek(num * i)
            array[i] = bytes.read(1)[0]

        return array.hex()

    def from_array(arr):
        """
        Convert an array to a string representation.

        Args:
            arr (list or dict): The array to convert.

        Returns:
            str: The string representation of the array.
        """
        result = ""
        for item in arr:
            if isinstance(item, (pyamf.ASObject, pyamf.TypedObject)):
                result += from_object(item)
            else:
                result += from_object_inner(item)
        return result

    def get_ticket_value(arr):
        """
        Get the ticket value from the array.

        Args:
            arr (list or dict): The array containing objects.

        Returns:
            str: The ticket value or no ticket value if not found.
        """
        for obj in arr:
            if isinstance(obj, pyamf.ASObject) and "Ticket" in obj:
                ticket_str = obj["Ticket"]
                if ',' in ticket_str:
                    ticket_parts = ticket_str.split(',')
                    return ticket_parts[0] + ticket_parts[5][-5:]
        return no_ticket_value

    def from_object_inner(obj):
        """
        Convert an inner object to a string representation.

        Args:
            obj: The object to convert.

        Returns:
            str: The string representation of the object.
        """
        result = ""
        if isinstance(obj, dict):
            for key in sorted(obj.keys()):
                if key not in checked_objects:
                    result += from_object(obj[key])
                    checked_objects[key] = True
        else:
            result += from_object(obj)
        return result

    result_str = from_object_inner(arguments) + salt + get_ticket_value(arguments)
    return hashlib.sha1(result_str.encode()).hexdigest()