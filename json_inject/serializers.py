from rest_framework import serializers

from .models import Sample


class CustomListSerializer(serializers.ListSerializer):

    def update(self , instance , validated_data):
        pass

    def to_representation(self, data):
        ret = super().to_representation(data)

        form = dict()
        fields = Sample._meta.get_fields()
        for f in fields:
            print('type:' , Sample._meta.get_field(f.name).get_internal_type())
            print(f.get_internal_type())
            form[f.name] = f.get_internal_type()

        ret.insert(0,form)

        return ret


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = ['name' , 'filter_fields']
        list_serializer_class = CustomListSerializer

    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     ret['ok'] = 'alright'
    #     print('ret:' , ret)
    #     return ret
