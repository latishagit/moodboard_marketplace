from django.contrib import admin
from .models import Moodboard, User, Category, Purchase, Review, Payment, ContactMessage

admin.site.register(Moodboard)
admin.site.register(User)
admin.site.register(Purchase)
admin.site.register(Review)
admin.site.register(Payment)
admin.site.register(ContactMessage)

#Customizing admin panel's look
admin.site.site_header = "Moodboard Marketplace Admin"
admin.site.site_title = "Moodboard Admin"
admin.site.index_title = "Welcome to the Moodboard Marketplace Admin Panel"

class MyModelAdmin(admin.ModelAdmin):
    class Media:  
        css = {
             'all': ('/css/admin/custom_admin.css',)
        }

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" style="border-radius:5px;" />'
        return "(No Image)"
    
    image_preview.allow_tags = True  # Allow HTML rendering in Django admin
    image_preview.short_description = "Preview"

admin.site.register(Category, CategoryAdmin)
