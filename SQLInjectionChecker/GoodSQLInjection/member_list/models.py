from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name + " " + str(self.age)