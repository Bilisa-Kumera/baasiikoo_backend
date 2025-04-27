from django.http import HttpResponse
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, permissions
from .models import Expense
from .serializers import ExpenseSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Sum
from .serializers import ExpenseAnalysisSerializer
from .services.gemini_client import analyze_with_gemini
from rest_framework import status

# Serializer for signup
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Signup API
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to Expense Tracker API</h1>")


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return expenses for the logged-in user
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Set the user on create
        serializer.save(user=self.request.user)

 

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def analyze_expenses(request):
    user = request.user
    qs = user.expenses.all()

    # 1) Total spent
    total = qs.aggregate(sum=Sum('amount'))['sum'] or 0

    # 2) Sum by category
    cat_data = qs.values('category') \
                 .annotate(total=Sum('amount')) \
                 .order_by('-total')

    by_category = {item['category']: item['total'] for item in cat_data}

    # 3) Recommendations
    recs = []
    if total > 0:
        for category, amt in by_category.items():
            pct = (amt / total) * 100
            if pct > 30:
                recs.append(
                  f"You spent {pct:.1f}% of your budget on {category}. "
                  "Consider reducing it by 10% next month."
                )
        if not recs:
            recs.append("Great job! Your spending is well-distributed.")
    else:
        recs.append("No expenses to analyze yet.")

    data = {
        'total_spent': total,
        'by_category': by_category,
        'recommendations': recs
    }

    serializer = ExpenseAnalysisSerializer(data)
    return Response(serializer.data)




@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def analyze_expenses_ai(request):
    user = request.user
    qs = user.expenses.order_by('-date')[:50]

    expenses_data = [
        {
            "title": e.title,
            "amount": float(e.amount),
            "category": e.category,
            "date": e.date.isoformat(),
        }
        for e in qs
    ]

    try:
        ai_response = analyze_with_gemini(expenses_data)
    except Exception as e:
        return Response(
            {"detail": "AI analysis failed", "error": str(e)},
            status=status.HTTP_502_BAD_GATEWAY
        )

    return Response({"analysis": ai_response})



