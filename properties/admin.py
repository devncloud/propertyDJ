from django.contrib import admin
from django.utils.html import mark_safe

from .models import State, City, Property, Feature, Amenity, FloorPlan, PropertyImage


class CityInline(admin.TabularInline):
    model = City
    extra = 1
    show_change_link = True

class StateAdmin(admin.ModelAdmin):
    model = State
    extra = 1
    show_change_link = True
    inlines = [CityInline]


class FloorPlanInline(admin.TabularInline):
    model = FloorPlan
    extra = 1
    show_change_link = True
    readonly_fields = ('display_image',)
    fields = ('floor_plan_file', 'description')

    def display_image(self, obj):
        return mark_safe(f'<img src="{obj.floor_plan_file.url}" width="50" height="50" />')
    display_image.short_description = 'Floor Plan'


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage  # Use PropertyImage directly
    extra = 0  # No extra empty forms
    fields = ('image', 'is_primary', 'display_image')  # Display image and is_primary
    readonly_fields = ('display_image',)  # Make the image display readonly

    # Add a method to display image thumbnails in the inline
    def display_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
    display_image.short_description = 'Image'


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'starting_price', 'status', 'city', 'created_at')
    search_fields = ('title', 'address', 'city__name')
    list_filter = ('property_type', 'status', 'city')
    ordering = ('-created_at',)

    filter_horizontal = ['features', 'amenities']

    # Adding the image display method for list view
    def display_images(self, obj):
        images = obj.property_images.all()  # 'property_images' is the related name we used
        html = ''
        for image in images:
            html += f'<img src="{image.image.url}" width="50" height="50" style="margin-right: 5px;" />'
        return mark_safe(html)  # Safely render HTML

    display_images.short_description = 'Images'

    # Add the PropertyImageInline to the property admin form
    inlines = [PropertyImageInline, FloorPlanInline]


# class FloorPlanAdmin(admin.ModelAdmin):
#     list_display = ['property', 'floor_plan_file', 'description']
#     search_fields = ['property__title', 'description']


# Register the models
admin.site.register(Property, PropertyAdmin)
admin.site.register(Feature)
admin.site.register(Amenity)
admin.site.register(State, StateAdmin)

