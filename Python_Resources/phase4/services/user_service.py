from ..models.user import User
from ..utils.formatters import format_greeting


def create_user(name: str, age: int) -> User:
    """Builds and returns a new User object."""
    return User(name=name, age=age)


def greet_user(user: User) -> str:
    """Uses a utility function to format a greeting message for a user."""
    return format_greeting(user.name)
