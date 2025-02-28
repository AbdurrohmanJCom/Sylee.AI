from django.contrib import admin
from django import forms
from .models import CustomUser, Subscription, Transaction, TopUp

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    
@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    form = CustomUserForm
    list_display = ('user_id', 'referred_by', 'words', 'balance', 'language', 'date_created', 'date_updated')
    search_fields = ('user_id', 'language')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'type', 'date_created', 'date_updated')
    search_fields = ('user_id',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'type', 'amount', 'date_created', 'date_updated')
    search_fields = ('user_id', 'type')

@admin.register(TopUp)
class TopUpAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'amount', 'status', 'date_created', 'date_updated')
    search_fields = ('user_id', 'status')
