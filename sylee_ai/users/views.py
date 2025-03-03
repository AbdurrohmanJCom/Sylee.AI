from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from .models import CustomUser, Subscription, Transaction, TopUp
from .serializers import UserSerializer, SubscriptionSerializer, TransactionSerializer, TopUpSerializer
from rest_framework.permissions import AllowAny



class RegisterView(mixins.CreateModelMixin, GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

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
