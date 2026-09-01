import os
from urllib.parse import quote_plus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from connection import get_db
from models.base import Base
from models import models

from controller import app
from security.auth import tokenizer

user = os.getenv("DB_USER")
password = quote_plus(os.getenv("DB_PASSWORD"))
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

url = f"postgresql://{user}:{password}@{host}:{port}/igreja_teste"

engine = create_engine(url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


client = TestClient(app)

@pytest.fixture
def setup_db():
    Base.metadata.create_all(bind=engine)

@pytest.fixture
def teardown_db():
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def active_user(db):
    user_admin = models.User(
        nome="admin",
        email="admin@admin.com",
        senha="senha123",
        status="aceito"
    )
    db.add(user_admin)
    db.commit()
    db.refresh(user_admin)

    return user_admin

@pytest.fixture
def token_admin(active_user: models.User):
    token = tokenizer(active_user.nome, active_user.email)
    return token

@pytest.fixture
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client_test(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    app.dependency_overrides.clear()