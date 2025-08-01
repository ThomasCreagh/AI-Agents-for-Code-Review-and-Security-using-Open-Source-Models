from fastapi.testclient import TestClient

from app.core.config import settings


def auth_headers():

    return {"Authorization": f"{settings.NEXT_PUBLIC_API_KEY}"}


def test_review_code_text(client: TestClient):
    code_data = {
        "code": '"API_KEY = "AIzaSyD3Xz7-EXAMPLEKEY"  # Google API Key',
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

    assert data["suggestion"] != "[]"
    assert data["language"] == code_data["language"]


def test_review_code_file(client: TestClient):
    code_data = {
        "error_description": "test error",
        "language": "python",
    }

    file_content = ""
    with open("app/tests/ai/test_files/example.py", "r") as reader:
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
    assert data["suggestion"] != "[]"
