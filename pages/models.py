from django.db import models

class Measurement(models.Model):
    date = models.DateTimeField()
    type = models.CharField(max_length=255)
    set_power_W = models.FloatField()
    current_mA = models.FloatField()
    voltage_V = models.FloatField()
    serial_number = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)

class MeasurementValues(models.Model):
    # Fields for MeasurementValues model
    wavelength = models.FloatField()
    amplitude = models.FloatField()
    
    # Foreign key to the Measurement model
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE, related_name='measurement_values')

    def __str__(self):
        return f'{self.wavelength} - {self.amplitude}' 