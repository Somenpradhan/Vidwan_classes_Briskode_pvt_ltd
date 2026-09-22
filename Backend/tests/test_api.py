import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # Create test admin
    test_admin = User(
        email="testadmin@vidwanclasses.com",
        hashed_password=get_password_hash("TestPassword123"),
        full_name="Test Admin",
        is_admin=True,
        is_active=True
    )
    db.add(test_admin)
    db.commit()
    yield
    Base.metadata.drop_all(bind=engine)


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "Vidwan Classes API"


def test_admin_login():
    response = client.post(
        "/api/v1/auth/login/json",
        json={"username": "testadmin@vidwanclasses.com", "password": "TestPassword123"}
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data


def test_contact_form_submission():
    payload = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "9876543210",
        "subject": "Inquiry about Nurture Batch",
        "message": "I would like to enroll in JEE 2026 course.",
        "course": "Nurture Program"
    }
    response = client.post("/api/v1/contact", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Jane Doe"
    assert data["status"] == "new"


def test_vst_registration():
    payload = {
        "student_name": "Rohan Kumar",
        "parent_name": "Suresh Kumar",
        "email": "rohan.kumar@example.com",
        "phone": "9123456789",
        "class_name": "Class 10th",
        "school": "DAV Public School",
        "city": "Bhubaneswar",
        "preferred_center": "Main Campus",
        "exam_type": "JEE Target"
    }
    response = client.post("/api/v1/vst/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["student_name"] == "Rohan Kumar"


def test_newsletter_subscription():
    payload = {"email": "subscriber@example.com"}
    response = client.post("/api/v1/newsletter/subscribe", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "subscriber@example.com"
