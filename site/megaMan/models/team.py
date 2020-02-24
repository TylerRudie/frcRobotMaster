from django.db import models
from frcRobotMaster.util.genKey import genKey
from localflavor.us.us_states import US_STATES


class team(models.Model):
    teamID = models.CharField(max_length=10,
                              primary_key=True,
                              verbose_name='Team ID'
                              )

    name = models.CharField(max_length=50,
                            verbose_name='Location Name')

    default = models.BooleanField(default=False)

    teamNumber = models.PositiveIntegerField(default= 0)

    event = models.CharField(max_length=50,
                             null= True,
                             blank= True)

    city = models.CharField(max_length=50,
                            null= True,
                            blank=True
                            )

    state = models.CharField(max_length=2,
                             choices=US_STATES,
                             null= True,
                             blank=True
                             )
    logo = models.ImageField(upload_to='qMaster/team/',
                             null=True,
                             blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        while not self.teamID:
            pk = genKey(prefix='CT-')
            if not team.objects.filter(pk=pk).exists():
                self.teamID = pk

        super().save(*args, **kwargs)
