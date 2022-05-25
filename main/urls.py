from django.urls import path
from main import views
from django.contrib.auth.views import LogoutView


app_name = "main"
#static urls patterns
urlpatterns = [
    path('', views.home_view, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.about, name='contact'),
    path('propety-agent/', views.property_agent, name='property_agent'),
    path('property-type/', views.property_type, name='property_type'),
    path('property-list/', views.property_list, name='property_list'),
    path('testimonial/', views.testimonial, name='testimonial')
   ]


htmx_patterns = []

urlpatterns += htmx_patterns