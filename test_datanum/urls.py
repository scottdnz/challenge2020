"""test_datanum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', views.index, name='index'),
    path('main/vetting-hard-coded-example', views.vetting_hard_coded_example, name='vettingHardCodedExample'),
    path('main/vetting-example', views.vetting_example, name='vettingExample'),
    path('main/get-construction-materials', views.get_construction_materials, name='get_construction_materials'),
    path('main/get-vetting-questions', views.get_vetting_questions, name='get_vetting_questions'),
    path('main/handle-construction-material-inputs', views.handle_construction_material_inputs,
         name='handle_construction_material_inputs'),
    path('main/train-results1', views.train_results1, name='train_results1'),
    path('main/app-summary-example', views.app_summary_example, name='app_summary_example'),
    path('main/diagram', views.diagram, name='diagram')

    # url(r'^products/$', 'viewname', name='urlname')

    # path('main/silly-test', views.silly_test, name='silly_test'),
    # path('main/silly-receive-json', views.silly_receive_json, name='silly_receive_json')
]
