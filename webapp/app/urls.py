from django.urls import path
import app.views as views
urlpatterns = [
    path('',views.mainpage,name='index'),
    path('load/',views.load,name='load'),
]
