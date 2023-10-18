from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.electronics.models import Characteristic


class CharAmountMixin:
    @action(methods=['POST'], detail=True)
    def characteristic(self, request, pk):
        """
        позволяет добавить характеристику продукта
        :param request: запрос
        :param pk: id продукта, которому нужно добавить характеристику
        """
        electronic = self.get_object()
        characteristic_obj, is_created = Characteristic.objects.get_or_create(electronic=electronic)
        data = dict(request.data)
        data = {k: v[0] for k, v in data.items() if isinstance(v, list)}
        for k, v in data.items():
            setattr(characteristic_obj, k, v)
        characteristic_obj.save()
        msg = 'характеристики обновлены'
        if is_created:
            msg = 'характеристики добавлены'
        return Response({'msg': msg}, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True)
    def amount(self, request, pk=None):
        """
        позволяет увеличить количество продукта
        :param request: запрос
        :param pk: id продукта который нужно увеличить
        """
        try:
            electronic = self.get_object()
            amount = request.data['amount']
            electronic.amount += int(amount)
            electronic.save(update_fields=['amount'])
            return Response({'msg': 'Продкуты добавлены'}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({'msg': 'Поле amount обязательно'}, status.HTTP_400_BAD_REQUEST)
