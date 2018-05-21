import feedparser
from unittest.mock import patch
from jong.core import get_content, get_data


def test_get_content_summary():
    data = {'summary_detail': 'some summary'}
    res = get_content(data)
    print("result ", res)
    assert type(res) is str


def test_get_content_description():
    data = {'description': 'foobar'}
    res = get_content(data)
    print("result ", res)
    assert type(res) is str


def test_set_content_empty():
    data = {'content': ''}
    res = get_content(data)
    print("result ", res)
    assert type(res) is str


def test_get_content():
    content = list()
    content.append({'foobar': 'value'})
    data = {'content': content}
    res = get_content(data)
    assert type(res) is str


def test_get_data():
    url = 'http://planetpython.org/rss20.xml'
    res = get_data(url)
    assert type(res) is feedparser.FeedParserDict or type(res) is str


def test_joplin_run():
    joplin_file = 'foobar.md'
    notebook = 'News'
    kwargs = {'joplin_file': joplin_file, 'notebook': notebook}
    with patch('jong.core') as mock_run:
        mock_run._joplin_run.return_value = True
        mock_run._joplin_run('import', **kwargs)
        mock_run._joplin_run.assert_called_once()


def test_joplin_set_title():
    title = "foo-bar"
    value = "Foo bar"
    kwargs = {'note': title, 'what': 'title', 'value': value}
    with patch('jong.core') as mock_set:
        mock_set._joplin_run.return_value = True
        mock_set._joplin_run('set', **kwargs)
        mock_set._joplin_run.assert_called_once()


def test_joplin_set_author():
    title = "foo-bar"
    value = "foxmask"
    kwargs = {'note': title, 'what': 'author', 'value': value}
    with patch('jong.core') as mock_set:
        mock_set._joplin_run.return_value = True
        mock_set._joplin_run('set', **kwargs)
        mock_set._joplin_run.assert_called_once()


def test_joplin_set_source_url():
    title = "foo-bar"
    value = "http://website.com/to/article/"
    kwargs = {'note': title, 'what': 'source_url', 'value': value}
    with patch('jong.core') as mock_set:
        mock_set._joplin_run.return_value = True
        mock_set._joplin_run('set', **kwargs)
        mock_set._joplin_run.assert_called_once()
