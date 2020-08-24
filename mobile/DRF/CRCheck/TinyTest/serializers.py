from django.utils.timezone import now
from rest_framework import serializers
from TinyTest.models import CRlogin

class TinyTestSerializer(serializers.ModelSerializer):
   days_since_created = serializers.SerializerMethodField()

   class Meta:
       model = CRlogin
       # fields = '__all__'
       fields = ('id', 'emplno', 'deptno', 'password', 'last_modify_date', 'created', 'days_since_created')

   def get_days_since_created(self, obj):
       return (now() - obj.created).days


class LoginSerializer(serializers.ModelSerializer):

   class Meta:
       model = CRlogin
       fields = ('id', 'emplno', 'deptno')

