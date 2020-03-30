from . import views
from django.urls import path
from apps.vdrive.views import GDriveListView, DeleteListView


app_name = 'login'

urlpatterns = [

    path('', views.GDriveListView.as_view()),
    path('', GDriveListView.as_view(), name='list'),
    path('imports_list/', views.UserListView.as_view()),
    path('imports_list/', views.UserListView.as_view(), name='imports_list'),
    path('delete_list/', views.DeleteListView.as_view(), name='delete_list'),
    path('start_scan/', views.StartScanView.as_view(), name='start_scan')

]
