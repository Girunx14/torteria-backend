# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.models import Base
from app.models.user import User, UserRole
from app.utils.security import hash_password

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine_test = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_test
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    existing = db.query(User).filter(User.username == "testadmin").first()
    if not existing:
        admin = User(
            username="testadmin",
            email="testadmin@test.com",
            password_hash=hash_password("test1234"),
            role=UserRole.admin,
            is_active=True,
        )
        db.add(admin)
        db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture(scope="session")
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def admin_token(client):
    response = client.post("/auth/login", data={
        "username": "testadmin",
        "password": "test1234",
    })
    assert response.status_code == 200
    return response.json()["access_token"]


# ← scope="session" para que sea compatible con fixtures de module y session
@pytest.fixture(scope="session")
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}