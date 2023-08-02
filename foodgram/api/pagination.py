from rest_framework.pagination import PageNumberPagination


class FoodgramPagination(PageNumberPagination):
    """
    Пагинатор с параметром количества результатов в выдаче = limit.
    """
    page_size_query_param = 'limit'
