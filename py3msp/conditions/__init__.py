from py3msp.exceptions import LoginException

def requires_login(func):
    """
    Decorator to ensure that a user is logged in before executing a method.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The wrapped function.
    """
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to check if the user is logged in before executing the decorated function.

        Args:
            self: The instance of the class.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The result of the decorated function if the user is logged in.

        Raises:
            LoginException: If the user is not logged in.
        """
        if not hasattr(self, 'ticket') or self.ticket is None:
            raise LoginException("User not logged in")
        return func(self, *args, **kwargs)
    return wrapper