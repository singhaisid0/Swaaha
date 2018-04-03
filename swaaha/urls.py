"""swaaha URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""



from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login, name="login"),
    url(r'^loginSubmit/', views.loginSubmit),
    url(r'^logout/', views.logout, name="logout"),
    url(r'^adminsInfo/', views.adminsInfo, name="adminsInfo"),
    url(r'^addAdmin/', views.addAdmin),
    url(r'^customersInfo/', views.customersInfo, name="customersInfo"),
    url(r'^updateCustomer/(?P<username>\D+)/', views.updateCustomer),
    url(r'^addCustomer/', views.addCustomer),
    url(r'^addCustomerInfo/', views.updateInfo),
    url(r'^wasteInfo/', views.wasteInfo, name="wasteInfo"),
    url(r'^operatorsInfo/', views.operatorsInfo, name="operatorsInfo"),
    url(r'^addOperator/', views.addOperator),
    url(r'^driversInfo/', views.driversInfo, name="driversInfo"),
    url(r'^addDriver/', views.addDriver),
    url(r'^clustersInfo/', views.clustersInfo, name="clustersInfo"),
    url(r'^addCluster/', views.addCluster),
    url(r'^filterWaste/', views.filterWaste),
    url(r'^filterWasteMonth/', views.filterWasteMonth),
    url(r'^chemical/', views.chemical, name="checmical"),
    url(r'^filterChemical/', views.filterChemical),
    url(r'^filterChemicalMonth/', views.filterChemicalMonth),
    url(r'^/downloadFilter/', views.downloadWaste, name="downloadFilter"),
    url(r'^/downloadFilterMonth/', views.downloadWasteMonth, name="downloadFilterMonth"),
    url(r'^/downloadChemical/', views.downloadChemical, name="downloadChemical"),
    url(r'^/downloadChemicalMonth/', views.downloadChemicalMonth, name="downloadChemicalMonth"),
]
