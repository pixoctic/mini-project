from django.contrib import admin
from .models import ServiceRequest

# This decorator registers the model and applies our custom layout
@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    # 1. The columns that will appear in the main admin table
    list_display = ('tracking_id', 'customer', 'device_brand', 'device_model', 'status', 'created_at')
    
    # 2. Adds a filter sidebar on the right to quickly sort by status or date
    list_filter = ('status', 'device_brand', 'created_at')
    
    # 3. Adds a search bar at the top to find specific tickets instantly
    search_fields = ('tracking_id', 'imei_number', 'customer__username')
    
    # 4. Protects the auto-generated fields so staff can't accidentally overwrite them
    readonly_fields = ('tracking_id', 'created_at')
    
    # 5. Organizes the detail view when a staff member clicks on a specific ticket
    fieldsets = (
        ('Customer & Device Info', {
            'fields': ('customer', 'device_brand', 'device_model', 'imei_number')
        }),
        ('Repair Details', {
            'fields': ('issue_description', 'status')
        }),
        ('System Tracking', {
            'fields': ('tracking_id', 'created_at')
        }),
    )
