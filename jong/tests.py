# coding: utf-8
from django.test import TestCase
import feedparser
from unittest.mock import patch
from jong.core import Core


class MainTest(TestCase):
    """

    """
    def setUp(self):
        self.c = Core()

    def test_get_content_summary(self):
        data = {'summary_detail': 'some summary'}
        res = self.c.get_content(data)
        assert type(res) is str

    def test_get_content_description(self):
        data = {'description': 'foobar'}
        res = self.c.get_content(data)
        assert type(res) is str

    def test_set_content_empty(self):
        data = {'content': ''}
        res = self.c.get_content(data)
        assert type(res) is str

    def test_get_content(self):
        content = list()
        content.append({'foobar': 'value'})
        data = {'content': content}
        res = self.c.get_content(data)
        assert type(res) is str

    def test_get_data(self):
        url = 'http://planetpython.org/rss20.xml'
        res = self.c.get_data(url)
        assert type(res) is feedparser.FeedParserDict or type(res) is str

    def test_joplin_create_note(self):
        entry = {'title': 'My Title', 'link': 'http://www.foobar.net', 'content': '<h1>Heading</h1><br>Content'}
        rss = {'name': 'FoxMaSk'}
        with patch('jong.core') as mock_set:
            mock_set.create_note.return_value = True
            mock_set.create_note(entry, rss)
            mock_set.create_note.assert_called_once()
