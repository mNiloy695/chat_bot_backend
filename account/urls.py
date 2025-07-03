from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('register',views.RegistrationView,basename='register')


urlpatterns = [
   
   path('',include(router.urls)),
   path('login/',views.LoginView.as_view(),name='login'),
   path('logout/',views.LogoutView.as_view(),name='logout'),
]


