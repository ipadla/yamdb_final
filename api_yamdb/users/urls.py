from django.urls import include, path
from rest_framework import routers
from users.views import AuthView, SignupView, UsersDetailViewSet, UsersViewSet

router = routers.DefaultRouter()
router.register(r'users', UsersViewSet, basename='user')
router.register(r'users', UsersDetailViewSet, basename='users-detail')

urlpatterns = [
    path('v1/auth/signup/', SignupView.as_view()),
    path('v1/auth/token/', AuthView.as_view()),
    path('v1/', include(router.urls))
]
