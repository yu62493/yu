from rest_framework import serializers
from CRLogin.models import CRUser

"""
class CRLoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    emplno = serializers.CharField(required=False, max_length=5)
    password = serializers.CharField(required=False, max_length=20)
    status = serializers.BooleanField(required=False)

    def create(self, validated_data):
        return CRLogin.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.emplno = validated_data.get('emplno', instance.emplno)
        instance.password = validated_data.get('password', instance.password)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
"""
class CRLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRUser
        fields = ['id', 'emplno', 'password', 'status','created']