from django.contrib import admin
from .models import Location, LocationImage

class LocationAdmin(admin.ModelAdmin):
    # Fields to show in the admin form
    list_display = ('name', 'description', 'price', 'created_by')
    exclude = ('created_by',)  # Hide created_by field from form
    
    def save_model(self, request, obj, form, change):
        # Automatically set the logged-in user as the creator
        if not obj.pk:  # Only for new objects
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

# Register your models with the custom admin class
admin.site.register(Location, LocationAdmin)
admin.site.register(LocationImage)