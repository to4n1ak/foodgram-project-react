from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.db.models import UniqueConstraint
from users.models import User


class Ingredient(models.Model):
    """Модель для ингредиентов."""
    name = models.CharField(
        'Ингредиент',
        max_length=100,
        blank=False
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=150,
        blank=False
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient_unit'
            ),)

    def __str__(self) -> str:
        return f'{self.name} {self.measurement_unit}'


class Tag(models.Model):
    """Модель для тэгов."""
    name = models.CharField(
        'Тэг',
        max_length=150,
        unique=True
    )
    color = models.CharField(
        'Цвет тэга',
        max_length=7,
        blank=True,
        null=True,
        default='#00ff7f',
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Введите значение в формате HEX!'
            )
        ]
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=150,
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Модель для рецептов."""
    name = models.CharField(
        'Название рецепта',
        max_length=200,
        blank=False
    )
    text = models.TextField(
        'Описание рецепта'
    )
    image = models.ImageField(
        'Изображение блюда',
        upload_to='recipes/',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингредиенты',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах',
        validators=(
            MinValueValidator(1, message='Не менее 1 минуты'),
            MaxValueValidator(10080, message='Не более 1 недели')
        ),
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:50]


class IngredientAmount(models.Model):
    """Модель для хранения ингредиентов в рецепте."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        'Сколько необходимо ингредиента?',
        validators=(
            MinValueValidator(1, message='Не менее 1 ед.'),
            MaxValueValidator(10000, message='Не более 10 000 ед.')
        ),
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
    
    def __str__(self):
        return f'{self.amount} {self.ingredient}'


class Favourite(models.Model):
    """Модель для избранного."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранный пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранный рецепт',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'user', ], name='is_favorite_already'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(models.Model):
    """Модель для корзины покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепты',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'], name='already_in_cart'
            )
        ]

    def __str__(self):
        return f'{self.user}'
