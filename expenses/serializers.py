from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = (
            'id',
            'title',
            'amount',
            'date',
            'cate    D DCD gory',
            'notes',
            'created_at',
            'updated_at',
        )

class ExpenseAnalysisSerializer(serializers.Serializer):
    total_spent = serializers.DecimalField(max_digits=12, decimal_places=2)
    by_category = serializers.DictField(
        child=serializers.DecimalField(max_digits=12, decimal_places=2)
    )
    recommendations = serializers.ListField(child=serializers.CharField())
