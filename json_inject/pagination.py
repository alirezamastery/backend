from rest_framework import pagination
from rest_framework.response import Response


class ListViewPagination(pagination.PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 20


class CustomPaginationBase(pagination.PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 20
    model_class = None
    filterable_types = {
        'BooleanField':  'boolean' ,
        'CharField':     'text' ,
        'DateField':     'date' ,
        'DateTimeField': 'date' ,
        'DecimalField':  'price' ,
        'TextField':     'text' ,
    }

    def get_paginated_response(self , data):
        form = self.set_filter_type()

        return Response({
            'next':        self.get_next_link() ,
            'previous':    self.get_previous_link() ,
            'count':       self.page.paginator.count ,
            'total_pages': self.page.paginator.num_pages ,
            'filters':     form ,
            'results':     data
        })

    def set_filter_type(self):
        if not self.model_class:
            raise RuntimeError('model_class is no specified')

        fields = self.model_class._meta.get_fields()

        form = dict()
        filters = ['price']
        for field in fields:
            field_type = field.get_internal_type()
            if field_type not in self.filterable_types.keys():
                continue
            form[field.name] = field.get_internal_type()
            filters.append(field.get_internal_type())

        for attr in self.model_class.__dict__:
            if hasattr(self.model_class.__dict__[attr] , 'filterable') and \
                    getattr(self.model_class.__dict__[attr] , 'filterable'):
                filters.append(attr)

        filters = set(filters)
        # print(filters)

        return filters
