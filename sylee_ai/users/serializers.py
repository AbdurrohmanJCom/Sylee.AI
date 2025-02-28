from rest_framework import serializers
from .models import CustomUser, Subscription, Transaction, TopUp
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'user_id',
            'referred_by',
            'words',
            'balance',
            'language',
            'is_active',
            'is_staff',
            'date_created',
            'date_updated',
        ]

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'id',
            'user_id',
            'date_created',
            'date_updated',
            'type',
        ]

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'user_id',
            'type',
            'amount',
            'date_created',
            'date_updated',
        ]

class TopUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopUp
        fields = [
            'id',
            'user_id',
            'amount',
            'status',
            'date_created',
            'date_updated',
        ]
