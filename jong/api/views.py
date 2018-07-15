from jong.api.serializers import RssSerializer
from jong.api.permissions import DjangoModelPermissions
from jong.models import Rss

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination


class RssResultsSetPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 50


class RssViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`, `update`
    and `destroy` actions.
    """
    queryset = Rss.objects.all()
    serializer_class = RssSerializer
    pagination_class = RssResultsSetPagination
    # filter the notes
    permission_classes = (DjangoModelPermissions, )

