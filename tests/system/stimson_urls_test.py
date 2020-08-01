# -*- coding: utf-8 -*-

import os
from time import time

from scraper import Article, Configuration

from ..mthreading import NewsPool


def article_thread_pool(urls, config):
    articles = [Article(url.replace("\n", ""), config=config) for url in urls]
    news_pool = NewsPool(config=config)
    news_pool.set(articles)
    news_pool.join()
    return articles


def article_curator(client, test_driver_file, config):
    print("\n")
    # set variables
    start_time = time()

    # URLPARSE fails on UTF8 string! https://stackoverflow.com/questions/50499273/urlparse-fails-with-simple-url
    urls = list()
    with open(test_driver_file, 'r', encoding='ascii', errors='ignore') as f:
        for line in f:
            parts = line.split(',')
            config.set_language(parts[0])
            urls.append(parts[1].replace('\n', '').strip())

    # spin up
    articles = article_thread_pool(urls, config)
    bad_titles = [
        "404 not found",
        "404",
        "503 service temporarily unavailable",
        "522/ connection timed out",
        "not found",
        "access denied",
        "server connection terminated",
        "page not found",
        "sorry, the page you were looking for was not found",
        "page not found - the australian-thai chamber of commerce (austcham)"
    ]
    for article in articles:
        if article.text.strip() == '':
            print(f"Error: Empty Article:{article.url}")
        else:
            try:
                response = client.post("/pdf", json=article.get_json())
                assert 200 == response.status_code
                assert '200 OK' == response.status
                assert 'utf-8' == response.charset
                assert response.data
            except Exception as ex:
                print('%r generated an exception: %s' % (article.url, ex))

    total_elapsed_time = time() - start_time
    print(f'Total elapsed time {total_elapsed_time} seconds')


# noinspection PyUnresolvedReferences
@pytest.mark.skip(reason="Running this test updates Google Drive")
def test_industrial_spaces_urls(fixture_directory, client):
    config = Configuration()
    config.follow_meta_refresh = True
    test_driver_file = os.path.join(fixture_directory, "url", "industrial-spaces-urls.csv")
    article_curator(client, test_driver_file, config)


# noinspection PyUnresolvedReferences
@pytest.mark.skip(reason="Running this test updates Google Drive")
def test_illegal_unreported_and_unregulated_fishing_urls(fixture_directory, client):
    config = Configuration()
    config.follow_meta_refresh = True
    config.use_meta_language = False
    config.language = 'en'
    config.http_success_only = False
    test_driver_file = os.path.join(fixture_directory, "url", "illegal-unreported-and-unregulated-fishing-urls.csv")
    article_curator(client, test_driver_file, config)


# noinspection PyUnresolvedReferences
@pytest.mark.skip(reason="Running this test updates Google Drive")
def test_energy_investment_mekong_delta_urls(fixture_directory, client):
    config = Configuration()
    config.follow_meta_refresh = True
    test_driver_file = os.path.join(fixture_directory, "url", "energy-investment-mekong-delta-Thailand-urls.csv")
    article_curator(client, test_driver_file, config)
