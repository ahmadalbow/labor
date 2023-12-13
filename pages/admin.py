from django.contrib import admin

from pages.models import MeasurementValues, Measurement


class MeasurementValuesInline(admin.TabularInline):
    model = MeasurementValues

class MeasurementAdmin(admin.ModelAdmin):
    inlines = [MeasurementValuesInline]

admin.site.register(Measurement, MeasurementAdmin)