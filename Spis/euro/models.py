# -*- coding: utf-8 -*-

from django.db import models


class Category(models.Model):
    name = models.CharField('Nazwa Kategorii', max_length=100)
    slug = models.SlugField('Odnośnik', unique=True, max_length=100)
    icon = models.ImageField('Ikonka Kategorii', upload_to='icons',
                              blank=True)

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __unicode__(self):
        return self.name


class EuroAuchanNames(models.Model):

    euro_name = models.CharField('Nazwa Euro: ', max_length=100)
    auchan_name = models.CharField('Nazwa Auchan: ', max_length=100)
    pol_num = models.CharField('Numer POL: ', max_length=10, default='POL0000000')

    class Meta:
        verbose_name = 'Nazwa produktu'
        verbose_name_plural = 'Nazwy produktów'

    def __str__(self):
        return self.euro_name + self.auchan_name