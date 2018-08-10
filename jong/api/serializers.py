from jong.models import Rss
from rest_framework import serializers


class RssSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rss
        fields = '__all__'


class FoldersSerializer(serializers.Serializer):

    title = serializers.CharField(required=False, max_length=255)
