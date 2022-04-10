from django.db import models

# Create your models here.
class dietm(models.Model):
    id = models.AutoField(primary_key=True)
    age=models.CharField(blank=False, max_length=50)
    weight = models.EmailField(blank=False)
    diet_type = models.CharField(choices=(
        ('Weight loss', "Weight loss"),
        ('Weight loss', 'Weight loss'),
        ('Weight loss', 'Weight loss'),
      
    ), max_length=40) 
   