# -*- coding: utf-8 -*-

import json

import pytest
from scraper.article import NLPED


def validate(response):
    assert 200 == response.status_code
    assert '200 OK' == response.status
    assert 'utf-8' == response.charset
    data = json.loads(response.data)
    return data


@pytest.mark.options(debug=True)
def test_article_th_pdf(client):
    response1 = client.get("/article?url=http://tpch-th.listedcompany.com/misc/ShareholderMTG/egm201701/20170914-tpch-egm201701-enc02-th.pdf&language=th")
    response1_data = validate(response1)
    assert len(response1_data) == 15  # returned 15 results on 2020/07/13!
    payload = response1_data
    while NLPED not in payload['workflow']:
        response2 = client.post("/article", json=payload)
        response2_data = validate(response2)
        assert len(response2_data) == 15  # returned 15 results on 2020/07/13!
        payload = response2_data
    assert len(payload['text'])
    response3 = client.post("/article/translate", json=payload)
    response3_data = validate(response3)
    assert len(response3_data['title'])
    assert len(response3_data['summary'])
    assert len(response3_data['text'])



