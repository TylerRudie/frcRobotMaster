from django.db import models
from frcRobotMaster.util.genKey import genKey

measurementSet = (('ea', 'Each'),
                  ('in', 'Inch'),
                  ('lb', 'Pounds')
                  )


class partDetail(models.Model):
    partID = models.CharField(max_length=10,
                              primary_key= True,
                              verbose_name= 'Part ID'
                              )

    name = models.CharField(max_length= 20,
                            verbose_name='Part Name')

    manufacturerPartNumber = models.CharField(max_length= 150,
                                              verbose_name='Manufacturer Part Number',
                                              null=True,
                                              blank=True,
                                              )

    shortDescription = models.CharField(max_length= 60,
                                        verbose_name='Short Description',
                                        null=True,
                                        blank=True,
                                        )

    longDescription = models.TextField(verbose_name='Long Description',
                                       null=True,
                                       blank=True,
                                       )

    marketPrice = models.DecimalField(default=0,
                                      decimal_places=2,
                                      max_digits=9)

    laborPrice = models.DecimalField(default=0,
                                     decimal_places=2,
                                     max_digits=9)

    weight = models.DecimalField(default=0,
                                 decimal_places=6,
                                 max_digits=9,
                                 verbose_name='Weight (lbs)')

    measurement = models.CharField(choices=measurementSet,
                                   max_length= 6,
                                   default='ea')

    cots = models.BooleanField(default= True,
                               verbose_name='Commercial off the shelf')

    material = models.ForeignKey('megaMan.material',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 )

    manufacturer = models.ForeignKey('megaMan.manufacturer',
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True,
                                     )

    category = models.ForeignKey('megaMan.category',
                                 on_delete=models.SET_NULL,
                                 null= True,
                                 blank= True,)

    thumbnail = models.ImageField(upload_to='qMaster/partDetail/',
                                  null=True,
                                  blank=True)

    def __str__(self):
        if self.name is not None and self.manufacturer is not None:
            return '{} - {}'.format(self.manufacturer.name,
                                    self.name)
        else:
            return '------------'

    def save(self, *args, **kwargs):
        while not self.partID:
            pk = genKey(prefix='PD-')
            if not partDetail.objects.filter(pk=pk).exists():
                self.partID = pk

        super().save(*args, **kwargs)
