from django.db import models


class Dht11(models.Model):
    temp = models.FloatField(null=True)
    hum = models.FloatField(null=True)
    dt = models.DateTimeField(auto_now_add=True,null=True)

class Incident(models.Model):
    temp = models.FloatField()
    hum = models.FloatField()
    dt = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Incident: Temp {self.temp}, Hum {self.hum}, Date {self.dt}"

class ArchivedIncident(models.Model):
    temp = models.FloatField()
    hum = models.FloatField()
    dt = models.DateTimeField()
    archived_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archived Incident: Temp {self.temp}, Hum {self.hum}, Date {self.dt}"

