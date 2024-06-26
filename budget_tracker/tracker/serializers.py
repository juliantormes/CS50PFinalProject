from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Expense, ExpenseCategory, IncomeCategory, Income, CreditCard, ExpenseChangeLog, IncomeChangeLog
from decimal import Decimal

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        return data

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        exclude = ['user']

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    credit_card = CreditCardSerializer(read_only=True)
    credit_card_id = serializers.PrimaryKeyRelatedField(
        queryset=CreditCard.objects.all(),
        source='credit_card',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Expense
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

    def validate(self, data):
        if data.get('pay_with_credit_card', False) and not data.get('credit_card'):
            raise serializers.ValidationError("Credit card must be provided if paying with credit card.")

        if data.get('pay_with_credit_card', False):
            credit_card = data.get('credit_card')
            current_balance = credit_card.current_balance()
            total_new_expense = data['amount'] + (data['amount'] * data['surcharge'] / 100)
            if current_balance + total_new_expense > credit_card.credit_limit:
                raise serializers.ValidationError(
                    f"Credit limit exceeded. Current balance: {current_balance}, "
                    f"New expense total: {total_new_expense}, Credit limit: {credit_card.credit_limit}"
                )

        if not data.get('pay_with_credit_card', False):
            data['credit_card'] = None
            data['installments'] = 1
            data['surcharge'] = Decimal('0.00')

        return data

    def create(self, validated_data):
        credit_card = validated_data.pop('credit_card', None)
        expense = Expense.objects.create(**validated_data)
        if credit_card:
            expense.credit_card = credit_card
            expense.save()
        return expense

    def update(self, instance, validated_data):
        credit_card = validated_data.pop('credit_card', None)
        instance = super().update(instance, validated_data)
        if credit_card:
            instance.credit_card = credit_card
            instance.save()
        return instance
class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

class IncomeSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Income
        fields = ['id', 'amount', 'date', 'user', 'category', 'category_name', 'is_recurring', 'description']
        extra_kwargs = {'user': {'read_only': True}}

class ExpenseChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseChangeLog
        fields = '__all__'

class IncomeChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeChangeLog
        fields = '__all__'
