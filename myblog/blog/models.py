from django.db import models


# Create your models here.
class Post(models.Model):
    """post info"""
    title = models.CharField('Заголовок поста', max_length=100)
    description = models.TextField('Описание')
    author = models.CharField('Автор', max_length=100)
    date = models.DateField('Дата публикации')
    img = models.ImageField('Изображение', upload_to='image/%Y')

    def __str__(self):
        return f'{self.title}, {self.author}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
