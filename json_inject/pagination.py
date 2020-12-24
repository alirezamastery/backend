from rest_framework import pagination
from rest_framework.response import Response

from .models import Sample


class ListViewPagination(pagination.PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 20


class CustomPagination(pagination.PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 20

    def get_paginated_response(self , data):
        fields = Sample._meta.get_fields()
        form = self.set_filter_type(fields)

        return Response({
            'next':         self.get_next_link() ,
            'previous':     self.get_previous_link() ,
            'count':        self.page.paginator.count ,
            'total_pages':  self.page.paginator.num_pages ,
            'available_filters': form ,
            'results':      data
        })

    @staticmethod
    def set_filter_type(fields):
        filterable_types = {
            'BooleanField':  'boolean' ,
            'CharField':     'text' ,
            'DateField':     'date' ,
            'DateTimeField': 'date' ,
            'DecimalField':  'price' ,
            'TextField':     'text' ,
        }

        form = dict()
        filters = ['price']
        for field in fields:
            field_type = field.get_internal_type()
            if field_type not in filterable_types.keys():
                continue
            form[field.name] = field.get_internal_type()
            filters.append(field.get_internal_type())

        # filters = set(filters)
        # print(filters)

        return form
