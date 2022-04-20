from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class StandardLanguage(models.Model):
    name = models.CharField(max_length=127)
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=127)
    active = models.BooleanField(default=True)
    parent_id = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True)
    
    def __str__(self):
        return self.name
    

class MenuItem(models.Model):
    name = models.CharField(max_length=127)
    prefix = models.CharField(max_length=127, null=True, blank=True)
    slug = models.SlugField(max_length=127, allow_unicode=True)
    priority = models.IntegerField(default=99)
    active = models.BooleanField(default=True)
    menu_id = models.ForeignKey(Menu, on_delete=models.RESTRICT, null=True, blank=True)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.link = '/' + ((str(self.prefix) + '/') if self.prefix else '') + str(self.slug)
        res = super().save(force_insert, force_update, using, update_fields)
        return res
    

class SqlReport(models.Model):
    # pass
    name = models.CharField(max_length=31)
    slug = models.SlugField(max_length=31, allow_unicode=True, unique=True)
    query = models.CharField(max_length=4191, null=True)
    tables = models.CharField(max_length=255)
    joins = models.CharField(max_length=1023, null=True)
    columns = models.CharField(max_length=1023)
    where = models.CharField(max_length=1023, null=True)
    group_by = models.CharField(max_length=1023, null=True)
    order_by = models.CharField(max_length=1023, null=True)
    having = models.CharField(max_length=1023, null=True)
    page_size = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.name)
        res = super().save(force_insert, force_update, using, update_fields)
        return res


class RestrictedIp(models.Model):
    ip = models.CharField(max_length=31)

    def __str__(self):
        return self.ip


class RestrictedGateWay(models.Model):
    address = models.CharField(max_length=31)

    def __str__(self):
        return self.address


class TimeZone(models.Model):
    name = models.CharField(max_length=127, unique=True)

    def __str__(self):
        return self.name


class UserTimeZone(models.Model):

    user = models.OneToOneField(User, related_name='time_zone', on_delete=models.CASCADE)
    timezone = models.ForeignKey(TimeZone, default=None, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__()


class SiteSettings(models.Model):
    field_name = models.CharField(max_length=127, unique=True)
    field_value = models.CharField(max_length=1023)


class RomanWord(models.Model):
    name = models.CharField(max_length=255, unique=True)
    improvement = models.CharField(max_length=255)
    lang = models.ForeignKey(StandardLanguage, on_delete=models.RESTRICT)

    def __str__(self):
        res = self.name
        return res
