from django import forms

class TransactionValueForm(forms.Form):
    value = forms.FloatField(label='', required=True)
    
class TransactionReceiverForm(forms.Form):
    receiver = forms.CharField(label='', max_length=32, required=True)
