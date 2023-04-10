import secrets
import string


def create_confirmation_code() -> str:
    """Генерирует код активации и возвращает его. В коде 9 случайных цифр."""
    confirmation_code = (
        ''.join(secrets.choice(string.digits) for _ in range(9))
    )
    return confirmation_code
