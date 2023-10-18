from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.feedback import services
from applications.feedback.services import get_reviewers


class FavoriteMixin:
    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        status_ = services.add_del_favorite(user=user, obj=obj)
        return Response(
            {
                'status': status_,
                'user': user.email,
                'movie': obj.title
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['GET'])
    def get_favorites(self, request):
        product_data = services.get_favorites(user=request.user)
        return Response(product_data, status=status.HTTP_200_OK)


class CommentMixin:
    @action(methods=['POST'], detail=True)
    def give_comment(self, request, pk=None):
        try:
            comment = request.data['comment']
            user = request.user
            obj = self.get_object()
            status_ = services.give_comment(user=user, obj=obj, comment=comment)
            return Response(
                {
                    'status': status_,
                    'user': user.email,
                    'comment': comment
                }, status=status.HTTP_200_OK
            )
        except MultiValueDictKeyError:
            return Response('поле comment обьязательно')
        except KeyError:
            return Response('поле comment обьязательно')

    @action(methods=['POST'], detail=True)
    def del_comment(self, request, pk=None):
        user = request.user
        obj = self.get_object()
        services.del_comment(obj=obj, user=user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=True)
    def commentators(self, request, pk=None):
        return Response(services.get_commentators(obj=self.get_object()), status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def comments(self, request):
        try:
            return Response(services.get_comments(user=request.user), status=status.HTTP_200_OK)
        except TypeError:
            return Response({'msg': 'вы не авторизованы'}, status=status.HTTP_400_BAD_REQUEST)


class LikeMixin:
    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        status_ = services.like_unlike(user=user, obj=obj)
        return Response({'status': status_, 'user': user.email}, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def fans(self, request, pk=None):
        obj = self.get_object()
        return Response(services.get_fans(obj=obj), status=status.HTTP_200_OK)


class RatingMixin:
    @action(detail=True, methods=['POST'])
    def give_rating(self, request, pk=None):
        try:
            obj = self.get_object()
            user = request.user
            rating = request.data['rating']
            status_ = services.give_rating(obj=obj, user=user, rating=rating)
            return Response({'status': status_, 'rating': rating, 'user': user.email}, status=status.HTTP_200_OK)
        except MultiValueDictKeyError:
            return Response('поле rating обязательно')

    @action(methods=['POST'], detail=True)
    def del_rating(self, request, pk=None):
        user = request.user
        obj = self.get_object()
        services.del_rating(user=user, obj=obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=True)
    def reviewers(self, request, pk=None):
        obj = self.get_object()
        users_data = get_reviewers(obj=obj)
        return Response(users_data, status=status.HTTP_200_OK)
