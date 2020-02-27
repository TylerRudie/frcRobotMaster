from django.db import models
from frcRobotMaster.util.genKey import genKey


class manufacturer(models.Model):
    manufacturerID = models.CharField(max_length=10,
                                      primary_key=True,
                                      verbose_name='Manufacturer ID'
                                      )

    name = models.CharField(max_length=50,
                            verbose_name='Manufacturer Name')

    isSponsor = models.BooleanField(default= False,
                                    verbose_name='Sponsor')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        while not self.manufacturerID:
            pk = genKey(prefix='MA-')
            if not manufacturer.objects.filter(pk=pk).exists():
                self.manufacturerID = pk

        super().save(*args, **kwargs)
