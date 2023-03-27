from cers.companies.models import Company, CompanyConfig, Department
from cers.core.admin import admin_site
from django.contrib import admin


class DepartmentInline(admin.StackedInline):
    model = Department
    extra = 1


class CompanyConfigInline(admin.StackedInline):
    model = CompanyConfig


class CompanyAdmin(admin.ModelAdmin):
    inlines = (
        CompanyConfigInline,
        DepartmentInline,
    )


admin_site.register(Company, CompanyAdmin)
