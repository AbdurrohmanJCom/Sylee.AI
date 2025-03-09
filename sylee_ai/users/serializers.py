from rest_framework import serializers
from .models import CustomUser, Subscription, Transaction, TopUp

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'user_id',
            'password',
            'referred_by',
            'words',
            'balance',
            'language',
            'is_active',
            'is_staff',
            'date_created',
            'date_updated',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            user_id=validated_data['user_id'],
            password=validated_data['password'],
            referred_by=validated_data.get('referred_by', 0),
            words=validated_data.get('words', 200),
            balance=validated_data.get('balance', 0),
            language=validated_data.get('language', 'en'),
            is_active=validated_data.get('is_active', True),
            is_staff=validated_data.get('is_staff', False)
        )
        return user

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
