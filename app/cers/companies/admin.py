from django.contrib import admin

from cers.companies.models import Company, Department
from cers.core.admin import admin_site


class DepartmentInline(admin.StackedInline):
    model = Department
    extra = 1


class CompanyAdmin(admin.ModelAdmin):
    inlines = (DepartmentInline,)


admin_site.register(Company, CompanyAdmin)
