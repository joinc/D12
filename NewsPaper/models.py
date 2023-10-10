from django.db import models
from django.contrib.auth.models import User

######################################################################################################################


STATUS_CHOICES = (
    (0, 'Статья',),
    (1, 'Новость',)
)


######################################################################################################################

class Author(models.Model):
    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
    )
    rating = models.SmallIntegerField(
        verbose_name='Рейтинг пользователя',
        default=0,
    )

    def update_rating(self):
        self.rating = 3 * sum(
            Post.objects.filter(author=self).values_list('rating', flat=True)
        )
        self.rating = self.rating + sum(
            Comment.objects.filter(user=self.user).values_list('rating', flat=True)
        )
        self.rating = self.rating + sum(
            Comment.objects.filter(post__in=Post.objects.filter(author=self)).values_list('rating', flat=True)
        )
        self.save(update_fields=['rating', ])

    def __str__(self):
        return f'{self.user.get_full_name()}'

    class Meta:
        ordering = 'user',
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        managed = True


######################################################################################################################


class Category(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    name = models.CharField(
        verbose_name='Название категории',
        max_length=124,
        unique=True,
    )
    subscribers = models.ManyToManyField(
        User,
        blank=True
    )

    def get_count(self):
        return f'{Post.objects.filter(category=self).count()}'

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = 'name',
        verbose_name = 'Категория записи'
        verbose_name_plural = 'Категории записей'
        managed = True


######################################################################################################################


class Post(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    author = models.ForeignKey(
        Author,
        verbose_name='Автор записи',
        null=True,
        related_name='Author',
        on_delete=models.SET_NULL,
    )
    type_post = models.SmallIntegerField(
        verbose_name='Тип записи',
        choices=STATUS_CHOICES,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория записи',
        null=True,
        related_name='Category',
        on_delete=models.SET_NULL,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания записи',
        auto_now_add=True,
        null=True,
    )
    title = models.CharField(
        verbose_name='Заголовок записи',
        max_length=1024,
        default='',
    )
    text = models.TextField(
        verbose_name='Текст записи',
        default='',
    )
    rating = models.SmallIntegerField(
        verbose_name='Рейтинг записи',
        default=0,
    )

    def like(self):
        """
        Увеличивает рейтинг на единицу
        :return: None
        """
        self.rating = self.rating + 1
        self.save(update_fields=['rating', ])

    def dislike(self):
        """
        Уменьшает рейтинг на единицу
        :return: None
        """
        self.rating = self.rating - 1
        self.save(update_fields=['rating', ])

    def preview(self):
        """
        Возвращает начало статьи (предварительный просмотр) длиной 124 символа
        :return:
        """
        return f'{self.text[:124]}...'

    def __str__(self):
        return f'[{self.rating}] {self.title}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        ordering = '-create_date', 'title',
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        managed = True


######################################################################################################################


class Comment(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    post = models.ForeignKey(
        Post,
        verbose_name='Комментируемая запись',
        null=True,
        related_name='CommentPost',
        on_delete=models.SET_NULL,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        null=True,
        related_name='CommentUser',
        on_delete=models.SET_NULL,
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        default='',
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания комментария',
        auto_now_add=True,
        null=True,
    )
    rating = models.SmallIntegerField(
        verbose_name='Рейтинг комментария',
        default=0,
    )

    def like(self):
        """
        Увеличивает рейтинг на единицу
        :return: None
        """
        self.rating = self.rating + 1
        self.save(update_fields=['rating', ])

    def dislike(self):
        """
        Уменьшает рейтинг на единицу
        :return: None
        """
        self.rating = self.rating - 1
        self.save(update_fields=['rating', ])

    def __str__(self):
        return f'[{self.rating}] {self.user} - {self.text[:60]}...'

    class Meta:
        ordering = 'rating', 'user',
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        managed = True


######################################################################################################################
