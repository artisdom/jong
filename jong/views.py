# coding: utf-8
from __future__ import unicode_literals
import arrow
from django.conf import settings
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


class SuccessMixin(object):
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
    paginate_by = 3

    def get_queryset(self):
        return self.queryset.filter().order_by('-date_triggered')


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
