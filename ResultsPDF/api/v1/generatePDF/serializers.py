from rest_framework import serializers


class LinksListSerializer(serializers.ListSerializer):
    child = serializers.URLField()
    allow_empty = False