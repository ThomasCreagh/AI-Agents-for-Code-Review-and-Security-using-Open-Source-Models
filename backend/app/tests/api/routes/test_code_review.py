from fastapi.testclient import TestClient

from app.core.config import settings


def auth_headers():
    return {"Authorization": f"{settings.REACT_APP_API_KEY}"}


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


def test_review_code_file_with_code_and_document(client: TestClient):
    code_data = {
        "error_description": "test error",
        "language": "python",
        "model": "deepseek",
    }

    file_content = ""
    filepath = "app/tests/ai/test_files/example.py"
    with open(filepath, "r") as reader:
        file_content = reader.read()

    file_content_type = "text/plain"
    filename = "test_script.py"
    files = {
        "code_files": (filename, file_content, file_content_type),
        "code_files": (filename, file_content, file_content_type),
        "documentation_files": (filename, file_content, file_content_type),
        "documentation_files": (filename, file_content, file_content_type),
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


def test_review_code_file_with_only_code(client: TestClient):
    code_data = {
        "error_description": "test error",
        "language": "python",
        "model": "deepseek",
    }

    file_content = ""
    filepath = "app/tests/ai/test_files/example.py"
    with open(filepath, "r") as reader:
        file_content = reader.read()

    file_content_type = "text/plain"
    filename = "test_script.py"
    files = {
        "code_files": (filename, file_content, file_content_type),
        "code_files": (filename, file_content, file_content_type),
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


def test_review_code_file_with_no_files(client: TestClient):
    code_data = {
        "error_description": "test error",
        "language": "python",
        "model": "deepseek",
    }
    files = {}

    response = client.post(
        f"{settings.API_V1_STR}/code-review/file",
        data=code_data,
        files=files,
        headers=auth_headers(),
    )

    assert response.status_code == 200
    data = response.json()

    assert data["language"] == code_data["language"]
    assert data["suggestion"] != "[]"
