
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index , name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('investigator/dashboard/', views.investigator_dashboard, name='investigator_dashboard'),
    path('reporter/dashboard/', views.reporter_dashboard, name='reporter_dashboard'),  
    path('cases/', views.Case_View, name='create_view'),
    path('create_case/', views.create_case, name='create_case'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboards/', views.reporter_dashboards, name='reporter_view'),
    path('case/edit/<int:case_id>/', views.edit_case, name='edit_case'),
]   