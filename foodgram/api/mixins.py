from rest_framework import mixins, viewsets


class CreateDeleteViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    '''Создает и удаляет ообъек.'''

    pass


class CustomListViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    Вьюсет для получения списка объектов при GET-запросе.
    """
    pass
