from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='user/login.html', authentication_form = LoginForm, redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('VCI/', VCIListView.as_view(), name='VCI'),
    path('Distributor/', DistributorListView.as_view(), name='Distributors'),
    path('SalesPersonDelphi/', SalesPersonDelphiListView.as_view(), name='salesPersonDelphi'),
    path('VCIsalesPersonDelphi/<pk>', VCIsalesPersonDelphiListView.as_view(), name='VCIsalesPersonDelphi'),
    path('Subsidiary/<pk>', SubsidiaryListView.as_view(), name='Subsidiaries'),
    path('SalesPersonDistributor/<pk>', SalesPersonDistributorListView.as_view(), name='SalesPersonDistributor'),
    path('SalesPersonDistributorHistory/<pk>', VCIHistoryListView.as_view(), name='SalesPersonDistributorHistory'),
    path('VCIcreate/', VCICreateView.as_view(), name='VCIcreate'),
    path('VCIUpdate/<pk>', VCIUpdateView.as_view(), name='VCIUpdate'),
    path('VCIUpdateReturn/<pk>', VCIUpdateReturnView.as_view(), name='VCIUpdateReturn'),
    path('VCIworkshopUpdate/<pk>', VCIworkshopUpdateView.as_view(), name='VCIworkshopUpdate'),
    path('ajax/load-workshops/', load_workshops, name='ajax_load_workshops'),
    path('ajax/load-subsidiaries/', load_subsidiaries, name='ajax_load_subsiriaies'),
    path('ajax/load-salesPersonsDistributor/', load_salesPersonDistributor, name='ajax_load_salesPersonsDistributor'),
    path('ajax/load-subsidiaryAddressDelivery/', load_subsidiaryAddressDelivery, name='ajax_load_subsidiaryAddressDelivery'),
    path('ajax/load-salesPersonsDistributorContact/', load_salesPersonDistributorContact, name='ajax_load_salesPersonsDistributorContact'),
    path('ajax/load_workshopAddressDelivery/', load_workshopAddressDelivery, name='ajax_load_workshopAddressDelivery'),
    path('filia/', redirect_logic_func, name='get_data'),
    path('createsalesperson/<pk>', NewSalesPersonDistributor.as_view(), name='new_sales_person_distibutor'),
    path('createsubsidiary/<pk>', NewSubsidiary.as_view(), name='new_subsidiary'),


    #password resert and change
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='user/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='user/password_change_done.html'), name='password_change_done')
    ]
