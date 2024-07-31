from django.contrib import admin

from .models import *


class ApartmentsImagesInline(admin.TabularInline):
    model = ApartmentImage
    extra = 1


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "year", "city", "street", "number")
    list_display_links = ("id", "name")
    list_per_page = 20
    search_fields = ("name", "city", "street", "number")
    list_filter = ("year", "city")


@admin.register(Apartment)
class ApartmentsAdmin(admin.ModelAdmin):
    list_display = ("id", "building", "area", "rooms", "price", "floor")
    list_display_links = ("id", "building")
    list_per_page = 20
    search_fields = ("building",)
    list_filter = ("rooms", "floor")
    inlines = [ApartmentsImagesInline]


@admin.register(ApartmentImage)
class ApartmentsImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "apartment")
    list_display_links = ("id", "apartment")
    list_per_page = 20
    search_fields = ("apartment",)
    list_filter = ("apartment",)
