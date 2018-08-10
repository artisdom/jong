from django.conf.urls import url, include

from jong.api.views import RssViewSet, FoldersAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'rss', RssViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^folders/$', FoldersAPIView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
