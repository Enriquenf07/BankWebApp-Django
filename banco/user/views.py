from django.shortcuts import render, redirect
from django.views.generic import View
from django.db import transaction
from .models import UserAccount, UserTransaction

# Create your views here.


