from django.db import models

# Create your models here.

class SystemVuln(models.Model):
    vulnname = models.CharField(max_length=100)
    vulnlevel = models.CharField(max_length=2)
    vuln_createtime = models.DateField(auto_now=False, auto_now_add=False)
