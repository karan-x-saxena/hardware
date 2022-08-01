from django.urls import path
from . import views
urlpatterns = [
   path('',views.login,name='login'),
   path('home',views.index,name='home'),
   path('machine',views.type_of_machine,name='machine'),
   path('section',views.section_master,name='section'),
   path('hardware',views.hardware,name='hardware'),
   path('logout',views.logout,name='logout'),
   path('entry_sec',views.entry_section,name="entry_sec"),
   path('entry_emp',views.entry_employee,name="entry_emp"),
   path('report',views.report,name='report'),
   path('wing',views.wing,name='wing'), 
   path('reporte',views.entry_report,name='reporte'),
   path('reports',views.section_report,name='reports'),
]