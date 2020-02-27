from django.db import models
from frcRobotMaster.util.genKey import genKey


class material(models.Model):
    materialID = models.CharField(max_length=10,
                                  primary_key=True,
                                  verbose_name='Material ID'
                                  )

    name = models.CharField(max_length=50,
                            verbose_name='Material Name')

    def __str__(self):
        return "{} - ({})".format(self.name, self.materialID)

    def save(self, *args, **kwargs):
        while not self.materialID:
            pk = genKey(prefix='MT-')
            if not material.objects.filter(pk=pk).exists():
                self.materialID = pk

        super().save(*args, **kwargs)
