from fastapi import FastAPI
from dependency_injector import containers, providers

class UserRepository:
    def get_user(self, user_id: int):
        return {"user_id": user_id, "name": "John"}

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: int):
        return self.user_repository.get_user(user_id)

class Container(containers.DeclarativeContainer):
    user_repository = providers.Singleton(UserRepository)
    user_service = providers.Factory(UserService, user_repository=user_repository)

app = FastAPI()
container = Container()
container.user_service.override(providers.Factory(UserService))

@app.get("/users/{user_id}")
def read_user(user_id: int, user_service: UserService = container.user_service):
    return user_service.get_user(user_id)