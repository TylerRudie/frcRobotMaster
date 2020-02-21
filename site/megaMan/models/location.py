from django.db import models
from exclusivebooleanfield.fields import ExclusiveBooleanField
from frcRobotMaster.util.genKey import genKey
from megaMan.util.frcBOM import frcBOM

locationType=(('rb', 'Robot'),
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

    @property
    def FRC_Total(self):
        total = float(self.item_set.filter(inFRC_BOM=True).aggregate(models.Sum('totalPrice'))['totalPrice__sum'])
        return round(total, 2)

    @property
    def totalPrice(self):
        total = float(self.item_set.all().aggregate(models.Sum('totalPrice'))['totalPrice__sum'])
        return round(total, 2)

    @property
    def totalWeight(self):
        total = float(self.item_set.all().aggregate(models.Sum('totalWeight'))['totalWeight__sum'])
        return round(total, 2)

    def frcBOM_Entry(self):
        return self.item_set.filter(inFRC_BOM=True).values('details__shortDescription',
                                                           'details__material__name',
                                                           'details__manufacturer__name',
                                                           'quantity',
                                                           'details__measurement',
                                                           'details__marketPrice',
                                                           'totalPrice')

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

