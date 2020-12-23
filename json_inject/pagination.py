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
        form = dict()
        fields = Sample._meta.get_fields()
        for f in fields:
            if f.get_internal_type() != 'AutoField':
                form[f.name] = f.get_internal_type()

        return Response({
            'next':         self.get_next_link() ,
            'previous':     self.get_previous_link() ,
            'count':        self.page.paginator.count ,
            'total_pages':  self.page.paginator.num_pages ,
            'form_filters': form ,
            'results':      data
        })
