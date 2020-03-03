from django.db import models


# Create your models here.
class TextType(models.Model):
    type = models.CharField(max_length=128, verbose_name='课程种类')

    class Meta:
        db_table = 'course_type'
        verbose_name = '课程种类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type


class TextContext(models.Model):
    type = models.ForeignKey('TextType', verbose_name='课程种类')
    title = models.CharField(max_length=64, verbose_name='课程名')
    content = models.TextField(verbose_name='内容')

    class Meta:
        db_table = 'course_context'
        verbose_name = '课程内容'
        verbose_name_plural = verbose_name