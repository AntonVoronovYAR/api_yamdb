import secrets
import string


def create_confirmation_code():
    """Генерирует код активации и возвращает его. В коде 9 случайных цифр."""
    numbers = string.digits
    confirmation_code = ''.join(secrets.choice(numbers) for i in range(9))
    return confirmation_code
