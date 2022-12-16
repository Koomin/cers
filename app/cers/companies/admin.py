from django.contrib import admin

from cers.companies.models import Company, Department


class DepartmentInline(admin.StackedInline):
    model = Department
    extra = 1


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = (DepartmentInline,)
