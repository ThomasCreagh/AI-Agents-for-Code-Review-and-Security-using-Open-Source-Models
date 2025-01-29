from fastapi.testclient import TestClient

from app.core.config import settings
from app.models import CodeReviewForm


def test_submit_text(client: TestClient):
    post_data = CodeReviewForm(
        programming_language="python",
        raw_code="import random; print(random.randint(4))",
        error=None
    )

    response = client.post(
        f"{settings.API_V1_STR}/code-review-form",
        content=post_data.model_dump_json()
    )

    assert response.status_code == 200
    assert response.json() == {
        "agents_response": "some response that the ai agents returned"}
