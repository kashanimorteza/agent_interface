from my_model._declarations import AwaitingGeneration, GenerationMethod
from my_model._models.user import User

RECORDS: tuple[User, ...] = (
    User(
        name="Admin",
        username="admin",
        password=AwaitingGeneration(GenerationMethod.SECURE),
        api_key=AwaitingGeneration(GenerationMethod.SECURE),
    ),
)
