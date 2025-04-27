from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignupView, ExpenseViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')

from .views import analyze_expenses
from .views import analyze_expenses_ai




urlpatterns = [
    # Auth
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('analysis/', analyze_expenses, name='expense-analysis'),
    path('analysis/ai/', analyze_expenses_ai, name='expense-analysis-ai'),



    # Expense CRUD
    path('', include(router.urls)),

]
