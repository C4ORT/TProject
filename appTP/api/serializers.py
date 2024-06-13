from rest_framework import serializers
from ..models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "id",
            "name",
            "surname",
            "lastname",

            "gender",
            "status",
            "office",
            "work_phone",
            "cellphone",
            "position",
            "photo",
            "created",



        )