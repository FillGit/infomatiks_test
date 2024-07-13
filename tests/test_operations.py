from .conftest import client


def test_create_user():
    response = client.get(
        "/v1/metadata_video_fragments/qwe"
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []
