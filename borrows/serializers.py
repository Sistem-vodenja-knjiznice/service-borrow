from rest_framework import serializers

from .models import Borrow

class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = '__all__'

class BorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ['user_id', 'book_id']