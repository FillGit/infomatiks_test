from .conftest import client
from hamcrest import assert_that, is_
from operations.models import Operation


def test_v1_metadata_video_fragments(session):
    result = Operation(name='tttt',
                       flight_number='17a',
                       coordinatex='85.1',
                       coordinatey='56.1',
                       out_n='out1',
                       coordinates_time='2022-01-01 06:06:08',
                       out_time='2022-01-01 06:06:01',
                       name_time='tttt_01:01:01'
                       )
    session.add(result)
    session.commit()
    response = client.get(
        "/v1/metadata_video_fragments/tttt"
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert_that(data, is_([{'id': 1,
                            'name': 'tttt',
                            'flight_number': '17a',
                            'coordinatex': '85.1',
                            'coordinatey': '56.1',
                            'out_n': 'out1',
                            'coordinates_time': '2022-01-01 06:06:08',
                            'out_time': '2022-01-01 06:06:01',
                            'name_time': 'tttt_01:01:01'}]))


def test_v1_video():
    rtsp_url = "rtsp://"
    with open('rtsp_url.txt', 'w+', encoding='utf-8') as f:
        f.truncate(0)
        f.write(rtsp_url)
    response = client.get("/v1/video")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


def test_v1_emulation_server():
    response = client.get(
        "/v1/emulation_server"
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []
