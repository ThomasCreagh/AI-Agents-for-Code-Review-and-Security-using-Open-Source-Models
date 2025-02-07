from fastapi.testclient import TestClient

from app.core.config import settings


def auth_headers():
    return {"X-API-Key": f"{settings.API_KEY}"}


def test_review_code_text(client: TestClient):
    code_data = {
        "code": "import random;\nprint(random.randint(4))",
        "error_description": "test error",
        "language": "python",
    }

    response = client.post(
        f"{settings.API_V1_STR}/code-review/text",
        json=code_data,
        headers=auth_headers(),
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data["suggestion"]) > 0
    assert data["language"] == code_data["language"]


def test_review_code_file(client: TestClient):
    code_data = {
        "error_description": "test error",
        "language": "python",
    }

    file_content = ""
    with open("app/tests/api/routes/test_files/script.txt", "r") as reader:
        file_content = reader.read()

    file_content_type = "text/plain"
    filename = "test_script.py"

    files = {
        "file": (filename, file_content, file_content_type)
    }

    response = client.post(
        f"{settings.API_V1_STR}/code-review/file",
        data=code_data,
        files=files,
        headers=auth_headers(),
    )

    assert response.status_code == 200
    data = response.json()

    assert data["filename"] == filename
    assert data["language"] == code_data["language"]
    assert len(data["suggestion"]) > 0
