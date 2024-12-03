import jwt
from django.conf.global_settings import SECRET_KEY
from django.utils import timezone
from rest_framework import serializers

from ..models import Document


class DocumentSerializer(serializers.ModelSerializer):
    is_sharing = serializers.BooleanField(required=False, write_only=True)
    is_editor = serializers.BooleanField(required=False, write_only=True)

    class Meta:
        model = Document
        exclude = ['users']
        extra_kwargs = {
            'title': {'required': True},
            'sharing_token': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data.pop('is_sharing', None)
        validated_data.pop('is_editor', None)
        document = Document.objects.create(**validated_data)
        document.users.add(self.context['request'].user)
        return document

    def update(self, instance, validated_data):
        is_sharing = validated_data.pop('is_sharing', None)
        is_editor = validated_data.pop('is_editor', None)
        if is_sharing is not None and is_editor is not None:
            sharing_token = jwt.encode({
                'file_id': instance.id,
                'is_editor': is_editor,
                'exp': timezone.now() + timezone.timedelta(days=1),
            }, SECRET_KEY, algorithm='HS256')
            instance.sharing_token = sharing_token
        return super().update(instance, validated_data)
