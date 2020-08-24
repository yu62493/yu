from django.db import models

# Create your models here.
class CRlogin(models.Model):
    emplno = models.TextField()
    password = models.TextField()
    deptno = models.TextField()
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "CRlogin"


    def login_check(**kwargs):
        emplno = kwargs.get('emplno')
        password = kwargs.get('password')
        print(emplno)
        print(password)
        if emplno:
            result = CRlogin.objects.raw('SELECT * FROM CRlogin WHERE emplno = %s and password = %s', [emplno,password])
        else:
            result = []
        return result

    def fun_raw_sql_query(**kwargs):
        emplno = kwargs.get('emplno')
        if emplno:
            result = CRlogin.objects.raw('SELECT * FROM CRlogin WHERE emplno = %s', [emplno])
        else:
            result = CRlogin.objects.raw('SELECT * FROM CRlogin')
        return result