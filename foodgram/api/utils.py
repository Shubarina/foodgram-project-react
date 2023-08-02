from rest_framework import status
from rest_framework.response import Response


def model_object_create(request, object, serializer):
    """
    Базовая функция для создания объекта связанной модели.
    Для моделей Favorite/ShoppingList.
    """
    serializer = serializer(
        data={'user': request.user.id, 'recipe': object.id},
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def model_object_delete(request, object, Model, message):
    """
    Базовая функция для удаления объекта связанной модели.
    Для моделей Favorite/ShoppingList.
    """
    object = Model.objects.filter(user=request.user, recipe=object)
    if not object.exists():
        return Response({'errors': message},
                        status=status.HTTP_400_BAD_REQUEST)
    object.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
