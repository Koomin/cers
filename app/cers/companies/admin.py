from cers.companies.models import Company, Department
from cers.core.admin import admin_site
from django.contrib import admin


class DepartmentInline(admin.StackedInline):
    model = Department
    extra = 1


class CompanyAdmin(admin.ModelAdmin):
    inlines = (DepartmentInline,)


admin_site.register(Company, CompanyAdmin)
