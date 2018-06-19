# coding: utf-8
from __future__ import unicode_literals
import arrow
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView, ListView, DeleteView, CreateView

# trigger_happy
from jong.forms import RssForm
from jong.models import Rss


import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


def rss_switch_status(request, pk):
    rss = get_object_or_404(Rss, pk=pk)
    if rss.status:
        rss.status = False
    else:
        rss.status = True
        # set the trigger to the current date when the
        # the trigger is back online
        rss.date_triggered = arrow.utcnow().to(settings.TIME_ZONE).format('YYYY-MM-DD HH:mm:ssZZ')
    rss.save()

    return HttpResponseRedirect(reverse('base'))


def page_it(data, record_per_page, page=''):
    """
        return the data of the current page
    """
    paginator = Paginator(data, record_per_page)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999),
        # deliver last page of results.
        data = paginator.page(paginator.num_pages)

    return data


class PaginateMixin:
    """
        Mixin to just handle the Paginate behavior
    """
    def get_context_data(self, **kw):
        data = self.model.objects.all()
        # paginator vars
        record_per_page = 3
        page = self.request.GET.get('page')
        # paginator call
        data = page_it(data, record_per_page, page)
        context = super(PaginateMixin, self).get_context_data(**kw)
        context['data'] = data
        return context


class SuccessMixin:
    """
        Mixin to just return to the expected page
        where the name is based on the model name
    """
    def get_success_url(self):
        return reverse('base')


class RssMixin(SuccessMixin):
    form_class = RssForm
    model = Rss


class RssListView(ListView):
    """
        list of Rss
    """
    context_object_name = "rss_list"
    queryset = Rss.objects.all()

    def get_queryset(self):
        return self.queryset.filter().order_by('-date_triggered')

    def get_context_data(self, **kw):
        data = self.queryset.filter().order_by('-date_triggered')
        # paginator vars
        record_per_page = 10
        page = self.request.GET.get('page')
        # paginator call
        paginator = Paginator(data, record_per_page)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            data = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            data = paginator.page(paginator.num_pages)

        context = super(RssListView, self).get_context_data(**kw)
        context['data'] = data
        return context


class RssCreateView(RssMixin, CreateView):
    """
        list of Rss
    """
    template_name = 'jong/rss_create.html'


class RssUpdateView(RssMixin, UpdateView):
    """
        Form to update description
    """
    template_name = 'jong/rss_update.html'


class RssEditedTemplateView(TemplateView):
    """
        just a simple form to say thanks :P
    """


class RssDeleteView(RssMixin, DeleteView):
    """
        page to delete a trigger
    """


class RssDeletedTemplateView(TemplateView):
    """
        just a simple form to say thanks :P
    """
