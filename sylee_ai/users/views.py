from django.shortcuts import render
from rest_framework import viewsets
from .models import CustomUser, Subscription, Transaction, TopUp
from .serializers import UserSerializer, SubscriptionSerializer, TransactionSerializer, TopUpSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TopUpViewSet(viewsets.ModelViewSet):
    queryset = TopUp.objects.all()
    serializer_class = TopUpSerializer
