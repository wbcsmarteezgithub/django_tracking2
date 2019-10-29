from datetime import timedelta
from django.contrib import admin
from tracking.models import Visitor, Pageview
from tracking.settings import TRACK_PAGEVIEWS


class AdminDisplay(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields] + [field.name for field in
                                                                           self.opts.local_many_to_many]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class VisitorAdmin(AdminDisplay):
    date_hierarchy = 'start_time'

    list_display = ('session_key', 'user', 'start_time', 'session_over',
                    'pretty_time_on_site', 'ip_address', 'user_agent')
    # list_filter = ('user', 'ip_address')
    search_fields = ('session_key', 'user__username', 'ip_address',)

    def session_over(self, obj):
        return obj.session_ended() or obj.session_expired()

    session_over.boolean = True

    def pretty_time_on_site(self, obj):
        if obj.time_on_site is not None:
            return timedelta(seconds=obj.time_on_site)

    pretty_time_on_site.short_description = 'Time on site'


admin.site.register(Visitor, VisitorAdmin)


class PageviewAdmin(admin.ModelAdmin):
    date_hierarchy = 'view_time'

    list_display = ('url', 'view_time')


if TRACK_PAGEVIEWS:
    admin.site.register(Pageview, PageviewAdmin)
