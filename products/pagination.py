from rest_framework import pagination
from rest_framework.response import Response


class ListViewPagination(pagination.PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 20


class CustomPagination(pagination.PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 20

    def get_paginated_response(self , data):
        return Response({
            'next':        self.get_next_link() ,
            'previous':    self.get_previous_link() ,
            'count':       self.page.paginator.count ,
            'total_pages': self.page.paginator.num_pages ,
            'results':     data
        })
