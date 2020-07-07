from django.db import models


class Deal(models.Model):
    """
       customer - логин покупателя
       item - наименование товара
       total - сумма сделки
       quantity - количество товара, шт
       date - дата и время регистрации сделки
    """
    customer = models.CharField(verbose_name='Customer',max_length=64, db_index=True)
    item = models.CharField(verbose_name='Item', max_length=64, db_index=True)
    total = models.IntegerField(verbose_name='Total')
    quantity = models.IntegerField(verbose_name='Quantity')
    date = models.DateTimeField(verbose_name='Date')


class UploadFile(models.Model):
    """
       file - csv файл который мы загружаем к себе на сервер
    """
    file = models.FileField(upload_to="csv_files/", max_length=150, blank=True)