from django.urls import path,include
from .views import Register,Unamevalid,homec,Emailvalid,LoginView,LogoutView
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.home,name='home page'),
    path('c/', homec.as_view()),
    path('register/',Register.as_view(), name ='register'),
    path('login/',LoginView.as_view(), name ='login'),
    path('u_validate',csrf_exempt( Unamevalid.as_view()),name='uvalidate'),
    path('e_validate',csrf_exempt(Emailvalid.as_view()),name="evalidate"),
    path('logout/',LogoutView.as_view(),name="logout")
    
]


