from django.db import models
from exclusivebooleanfield.fields import ExclusiveBooleanField
from frcRobotMaster.util.genKey import genKey
from django.urls import reverse
from django.utils.safestring import mark_safe
from megaMan.util.frcBOM import frcBOM

locationType = (('rb', 'Robot'),
                ('as', 'Assembly'),
                ('bi', 'Bin'),
                ('to', 'Tote'),
                ('sf', 'Shelf')
                )


class location(models.Model):
    locationID = models.CharField(max_length=10,
                                  primary_key=True,
                                  verbose_name='Location ID'
                                  )

    default = ExclusiveBooleanField(default = False)

    name = models.CharField(max_length=50,
                            verbose_name='Location Name')

    owner = models.ForeignKey('megaMan.team',
                              on_delete=models.SET_NULL,
                              null='True',
                              blank='True')

    partOf = models.ForeignKey('self',
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               verbose_name='Part Of')

    type = models.CharField(max_length=6,
                            choices= locationType,
                            default='sf')

    dropDownWeight = models.PositiveIntegerField(default=30
                                                 )

    thumbnail = models.ImageField(upload_to='qMaster/location/',
                                  null=True,
                                  blank=True)

    @property
    def FRC_Total(self):
        itemSet = self.item_set.filter(inFRC_BOM=True)
        if itemSet is not None and len(itemSet) > 0:
            total = float(itemSet.aggregate(models.Sum('totalPrice'))['totalPrice__sum'])
        else:
            total = 0
        return round(total, 2)

    @property
    def totalPrice(self):
        itemSet = self.item_set.all()
        if itemSet is not None and len(itemSet) > 0:
            total = float(itemSet.aggregate(models.Sum('totalPrice'))['totalPrice__sum'])
        else:
            total = 0
        return round(total, 2)

    @property
    def totalWeight(self):
        itemSet = self.item_set.all()
        if itemSet is not None and len(itemSet) > 0:
            total = float(itemSet.aggregate(models.Sum('totalWeight'))['totalWeight__sum'])
        else:
            total = 0
        return round(total, 2)

    @property
    def grandFRC_Total(self):
        total = self.FRC_Total
        for it in self.location_set.all():
            total = total + it.FRC_Total
        return total

    @property
    def grandTotalWeight(self):
        total = self.totalWeight
        for it in self.location_set.all():
            total = total + it.totalWeight
        return round(total, 4)

    @property
    def grandTotalPrice(self):
        total = self.totalPrice
        for it in self.location_set.all():
            total = total + it.totalPrice
        return round(total, 2)

    @property
    def getFRC_BOM_URL(self):
        if self.locationID is not None and len(self.locationID) > 0:
            url = reverse('frc-bom', kwargs={'pk': self.locationID})
            return mark_safe('<a href="{0}">{1} - FRC BOM</a>'.format(url, self.name))
        else:
            return '----'

    def frcBOM_Entry(self):
        return self.item_set.filter(inFRC_BOM=True).values('details__name',
                                                           'details__shortDescription',
                                                           'details__material__name',
                                                           'details__manufacturer__name',
                                                           'quantity',
                                                           'details__measurement',
                                                           'details__marketPrice',
                                                           'totalPrice')

    @property
    def frcBOM_fullListing(self):
        list = []
        for it in  self.location_set.all():
            list.append(frcBOM(name  = it.name,
                               cost  = it.FRC_Total,
                               items = it.frcBOM_Entry()
                               ))

        list.append(frcBOM(name  = 'Misc',
                           cost  = self.FRC_Total,
                           items = self.frcBOM_Entry()
                           ))
        return list

    def __str__(self):
        if self.name is not None and self.type is not None:
            return "{} - {}".format(self.get_type_display(),
                                    self.name)
        else:
            return '------'

    def save(self, *args, **kwargs):
        while not self.locationID :
            pk = genKey(prefix='LO-')
            if not location.objects.filter(pk= pk).exists():
                self.locationID = pk

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['dropDownWeight', 'name']

