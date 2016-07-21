from django.db import models


class Gem(models.Model):
    name = models.CharField(verbose_name=u'название', max_length=32, unique=True)
    category = models.ForeignKey('Category')
    image = models.ImageField(upload_to='', blank=True)
    rating = models.PositiveIntegerField(verbose_name='рейтинг', default=0)
    description = models.TextField(verbose_name='описание', blank=True)

    # def __str__(self):
    #     return "Gem {}".format(self.name)


class Category(models.Model):
    name = models.CharField(verbose_name=u'название', max_length=16)
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return self.name
