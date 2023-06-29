from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class UserAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='userAccount', on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11)
    pix_key = models.CharField(max_length=100, unique=True, blank=False)
    balance = models.FloatField(_("balance"), default=0)

    def __str__(self):
        return f'{self.user.username}'

class UserTransaction(models.Model):
    sender = models.ForeignKey("UserAccount", on_delete=models.CASCADE, related_name="sent_transactions")
    receiver = models.ForeignKey("UserAccount", on_delete=models.CASCADE, related_name="received_transactions")
    value = models.FloatField(_("value"))
    date_time = models.DateTimeField(_("date"), auto_now=False, auto_now_add=True)
        
    


