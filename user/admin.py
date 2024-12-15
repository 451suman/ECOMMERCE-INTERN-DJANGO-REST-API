from django.contrib import admin

from user.models import Customer

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [ "user", "phone", "address","created_on", "update_on"]
    search_fields = ["phone"]
    list_filter=["created_on"]
