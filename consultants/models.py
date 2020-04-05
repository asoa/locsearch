from django.db import models


class Consultant(models.Model):

    name = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=5, null=True)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    r_certified = models.BooleanField(default=False)
    ambassador = models.BooleanField(default=False)
    distributor = models.BooleanField(default=False)
    trainee = models.BooleanField(default=False)
    trichology = models.BooleanField(default=False)
    approved = models.BooleanField(default=True)
    web_site = models.CharField(max_length=100, null=True)
    likes = models.IntegerField(default=0)

    def __str__(self):  # Show name as the identifying field
        return self.name


# class Like(models.Model):
#     foreign_key = models.ForeignKey(Consultant, on_delete='CASCADE')
