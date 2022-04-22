from fastapi.testclient import TestClient

# noinspection PyUnresolvedReferences
import main
from utils.patch import MyFastAPI

app = MyFastAPI.get_app()

c = TestClient(app)
