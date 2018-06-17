# coding: utf-8
from datetime import datetime
from django.conf import settings
from django.test import TestCase, RequestFactory
import feedparser
from unittest.mock import patch
from jong.core import Core
from jong.forms import RssForm
from jong.models import Rss
from jong.views import RssListView, RssCreateView, RssUpdateView, RssDeleteView, rss_switch_status


class SettingsTest(TestCase):
    """
        settings
    """

    def test_settings(self):
        self.assertTrue(settings.JOPLIN_WEBCLIPPER)
        self.assertTrue(settings.JOPLIN_WEBCLIPPER > 0)


class RssModelTest(TestCase):
    """
        Model
    """
    def setUp(self):
        name = 'My Rss'
        url = 'https://foxmask.net/feeds/all.rss.xml'
        status = True
        notebook = 'News'
        tag = 'Foobar'
        self.r = Rss.objects.create(url=url,
                                    name=name,
                                    status=status,
                                    notebook=notebook,
                                    tag=tag)

    def test_rss(self):
        # r = self.create_rss()
        self.assertTrue(isinstance(self.r, Rss))
        self.assertEqual(
            self.r.show(),
            "RSS %s %s" % (self.r.name, self.r.status)
        )
        self.assertEqual(self.r.__str__(), self.r.name)


class CoreTest(TestCase):
    """
        Core
    """
    def setUp(self):
        self.c = Core()
        name = 'My Rss'
        url = 'https://foxmask.net/feeds/all.rss.xml'
        status = True
        notebook = 'News'
        tag = 'Foobar'
        self.r = Rss.objects.create(url=url,
                                    name=name,
                                    status=status,
                                    notebook=notebook,
                                    tag=tag)

    def test_update_date(self):
        self.c._update_date(self.r.id)

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


class RssFormTest(TestCase):
    """
        Form
    """
    def test_valid_form(self):
        name = 'Sam et max'
        url = 'http://sametmax.com/feed/'
        status = True
        notebook = 'News'
        tag = 'Foobar'
        data = {'name': name,
                'url': url,
                'notebook': notebook,
                'tag': tag,
                'status': status,
                }
        form = RssForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = RssForm(data={})
        self.assertFalse(form.is_valid())


class RssListViewTestCase(TestCase):
    """
        Views
    """

    def setUp(self):
        super(RssListViewTestCase, self).setUp()
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_get(self):
        template = "base.html"
        # Setup request and view.
        request = RequestFactory().get('/')
        view = RssListView.as_view(template_name=template)
        # Run.
        response = view(request)
        # Check.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "base.html")


class RssCreateViewTestCase(TestCase):
    """
        Views
    """

    def test_get(self):
        template_name = "jong/rss_create.html"
        # Setup request and view.
        request = RequestFactory().get('add/')
        view = RssCreateView.as_view(template_name=template_name)
        # Run.
        response = view(request)
        # Check.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], template_name)


class RssUpdateViewTestCase(RssModelTest):
    """
        Views
    """

    def test_get(self):
        template_name = "jong/rss_update.html"
        # Setup request and view.
        request = RequestFactory().get('edit/')
        view = RssUpdateView.as_view(template_name=template_name)
        # Run.
        response = view(request, pk=self.r.id)
        # Check.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], template_name)


class RssDeleteViewTestCase(RssModelTest):
    """
        Views
    """

    def test_get(self):
        template_name = "jong/rss_confim_delete.html"
        # Setup request and view.
        request = RequestFactory().get('delete/')
        view = RssDeleteView.as_view(template_name=template_name)
        # Run.
        response = view(request, pk=self.r.id)
        # Check.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], template_name)


class ViewFunction(RssModelTest):
    """
        Views
    """

    def test_rss_switch_status(self):
        request = RequestFactory().get('switch/')

        response = rss_switch_status(request, self.r.id)
        self.assertEqual(response.status_code, 302)

        response = rss_switch_status(request, self.r.id)
        self.assertEqual(response.status_code, 302)
