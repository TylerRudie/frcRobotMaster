from django.db import models
from frcRobotMaster.util.genKey import genKey


class team(models.Model):
    teamID = models.CharField(max_length=10,
                              primary_key=True,
                              verbose_name='Team ID'
                              )

    name = models.CharField(max_length=50,
                            verbose_name='Location Name')

    default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        while not self.teamID:
            pk = genKey(prefix='CT-')
            if not team.objects.filter(pk=pk).exists():
                self.teamID = pk

        super().save(*args, **kwargs)
