# coding: utf-8

from rest_framework import serializers
from rest_framework.fields import FileField
from .models import Entry


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'


class EntryFileSerializer(serializers.Serializer):
    file = FileField(required=True)
