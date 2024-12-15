from django.contrib import admin

from order.models import Order, OrderItem

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderItem)
# @admin.register(Order)
# # cl ass OrderAdmin(admin.ModelAdmin):
# #     l ist_display=[ "user", "product", "quantity", "status", "totalAmount", "created_on", "update_on"]
# #     li st_filter = ["status", "created_on","product"]
    