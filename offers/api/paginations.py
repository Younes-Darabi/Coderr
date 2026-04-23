from rest_framework.pagination import PageNumberPagination


class OfferPagination(PageNumberPagination):
    """Custom pagination for offers list."""
    page_size = 5
    page_size_query_param = 'page_size'
