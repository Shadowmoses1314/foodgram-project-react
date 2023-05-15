from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientsInRecipe, Recipe,
                     ShoppingCart)


class IngredientsInRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class IngredientsInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'ingredient',
        'recipe',
        'amount'
    )
    search_fields = ('recipe__name', 'ingredient__name')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    search_fields = ('measurement_unit',)
    list_filter = ('measurement_unit',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientsInRecipeInline,)
    list_display = (
        'pk',
        'name',
        'author'
    )
    search_fields = (
        'name',
        'author__username',
        'author__email'
    )
    readonly_fields = ('is_favorited',)

    def is_favorited(self, instance):
        return instance.favorite_recipes.count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name'
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name'
    )


admin.site.register(
    IngredientsInRecipe,
    IngredientsInRecipeAdmin
)
