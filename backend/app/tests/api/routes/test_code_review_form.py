from fastapi.testclient import TestClient

from app.core.config import settings
from app.models import CodeReviewFormTextBox, CodeReviewForm, TestOuput


def test_submit_text(client: TestClient):
    post_data = CodeReviewFormTextBox(
        programming_language="python",
        raw_code="import random; print(random.randint(4))",
        error=None
    )

    response = client.post(
        f"{settings.API_V1_STR}/code-review-form/text-box",
        json=post_data.model_dump(),
    )

    assert response.status_code == 200
    assert response.json() == TestOuput(
        returned_message="got the text correctly",
        input_value=post_data.model_dump()
    ).model_dump()


def test_submit_file(client: TestClient):
    post_data = {
        "programming_language": "python",
        "error": "None",
    }

    file_content = ""
    with open("app/tests/api/routes/test_files/script.txt", "r") as reader:
        file_content = reader.read()

    # file_content = b"print('Hello, World!')"
    file_content_type = "text/plain"
    filename = "test_script.py"

    fileoutput = {
        "filename": filename,
        "content_type": file_content_type,
    }

    files = {
        "file": (filename, file_content, file_content_type)
    }

    response = client.post(
        f"{settings.API_V1_STR}/code-review-form/file-upload",
        data=post_data,
        files=files,
    )

    assert response.status_code == 200
    assert response.json() == TestOuput(
        returned_message="got the file correctly",
        input_value=post_data | fileoutput
    ).model_dump()

    # input_value={
    #     "programming_language": programming_language,
    #     "error": error,
    #     "filename": file.filename,
    #     "content_type": file.content_type
    # }
