from rest_framework import serializers
from deals.models import Deal


class DealSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ('file',)


class DealBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = ('customer', 'item', 'total', 'quantity', 'date')
