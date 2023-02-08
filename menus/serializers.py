from rest_framework import serializers
from django.db import transaction
from dishes.models import Dish
from dishes.serializers import DishSerializer
from .models import Menu


class MenuSerializer(serializers.ModelSerializer):

    dishes = DishSerializer(many=True, required=False)

    class Meta:
        model = Menu
        fields = [
            'id',
            'dishes',
            'name',
            'description',
        ]

    @transaction.atomic
    def create(self, validated_data: dict[str, str]) -> Menu:
        """
        Saving a sent menu to the database. Record made transactional to ensure data correctness.
        Dishes submitted in the menu will be saved to the database
        """
        instance = Menu.objects.create(
            name=validated_data["name"],
            description=validated_data["description"],
        )

        if dishes := validated_data.get('dishes', None) and validated_data['dishes']:
            Dish.objects.bulk_create(self._get_list_of_unsaved_objects(instance, dishes))

        return instance

    @transaction.atomic
    def update(self, instance: Menu, validated_data: dict[str, str]) -> Menu:
        """
        Data update via PUT and PATCH methods
        Dishes sent in the data will be handled as follows:
        - Dishes with data will remove dishes from the menu and insert new dishes
        - Dishes with an empty list will remove the dishes from the menu relationship
        - Data without dishes will not result in any operation.
        Record made transactional to ensure data correctness.
        """
        if 'dishes' in validated_data:
            Dish.objects.filter(menu=instance.id).delete()
            if dishes := validated_data['dishes']:
                Dish.objects.bulk_create(self._get_list_of_unsaved_objects(instance, dishes))

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        instance.save()

        return instance

    @staticmethod
    def _get_list_of_unsaved_objects(instance: Menu, list_of_dishes: list[dict[str, str]]) -> list[Dish]:
        """
        In order to use the bulk create function, open unsaved objects that will be passed to the function
        """
        return [Dish(**item) for item in list_of_dishes if not item.update({"menu": instance})]


class MenuDetailSerializer(serializers.ModelSerializer):

    dishes = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = [
            'id',
            'dishes',
            'name',
            'description',
        ]

    @staticmethod
    def get_dishes(menu_obj: Menu) -> Dish:
        """
        The function returns all serialized data for the entered menu object
        """
        dish = Dish.objects.filter(menu=menu_obj)
        serializer = DishSerializer(dish, many=True)
        return serializer.data
