from django.shortcuts import render, redirect
from django.views.generic import View
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib import messages

from user import models
from user import forms

# Create your views here.
User = get_user_model()

class HomeView(View):
    def get(self, request):
        current_user = User.objects.get(id='2')
        current_account = models.UserAccount.objects.get(id='1')
        balance = current_account.balance
        transactions = models.UserTransaction.objects.filter(Q(sender=current_account) | Q(receiver=current_account))
        context = {
            'user': current_user,
            'account': current_account,
            'transactions': transactions,
            'balance': balance
        }
        return render(request=request, template_name='user_interface/home.html', context=context)

class AccountView(View):
    def get(self, request):
        #current_user = models.UserAccount.objects.get(user=request.user)
        current_user = User.objects.get(id='2')
        current_account = models.UserAccount.objects.get(id='1')
        balance = current_account.balance
        transactions = models.UserTransaction.objects.filter(Q(sender=current_account) | Q(receiver=current_account))
        context = {
            'user': current_user,
            'account': current_account,
            'transactions': transactions,
            'balance': balance
        }
        return render(request=request, template_name='user_interface/account.html', context=context)

class TransactionView(View):
    def get(self, request):
        form1 = forms.TransactionValueForm()
        form2 = forms.TransactionReceiverForm()
        current_user = User.objects.get(id='2')
        current_account = models.UserAccount.objects.get(id='1')
        balance = current_account.balance
        context = {
            'user': current_user,
            'account': current_account,
            'balance': balance,
            'form1': form1,
            'form2': form2
        }
        return render(request=request, template_name='user_interface/transaction.html', context=context)
    def post(self, request):
        form1 = forms.TransactionValueForm(request.POST)
        form2 = forms.TransactionReceiverForm(request.POST)
        current_user = models.UserAccount.objects.get(id='1')
        
        if form1.is_valid() and form2.is_valid():
            value = form1.cleaned_data['value']
            receiver_key = form2.cleaned_data['receiver']
            if models.UserAccount.objects.filter(pix_key=receiver_key).count() == 1:
                receiver_user = models.UserAccount.objects.get(pix_key=receiver_key)
            else:
                messages.error(request, 'Chave pix não encontrada')
                return redirect('transaction')
            with transaction.atomic():
                if current_user.balance >= value and value>0:
                    current_user.balance -= value
                    receiver_user.balance += value
                    ts = models.UserTransaction(sender=current_user, receiver=receiver_user, value=value)
                    current_user.save()
                    receiver_user.save()
                    ts.save()
                    return redirect('success')
                else:
                    messages.error(request, 'Saldo insuficiente ou valor não suportado')
                    return redirect('transaction')
        return redirect('transaction')
    
class SuccessView(View):
    def get(self, request):
        current_account = models.UserAccount.objects.get(id='1')
        transactions = models.UserTransaction.objects.filter(sender=current_account) 
        transaction = transactions.latest('date_time')
        context = {
            'transaction': transaction
        }
        return render(request=request, template_name='user_interface/success.html', context=context)

class TransferAreaView(View):
    def get(self, request):
        current_account = models.UserAccount.objects.get(id='1')
        pix_key = current_account.pix_key
        context = {
            'pix_key': pix_key
        }
        return render(request=request, template_name='user_interface/transfer.html', context = context)

