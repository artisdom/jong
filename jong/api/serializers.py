from jong.models import Rss
from rest_framework import serializers


class RssSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rss
        fields = '__all__'


