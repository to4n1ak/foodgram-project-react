from django.contrib import admin

from .models import (Favourite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)



class IngredientAmountAdmin(admin.StackedInline):
    model = IngredientAmount
    autocomplete_fields = ('ingredient',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'author', 'cooking_time', 'pub_date', 'in_favorites',)
    list_filter = ('author', 'name', 'pub_date', 'tags',)
    inlines = (IngredientAmountAdmin,)
    empty_value_display = '-нет рецептов-'

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        return '\n '.join([
            f'{item["ingredient__name"]} - {item["amount"]}'
            f' {item["ingredient__measurement_unit"]}.'
            for item in obj.recipe.values(
                'ingredient__name',
                'amount', 'ingredient__measurement_unit')])

    @admin.display(description='В избранном')
    def in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    empty_value_display = '-нет тагов-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    empty_value_display = '-нет корзин-'


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    empty_value_display = '-нет избранного-'


@admin.register(IngredientAmount)
class IngredientInRecipe(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)
    empty_value_display = '-нет такого-'
