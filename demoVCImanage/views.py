from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import *
from .forms import *
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse
#import win32com.client as win32
from bootstrap_modal_forms.generic import BSModalCreateView
from django.urls import reverse
from datetime import date, timedelta
from django.utils.html import strip_tags
import os
import pathlib
from django.template.loader import get_template
from django.contrib.auth.models import User



class VCIListView(ListView):
    model = VCI
    context_object_name = 'VCI'
    template_name = 'VCI.html'



class VCIHistoryListView(ListView):
    model = VCI
    context_object_name = 'VCIhistory'
    template_name = 'VCIhistory.html'

    def get_queryset(self):
        return VCI.history.filter(salesPersonDistributor = self.kwargs['pk'])


class DistributorListView(ListView):
    model = Distributor
    context_object_name = 'distributor'
    template_name = 'distributor_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DistributorListView, self).get_context_data(*args, **kwargs)
        salesPersonDistributorWithVCI = list(VCI.objects.exclude(salesPersonDistributor__isnull=True).values_list('salesPersonDistributor', flat=True))
        salesPersonDistributorWithVCI_sub = list(SalesPersonDistributor.objects.filter(idSalesPersonDistributor__in=salesPersonDistributorWithVCI).values_list('subsidiary', flat=True))
        distWithVCI = list(Subsidiary.objects.filter(idSubsidiary__in=salesPersonDistributorWithVCI_sub).values_list('distributor', flat=True))
        distributors = Distributor.objects.all()

        context.update({
            'distWithVCI': distWithVCI,
            'distributors': distributors
        })
        return context


class SubsidiaryListView(ListView):
    model = Subsidiary
    context_object_name = 'subsidiary'
    template_name = 'subsidiaries_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SubsidiaryListView, self).get_context_data(*args, **kwargs)
        salesPersonDistributorWithVCI = list(VCI.objects.exclude(salesPersonDistributor__isnull=True).values_list('salesPersonDistributor', flat=True))
        salesPersonDistributor_sub = list(SalesPersonDistributor.objects.filter(idSalesPersonDistributor__in=salesPersonDistributorWithVCI).values_list('subsidiary', flat=True))
        subsidiary_of_dist = Subsidiary.objects.filter(distributor=self.kwargs['pk'])

        context.update({
            'salesPersonDistributor_sub': salesPersonDistributor_sub,
            'subsidiary_of_dist': subsidiary_of_dist
        })
        return context



class SalesPersonDelphiListView(ListView):
    model = SalesPersonDelphi
    context_object_name = 'salesPersonDelphi'
    template_name = 'salesPersonDelphi_list.html'



class VCIsalesPersonDelphiListView(ListView):
    model = VCI
    context_object_name = 'VCI'
    template_name = 'VCI.html'

    def get_queryset(self):
        return VCI.objects.filter(salesPersonDelphi=self.kwargs['pk'])



class SalesPersonDistributorListView(ListView):
    model = SalesPersonDistributor
    context_object_name = 'salesPersonDistributor'
    template_name = 'salesPersonDistributor_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SalesPersonDistributorListView, self).get_context_data(*args, **kwargs)
        salesPersonDistributor = SalesPersonDistributor.objects.filter(subsidiary=self.kwargs['pk'])
        vcilent = list(VCI.objects.all().values_list('salesPersonDistributor', flat=True))

        context.update({
            'salesPersonDistributor': salesPersonDistributor,
            'vcilent': vcilent
        })
        return context
    #def get_queryset(self):
        #return SalesPersonDistributor.objects.filter(subsidiary=self.kwargs['pk'])



class VCICreateView(CreateView):
    model = Distributor
    context_object_name = 'VCIcreate'
    form_class = VCIModelForm
    template_name = 'VCIcreate.html'



class NewSalesPersonDistributor(BSModalCreateView):
    template_name = 'newsalespersondistributor.html'
    form_class = NewSalesPersonDistributor

    #def form_valid(self, form):
    #    self.plus_context['you_want_context'] = value
    #    return super(UploadTest, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NewSalesPersonDistributor, self).get_context_data(**kwargs)
        context['VCInumber'] = self.kwargs['pk']
        return context

    def get_success_url(self):
         VCInumber = self.kwargs['pk']
         return reverse_lazy('VCIUpdate', kwargs={'pk': VCInumber})

    #def get_success_url(self):
        #  VCInumber = self.kwargs['pk']
         # return reverse_lazy('VCIUpdate', kwargs={'pk': VCInumber})



class NewSubsidiary(BSModalCreateView):
    template_name = 'newsubsidiary.html'
    form_class = NewSubsidiary

    def get_context_data(self, **kwargs):
        context = super(NewSubsidiary, self).get_context_data(**kwargs)
        context['VCInumber'] = self.kwargs['pk']
        return context

    def get_success_url(self):
         VCInumber = self.kwargs['pk']
         return reverse_lazy('VCIUpdate', kwargs={'pk': VCInumber})

"""

class VCIUpdateView(UpdateView):
    model = VCI
    context_object_name = 'VCIUpdate'
    form_class = VCIModelForm
    template_name = 'VCIupdatedist.html'
    success_url = "/VCI"

    #def form_valid(self, form):
    #    lent = form.fields['lent']
    #    if request.method == 'POST':
    #        form = TestModelForm(request.POST)
    #        if form.is_valid():
    #            lent = True
    #            form.save()
    #            return super(VCIUpdateView, self).form_valid(form)

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.lent = True
            obj.lendDate = date.today()
            try:
                hist = obj.history.first()
                hist.returnDate = date.today()
                hist.save()
            except AttributeError:
                pass
            return super(VCIUpdateView, self).form_valid(form)
    #def form_valid(self, form):
    #    form.save()
        #send_mail('temat', data, 'delphi', ['demovcimanage@gmail.com'])
    #    super(VCIUpdateView, self).form_valid(form)
    #    return redirect_logic_func(self.request)

"""
def _get_form(request, formcls, prefix, **kwargs):
    data = request.POST if prefix in request.POST else None
    return formcls(data, prefix=prefix)


class VCIworkshopUpdateView(UpdateView):
    model = VCI
    form_class = VCIworkshopModelForm
    form_class2 = NewWorkshopFrom
    template_name = 'VCIUpdateworkshop.html'


    def get(self, request, *args, **kwargs):
        vci = self.kwargs['pk']
        VCIset = VCI.objects.get(VCInumber = vci)
        return self.render_to_response({
            'vci': vci,
            'form': self.form_class(prefix='formv'),
            'form2': self.form_class2(prefix='formw'),
            'VCIUpdate': VCIset
        })

    def post(self, request, *args, **kwargs):
        vci = self.kwargs['pk']
        VCIset = VCI.objects.get(VCInumber = vci)
        salesPersonDelphi = VCIset.salesPersonDelphi

        form = _get_form(request, VCIworkshopModelForm, 'formv')
        form2 = _get_form(request, NewWorkshopFrom, 'formw')
        if form.is_bound and form.is_valid():
            obj = form.save(commit=False)
            obj.VCInumber = vci
            obj.salesPersonDelphi = salesPersonDelphi
            obj.lent = True
            obj.lendDate = date.today()
            try:
                hist = obj.history.first()
                hist.returnDate = date.today()
                hist.save()
            except AttributeError:
                pass
            obj.save()
            return redirect('/VCI', vci)
        elif form2.is_bound and form2.is_valid():
            form2.save()
            return redirect('VCIworkshopUpdate', vci)



class VCIUpdateReturnView(UpdateView):
    model = VCI
    form_class = VCIReturnModelForm
    context_object_name = 'VCIUpdate'
    template_name = 'VCIUpdateReturn.html'
    success_url = "/VCI"

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.lent = False
            obj.lendDate = None
            obj.salesPersonDistributor = None
            obj.workshop = None
            try:
                hist = obj.history.first()
                hist.returnDate = date.today()
                hist.save()
            except AttributeError:
                pass
            return super(VCIUpdateReturnView, self).form_valid(form)



#def redirect_logic_func(request):
#    import pythoncom
#    pythoncom.CoInitialize()
#    filia = request.POST.get('data')
#    outlook = win32.Dispatch('outlook.application')
#    mail = outlook.CreateItem(0)
#    mail.To = ""
#    mail.Subject = ""
#    mail.HtmlBody = filia
#    mail.Display(True)



def redirect_logic_func(request):
    #filia = request.POST.get('data')
    #print(filia)
    #send_mail('temat', filia, 'delphi', ['grzegorz.dziadkowiec@gmail.com'])
    #return HttpResponse(filia)
    vci = request.POST.get('vci')
    filia = request.POST.get('data')
    current_user = request.user.email
    print(current_user)
    with open('demoVCImanage//templates//email.html', 'w', encoding='utf-8') as f:
        f.write(filia)
    rendered = render_to_string('emailhead.html') + render_to_string('email.html')
    send_mail('Wysyłka testera: ' + vci,'', 'delphi', [current_user], html_message=rendered)
#    def get(self, request, form, **kwargs):
#        cos1 = kwargs.get('pk')
#        obj = VCI.objects.filter(VCInumber=cos1)
#        if form.is_valid():
#            cos = str(obj)
#            send_mail('temat', cos, 'delphi', ['demovcimanage@gmail.com'])
#    return redirect('CI')



def load_subsidiaries(request):
    distributor_id = request.GET.get('distributor')
    subsidiaries = Subsidiary.objects.filter(distributor_id=distributor_id)
    return render(request, 'subsidiary_drop_down.html', {'subsidiaries': subsidiaries})



def load_salesPersonDistributor(request):
    subsidiary_id = request.GET.get('subsidiary')
    salesPersonsDistributor = SalesPersonDistributor.objects.filter(subsidiary_id=subsidiary_id)
    return render(request, 'salesPersonDistributor_drop_down.html', {'salesPersonsDistributor': salesPersonsDistributor})



def load_subsidiaryAddressDelivery(request):
    subsidiary_id = request.GET.get('subsidiary')
    subsidiary_address = Subsidiary.objects.filter(idSubsidiary=subsidiary_id)
    return render(request, 'subsidiary_address_delivery.html', {'subsidiary_address': subsidiary_address})



def load_salesPersonDistributorContact(request):
    salesPersonDistributor = request.GET.get('salesPersonDistributor')
    salesPersonDistributor_contact = SalesPersonDistributor.objects.filter(idSalesPersonDistributor=salesPersonDistributor)
    return render(request, 'salesPersonDistributor_contact.html', {'salesPersonDistributor_contact': salesPersonDistributor_contact})


def load_workshopAddressDelivery(request):
    workshop = request.GET.get('workshop')
    workshopDelivery = Workshop.objects.filter(idWorkshop = workshop)
    return render(request, 'workshopDelivery.html', {'workshopDelivery': workshopDelivery})


def load_workshops(request):
    workshops = Workshop.objects.all()
    return render(request, 'workshop_drop_down.html', {'workshops': workshops})



def index(request):
    return render(request, 'index.html')



class NewSubsidiary(BSModalCreateView):
    template_name = 'newsubsidiary.html'
    form_class = NewSubsidiary

    def get_context_data(self, **kwargs):
        context = super(NewSubsidiary, self).get_context_data(**kwargs)
        context['VCInumber'] = self.kwargs['pk']
        return context

    def get_success_url(self):
         VCInumber = self.kwargs['pk']
         return reverse_lazy('VCIUpdate', kwargs={'pk': VCInumber})



class VCIUpdateView(UpdateView):
    model = VCI
    form_class = VCIModelForm
    form_class2 = NewSubsidiary
    template_name = 'VCIupdatedist.html'
    success_url = "/VCI"

    def get(self, request, *args, **kwargs):
        vci = self.kwargs['pk']
        VCIUpdate = VCI.objects.get(VCInumber = vci)
        return self.render_to_response({
            'vci': vci,
            'form': self.form_class(prefix='formv'),
            'form2': self.form_class2(prefix='formw'),
            'VCIUpdate': VCIUpdate
        })

    def post(self, request, *args, **kwargs):
        vci = self.kwargs['pk']
        VCIUpdate = VCI.objects.get(VCInumber = vci)
        salesPersonDelphi = VCIset.salesPersonDelphi

        form = _get_form(request, VCIModelForm, 'formv')
        form2 = _get_form(request, NewSubsidiary, 'formw')
        if form.is_bound and form.is_valid():
            obj = form.save(commit=False)
            obj.VCInumber = vci
            obj.salesPersonDelphi = salesPersonDelphi
            obj.lent = True
            obj.lendDate = date.today()
            try:
                hist = obj.history.first()
                hist.returnDate = date.today()
                hist.save()
            except AttributeError:
                pass
            obj.save()
            return redirect('/VCI', vci)
        elif form2.is_bound and form2.is_valid():
            form2.save()
            return redirect('VCIUpdate', vci)

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.lent = True
            obj.lendDate = date.today()
            try:
                hist = obj.history.first()
                hist.returnDate = date.today()
                hist.save()
            except AttributeError:
                pass
            return super(VCIUpdateView, self).form_valid(form)
