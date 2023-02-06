from rest_framework import serializers
from .models import Dish


class DishSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dish
        fields = [
            'id',
            'name',
            'description',
            'price',
            'preparation_time',
            'is_vegetarian',
        ]

    @staticmethod
    def validate_preparation_time(value: int) -> int:
        """
        Validation whether the preparation time of the dish has been entered correctly
        """
        if value > 90:
            raise serializers.ValidationError("The preparation time cannot be greater than 90")
        return value
