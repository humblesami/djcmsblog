from django.apps import apps
from django.contrib import admin
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SiteSettings, TimeZone, UserTimeZone, RestrictedIp, RestrictedGateWay, RomanWord, Menu
from .utils import set_session_timezone


class ListAdminMixin(object):
    
    def __init__(self, model, admin_site):
        self.search_fields = []
        self.list_display = [field.name for field in model._meta.fields]
        super().__init__(model, admin_site)


app_models = apps.get_app_config('website').get_models()
for model in app_models:
    admin_models = [
        '<class \'website.models.DbQuery\'>',
    ]
    if str(model) not in admin_models:
        continue
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        ar_search = []
        for field_obj in model._meta.concrete_fields:
            if field_obj.column != 'id':
                ar_search.append(field_obj.column)
        admin_class.search_fields = ar_search
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass


class UserTimeZoneAdmin(admin.ModelAdmin):
    list_display = ['user', 'timezone']
    autocomplete_fields = ['timezone']


class RomanWordAdmin(admin.ModelAdmin):
    list_display = ['name', 'improvement']


class TimeZoneAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        first = TimeZone.objects.first()
        UserTimeZone.objects.create(user=instance, timezone=first)


post_save.connect(create_user_profile, sender=User)


@receiver(user_logged_in)
def assign_user_timezone(request, user, **kwargs):
    tz_name = 'GMT'
    try:
        user_tz = user.time_zone
        timezone = user_tz.timezone
        tz_name = timezone.name
    except:
        a = 1
    set_session_timezone(request.session, tz_name)


class SettingAdmin(admin.ModelAdmin):
    list_display = ['field_name', 'field_value']


class RestrictedIpAdmin(admin.ModelAdmin):
    list_display = ['ip']


class RestrictedGateWayAdmin(admin.ModelAdmin):
    list_display = ['address']


class MenuAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    list_display = ['name', 'link']
    

admin.site.register(SiteSettings, SettingAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(RomanWord, RomanWordAdmin)
admin.site.register(TimeZone, TimeZoneAdmin)
admin.site.register(UserTimeZone, UserTimeZoneAdmin)
admin.site.register(RestrictedIp, RestrictedIpAdmin)
admin.site.register(RestrictedGateWay, RestrictedGateWayAdmin)
