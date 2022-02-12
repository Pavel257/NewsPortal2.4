from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.authorUser.username

    # def __int__(self):
    #     return self.ratingAuthor

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()
    #

    def __str__(self):
        return f'{self.authorUser}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, )

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Авторы")

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новости'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE, verbose_name="Категория")
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name="Время создания новости")
    postCategory = models.ManyToManyField(Category, through='PostCategory', verbose_name="Название категории")
    title = models.CharField(max_length=128, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    rating = models.SmallIntegerField(default=0)
    #
    def __str__(self):
        return f'{self.title}'

    # def __int__(self):
    #     self.rating

    #
    # def __str__(self):
    #     return 'Заголовок: {}, Пользователь: {}, Рейтинг: {}, Категория: {} * '.format(self.title, self.author,
    #                                                                             self.rating, self.postCategory.all(), self.save())


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'
        # return '{} ... {}'.format(self.text[0:123], str(self.rating), str(self.postCategory)) #когда много данных, чтобы не жрало память.

    def get_absolute_url(self):
        return f'/news/{self.id}'



class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.postThrough.postCategory.name, self.pk


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата написания')
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг комментария')

    def __str__(self):
        return self.commentPost.author.authorUser.username + ':  Рейтинг = ' + str(self.pk)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # def __str__(self):
    #     return 'Пользователь: {} Текст: {} Рейтинг: {} * '.format(self.commentUser, self.text,
    #                                                               self.rating)
    # #
    # class Meta:
    #     verbose_name = 'Комментарий'
    #     verbose_name_plural = 'Комментарии'

    # def __str__(self):
    #     return '{} ... {}'.format(self.text[0:123], str(self.rating))

    # def __int__(self):
    #     return f'{self.dateCreation()}'


