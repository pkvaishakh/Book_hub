from .models import *
from rest_framework import serializers

class DestinationSerializers(serializers.ModelSerializer):
    image=serializers.ImageField(required=False)
    class Meta:
        model=Destination
        fields='__all__'