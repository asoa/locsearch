from django.contrib import admin

from .models import Consultant


class ConsultantAdmin(admin.ModelAdmin):
    list_display = ('id','name','trainee', 'r_certified','ambassador','distributor','trichology', 'approved')
    list_display_links = ('id',)
    list_editable = ('trainee', 'r_certified','ambassador','distributor','trichology', 'approved')
    search_fields = ('name','city')
    list_per_page = 25


admin.site.register(Consultant, ConsultantAdmin)

