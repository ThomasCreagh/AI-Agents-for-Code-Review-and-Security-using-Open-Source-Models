from fastapi.testclient import TestClient

from app.core.config import settings
from app.models import CodeReviewFormTextBox, CodeReviewForm, TestOuput


def test_submit_file(client: TestClient):
    post_data = CodeReviewForm(
        programming_language="python",
        error=None
    )

    response = client.post(
        f"{settings.API_V1_STR}/code-review-form/text-box",
        content={}
    )

    assert response.status_code == 200
    assert response.json() == TestOuput(
        returned_message="got the text correctly",
        input_value=post_data.model_dump()
    ).model_dump()


def test_submit_text(client: TestClient):
    post_data = CodeReviewFormTextBox(
        programming_language="python",
        raw_code="import random; print(random.randint(4))",
        error=None
    )

    response = client.post(
        f"{settings.API_V1_STR}/code-review-form/file-upload",
        content=post_data.model_dump_json()
    )

    assert response.status_code == 200
    assert response.json() == TestOuput(
        returned_message="got the text correctly",
        input_value=post_data.model_dump()
    ).model_dump()
