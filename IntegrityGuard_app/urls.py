
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index , name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('investigator/dashboard/', views.investigator_dashboard, name='investigator_dashboard'),
    path('reporter/dashboard/', views.reporter_dashboard, name='reporter_dashboard'),  
    path('cases/', views.Case_View, name='create_view'),
    path('create_case/', views.create_case, name='create_case'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboards/', views.reporter_dashboards, name='reporter_view'),
    path('case/edit/<int:case_id>/', views.edit_cases, name='edit_case'),
    path('view_all_Cases/', views.view_all_Cases, name='view_all_Cases'),
    path('Investigators_create', views.investigators_create, name='investigator_create'),
    path('Investigators_list', views.investigator_List, name='investigator_view'),
    path('edit_case/<int:case_id>/', views.edit_case, name='Assigned_case'),
     path('casess/', views.cases_list, name='cases_list'),
]   