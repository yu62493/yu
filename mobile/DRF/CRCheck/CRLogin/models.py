from django.db import models

class CRUser(models.Model):
    emplno = models.CharField(max_length=5, default='')
    password = models.CharField(max_length=20, default='123456')
    deptno = models.CharField(max_length=1, default='')
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']