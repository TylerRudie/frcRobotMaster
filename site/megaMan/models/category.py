from django.db import models
from frcRobotMaster.util.genKey import genKey


class category(models.Model):
    categoryID = models.CharField(max_length=10,
                                  primary_key=True,
                                  verbose_name='Category ID'
                                  )

    name = models.CharField(max_length=50,
                            verbose_name='Category Name')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        while not self.categoryID:
            pk = genKey(prefix='CT-')
            if not category.objects.filter(pk=pk).exists():
                self.categoryID = pk

        super().save(*args, **kwargs)