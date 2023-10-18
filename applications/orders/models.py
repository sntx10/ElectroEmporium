from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from creditcards.models import CardNumberField, SecurityCodeField

from applications.electronics.models import Electronic


User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    electronic = models.ForeignKey(Electronic, on_delete=models.CASCADE, related_name='orders')
    count = models.PositiveIntegerField(default=1)
    order_confirm = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    cc_number = CardNumberField(_('card number'))
    cc_expiry = models.CharField(max_length=4)
    cc_code = SecurityCodeField(_('security code'))
    address = models.CharField(max_length=130)

    confirm_code = models.CharField(max_length=130, default='', null=True, blank=True)

    def create_confirm_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.confirm_code = code
