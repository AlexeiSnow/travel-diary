from django.contrib import admin
from .models import Trip, TripPhoto


class TripPhotoInline(admin.TabularInline):
    model = TripPhoto
    extra = 1


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'location_name', 'rating_avg', 'created_at']
    list_filter = ['author', 'created_at']
    search_fields = ['title', 'location_name', 'description']
    inlines = [TripPhotoInline]


@admin.register(TripPhoto)
class TripPhotoAdmin(admin.ModelAdmin):
    list_display = ['trip', 'caption']