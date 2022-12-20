from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password using passlib.

    Args:
        plain_password (str): Plain password.
        hashed_password (str): Hashed password.

    Returns:
        bool: True if password is valid, False otherwise.
    """
    return pwd_context.verify(
        secret=plain_password,
        hash=hashed_password,
    )


def get_password_hash(password: str) -> str:
    """
    Get password hash using passlib.

    Args:
        password (str): Password.

    Returns:
        str: Password hash.

    """
    return pwd_context.hash(
        secret=password,
    )
