from phase4.models.user import User
from phase4.services.user_service import create_user, greet_user


def main():
    user = create_user(name="Minal", age=25)
    print(f"Created: {user}")

    message = greet_user(user)
    print(message)


if __name__ == "__main__":
    main()