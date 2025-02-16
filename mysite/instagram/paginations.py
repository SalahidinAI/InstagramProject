from rest_framework.pagination import PageNumberPagination


class TwoPagination(PageNumberPagination):
    page_size = 2
