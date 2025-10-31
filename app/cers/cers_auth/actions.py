
from django.contrib import admin

from cers.companies.models import Company


@admin.action(description="Dodaj wszystkie firmy")
def add_companies(modeladmin, request, queryset):
    companies = Company.objects.all()
    users_count = 0
    for user in queryset:
        if user.groups.name in ["admin", "technician"]:
            user.companies.set(companies)
            users_count += 1

    modeladmin.message_user(request, f"Dodano {companies.count()} firm {users_count} użytkownikom.")
