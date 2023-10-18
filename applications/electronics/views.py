# import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from applications.electronics.mixins import CharAmountMixin
from applications.electronics.models import Electronic, ParsedElectronic
from applications.electronics.permissions import IsSellerOrReadOnly
from applications.electronics.serializers import ElectronicSerializer, ParsedElectronicSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from applications.feedback.mixins import FavoriteMixin, CommentMixin, RatingMixin, LikeMixin

# loger = logging.getLogger('django_logger')


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 10000


class ElectronicViewSet(FavoriteMixin, CommentMixin, RatingMixin, LikeMixin, CharAmountMixin, ModelViewSet):
    # loger.warning('electronic CRUD')
    queryset = Electronic.objects.all()
    serializer_class = ElectronicSerializer
    permission_classes = [IsSellerOrReadOnly]
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filterset_fields = ['category']
    search_fields = ['title']
    ordering_fields = ['id', 'price']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['DELETE'])
    def del_images(self, request, pk=None):
        """
        Удаляет все картинки выбранного продукта
        :param request: запрос
        :param pk: id продукта
        """
        product = self.get_object()
        images = product.images.all()
        images.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ElectronicRecommendApiView(APIView):
    # loger.warning('electronic recommend')

    def get(self, request):
        """
        для продавцов выводит товары, спаршенные из других сайтов, а для остальных - лучшие товары нашего сайта
        :param request: запрос
        """
        try:
            user = self.request.user
            if not user.is_seller:
                queryset = Electronic.objects.order_by('-orders_count')[:9]
                serializer = ElectronicSerializer(queryset, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            queryset = ParsedElectronic.objects.all()
            serializer = ParsedElectronicSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AttributeError:
            queryset = Electronic.objects.order_by('-orders_count')[:9]
            serializer = ElectronicSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
