from rest_framework import serializers

from .models import Category , Sample , Genre , Band


class CustomListSerializer(serializers.ListSerializer):

    def update(self , instance , validated_data):
        pass

    def to_representation(self , data):  # we can inject the payload here or in the pagination class
        ret = super().to_representation(data)

        # form = dict()
        # fields = Sample._meta.get_fields()
        # for f in fields:
        #     print('type:' , Sample._meta.get_field(f.name).get_internal_type())
        #     print(f.get_internal_type())
        #     form[f.name] = f.get_internal_type()
        #
        # ret.insert(0 , form)

        return ret


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        ordering = ['-id']
        fields = ['name' , 'get_children']


class SampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sample
        ordering = ['-id']
        fields = ['name' , 'in_stock' ,
                  # 'filter_fields'  # the method we added to the Sample model
                  ]
        # list_serializer_class = CustomListSerializer    # use CustomListSerializer to inject a payload

    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     ret['ok'] = 'alright'
    #     print('ret:' , ret)
    #     return ret


# https://stackoverflow.com/questions/13376894/django-rest-framework-nested-self-referential-objects
class GenreSerializerRecursive(serializers.HyperlinkedModelSerializer):
    subcategories = serializers.SerializerMethodField(read_only=True , method_name="get_child_categories")

    class Meta:
        model = Genre
        fields = [
            'name' ,
            'parent_id' ,
            'subcategories' ,
            'get_filters'
        ]

    def get_child_categories(self , obj):
        """ self referral field """
        # if obj.level == 0:
        #     serializer = GenreSerializer(instance=obj.children.all() , many=True)
        #     return serializer.data
        # else:
        #     print('else')
        #     return {}
        serializer = GenreSerializerRecursive(instance=obj.children.all() , many=True)
        return serializer.data


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = [
            'name' ,
            'get_filters'
        ]


class BandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Band
        fields = ['name' , 'genre_id' , 'has_inventory' , 'color']
