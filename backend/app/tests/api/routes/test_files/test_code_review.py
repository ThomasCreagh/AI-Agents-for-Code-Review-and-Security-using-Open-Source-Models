# app/tests/api/routes/test_code_review.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import Settings 

# Mock the `auth_headers` function if it's used for authentication
def auth_headers():
    return {"Authorization": f"Bearer {Settings.NEXT_PUBLIC_API_KEY}"}

# Example test function to review code text
def test_review_code_text(client: TestClient):
    # Mock the API key (if necessary) for testing purposes
    Settings.NEXT_PUBLIC_API_KEY = "mock_api_key"

    # Test data (the code you want to review)
    code_data = {
        "code": '"API_KEY = "AIzaSyD3Xz7-EXAMPLEKEY"  # Google API Key',
        "error_description": "test error",
        "language": "python",
    }

    # Send the post request to the code review endpoint
    response = client.post(
        f"{Settings.API_V1_STR}/code-review/text",
        json=code_data,
        headers=auth_headers(),  # Use the headers defined with the API key
    )

    # Assert the status code and expected behavior of the response
    assert response.status_code == 200
