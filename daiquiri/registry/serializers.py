from rest_framework import serializers

from daiquiri.core.serializers import JSONListField, JSONDictField


class DublincoreSerializer(serializers.Serializer):

    identifier = serializers.ReadOnlyField()
    title = serializers.ReadOnlyField()
    description = serializers.SerializerMethodField()
    publisher = serializers.SerializerMethodField()
    subjects = serializers.ReadOnlyField()

    def get_description(self, obj):
        return obj['content']['description']

    def get_publisher(self, obj):
        return obj['curation']['publisher']


class VoresourceSerializer(serializers.Serializer):

    identifier = serializers.ReadOnlyField()
    title = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()
    updated = serializers.ReadOnlyField()
    voresource_status = serializers.ReadOnlyField(default='active')

    curation = JSONDictField(default={})
    content = JSONDictField(default={})
    capabilities = JSONListField(default=[])
    tableset = JSONListField(default=[])

    managed_authority = serializers.ReadOnlyField(default=None)
    managing_org = serializers.ReadOnlyField(default=None)
    type = serializers.ReadOnlyField()
