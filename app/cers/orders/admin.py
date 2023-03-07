from django.contrib import admin

from cers.core.admin import CersModelAdmin, admin_site
from cers.orders.models import Order, Comment, Supplier


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class OrderAdmin(CersModelAdmin):
    context_field = 'company'
    list_display = ['name', 'status', 'selling_price_gross', 'supplier', 'company', 'created']
    inlines = (CommentInline,)
    fields = ('name', 'status', 'selling_price_gross', 'supplier')


admin_site.register(Order, OrderAdmin)
admin_site.register(Supplier, CersModelAdmin)
