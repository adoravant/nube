from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'accounts'
urlpatterns = [
    path('dashboard/', views.dashBoard, name="dashboard"),
    path('customer/<str:pk>/', views.customer, name="customer"),
        path('register/', views.registerPage, name="register"),
	path('registro-sponsor-libronube/', views.delayed_register, name="delayed_register"),
	path('accounts/login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),
    path('account/', views.accountSettings, name="account"),
    path('products/', views.products, name='products'),
    
    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    
    #PASSWORD RELATED
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),
]
