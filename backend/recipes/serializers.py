import users.serializers as users
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, IngredientsInRecipe, Recipe,
                            ShoppingCart)
from rest_framework import serializers, validators
from tags.models import Tag
from tags.serializers import TagField


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

        validators = (
            validators.UniqueTogetherValidator(
                queryset=IngredientsInRecipe.objects.all(),
                fields=('ingredient', 'recipe')
            ),
        )


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = users.CurrentUserSerializer()
    tags = TagField(
        slug_field='id', queryset=Tag.objects.all(), many=True
    )
    ingredients = IngredientInRecipeSerializer(
        source='ingredient_in_recipe',
        read_only=True, many=True
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'name',
            'author',
            'ingredients',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def in_list(self, obj, model):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return model.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_favorited(self, obj):
        return self.in_list(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self.in_list(obj, ShoppingCart)


class AddRecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = AddIngredientSerializer(many=True)
    image = Base64ImageField(max_length=None)

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'name',
            'ingredients',
            'image',
            'text',
            'cooking_time'
        )

    def to_representation(self, instance):
        serializer = RecipeSerializer(instance)
        return serializer.data

    def create_ingredients(self, ingredients, recipe):
        ingredients_list = []
        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient_id = ingredient['id']
            ingredient_obj = IngredientsInRecipe(
                recipe=recipe, ingredient_id=ingredient_id, amount=amount)
            ingredients_list.append(ingredient_obj)
        IngredientsInRecipe.objects.bulk_create(
            ingredients_list, ignore_conflicts=True)

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe.save()
        self.create_ingredients(ingredients, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        self.create_ingredients(ingredients, instance)
        instance.tags.clear()
        instance.tags.set(tags)
        return super().update(instance, validated_data)

    def validate(self, data):
        ings = data['ingredients']
        if not ings:
            raise serializers.ValidationError(
                'Поле с ингредиентами не может быть пустым'
            )
        unique_ings = set()
        for ingredient in ings:
            name = ingredient['id']
            amount = ingredient['amount']
            if amount <= 0:
                raise serializers.ValidationError(
                    f'Не корректное количество для {name}'
                )
            if not isinstance(amount, int):
                raise serializers.ValidationError(
                    'Количество ингредиентов должно быть целым числом'
                )
            if name in unique_ings:
                raise serializers.ValidationError(
                    'В рецепте не может быть повторяющихся ингредиентов'
                )
            unique_ings.add(name)
        return data

    def validate_cooking_time(self, data):
        if data <= 0:
            raise serializers.ValidationError(
                'Время приготовления не может быть меньше 1 минуты'
            )
        return data


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
