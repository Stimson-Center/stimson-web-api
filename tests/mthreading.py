# -*- coding: utf-8 -*-
"""
Anything that has to do with threading in this library
must be abstracted in this file. If we decide to do gevent
also, it will deserve its own gevent file.
"""

import logging
import queue
import traceback
from threading import Thread

import scraper
from scraper.configuration import Configuration

__title__ = 'stimson-web-scraper'
__author__ = 'Lucas Ou-Yang'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014, Lucas Ou-Yang'
__maintainer__ = "The Stimson Center"
__maintainer_email = "cooper@pobox.com"

log = logging.getLogger(__name__)


class ConcurrencyException(Exception):
    pass


class Worker(Thread):
    """
    Thread executing tasks from a given tasks queue.
    """

    def __init__(self, tasks, timeout_seconds):
        Thread.__init__(self)
        self.tasks = tasks
        self.timeout = timeout_seconds
        self.daemon = True
        self.start()

    def run(self):
        while True:
            try:
                func, args, kargs = self.tasks.get(timeout=self.timeout)
            except queue.Empty:
                # Extra thread allocated, no job, exit gracefully
                break
            # noinspection PyBroadException,PyUnusedLocal
            try:
                func(*args, **kargs)
            except Exception as ex:
                traceback.print_exc()

            self.tasks.task_done()


class ThreadPool:
    def __init__(self, num_threads, timeout_seconds):
        self.tasks = queue.Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks, timeout_seconds)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()


class NewsPoolException(Exception):
    pass


class NewsPool(object):

    def __init__(self, config=None):
        """
        Abstraction of a threadpool. A newspool can accept any number of
        article objects together in a list. It allocates one
        thread to every Article and then joins.

        We allocate one thread per source to avoid rate limiting.
        5 articles = 5 threads, one per articles.

        >>> from scraper import Article
        >>> from tests.mthreading import NewsPool

        >>> cnn_paper = Article('http://cnn.com')
        >>> tc_paper = Article('http://techcrunch.com')
        >>> espn_paper = Article('http://espn.com')

        >>> papers = [cnn_paper, tc_paper, espn_paper]
        >>> news_pool = NewsPool()
        >>> news_pool.set(papers)
        >>> news_pool.join()

        # All of your papers should have their articles html all populated now.
        >>> cnn_paper.text
        u'<html>blahblah ... '
        """
        self.pool = None
        self.config = config or Configuration()

    def join(self):
        """
        Runs the mtheading and returns when all threads have joined
        resets the task.
        """
        if self.pool is None:
            raise ConcurrencyException('Call set(..) with a list of source objects '
                                       'before calling .join(..)')
        self.pool.wait_completion()
        self.pool = None

    def set(self, news_list, threads_per_source=1, override_threads=None):
        """
        news_list can be a list of `Article`, `Source`, or both.

        If caller wants to decide how many threads to use, they can use
        `override_threads` which takes precedence over all. Otherwise,
        this api infers that if the input is all `Source` objects, to
        allocate one thread per `Source` to not spam the host.

        If both of the above conditions are not true, default to 1 thread.
        """

        if override_threads is not None:
            num_threads = override_threads
        else:
            num_threads = threads_per_source * len(news_list)

        timeout = self.config.thread_timeout_seconds
        self.pool = ThreadPool(num_threads, timeout)

        for news_object in news_list:
            if isinstance(news_object, scraper.Article):
                self.pool.add_task(news_object.build)
            else:
                raise NewsPoolException('Unsupported Class instance type')
