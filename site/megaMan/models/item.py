from django.db import models
from frcRobotMaster.util.genKey import genKey
from django.utils.timezone import now


class item(models.Model):

    itemID = models.CharField(max_length=10,
                              primary_key=True,
                              verbose_name='Item ID',
                              default= genKey(prefix='IT-'),
                              blank=True
                              )

    location = models.ForeignKey('megaMan.location',
                                 on_delete= models.SET_NULL,
                                 null= True,
                                 blank= True,
                                 verbose_name='Current Location')

    details = models.ForeignKey('megaMan.partDetail',
                                on_delete=models.CASCADE,
                                verbose_name='Is a')

    serialNumber = models.CharField(max_length=150,
                                    verbose_name='Serial Number',
                                    null=True,
                                    blank=True)

    purchasedPrice = models.DecimalField(default=0,
                                         decimal_places=2,
                                         max_digits=9,
                                         verbose_name='Purchased Price',
                                         )

    purchasedDate = models.DateField(default=now,
                                     null=True,
                                     blank=True,
                                     verbose_name='Purchased Date')

    kop = models.BooleanField(default=False,
                              verbose_name='From the Kit of Parts')

    quantity = models.PositiveIntegerField(default=1,
                                           verbose_name='Quantity')

    totalPrice = models.DecimalField(default=0,
                                     decimal_places=2,
                                     max_digits = 9,
                                     verbose_name='Total Price ($)'
                                     )

    totalWeight = models.DecimalField(default=0,
                                      decimal_places=5,
                                      max_digits=18,
                                      verbose_name='Total Weight (lb)')

    inFRC_BOM = models.BooleanField(default=True)

    @property
    def calcTotalPrice(self):
        running = 0
        if self.details is not None:
            running = self.quantity * self.details.marketPrice
            if not self.details.manufacturer.isSponsor:
                running = running + self.details.laborPrice

        return running

    @property
    def calcTotalWeight(self):
        if self.details is not None:
            return self.quantity * self.details.weight

    @property
    def calcInFRC_BOM(self):
        if self.kop:
            return False
        elif self.details.cots and self.totalPrice < 5:
            return False
        else:
            return True

    def save(self, *args, **kwargs):
        if self.details is not None:
            self.totalPrice = round(float(self.calcTotalPrice), 2)
            self.totalWeight = round(float(self.calcTotalWeight), 4)
            self.inFRC_BOM = self.calcInFRC_BOM

        super().save(*args, **kwargs)

    def __str__(self):
        if self.itemID is not None and self.details is not None:
            return '{} - {}'.format(self.itemID, self.details.name)

#TODO - When included with the other admin pages save fails.