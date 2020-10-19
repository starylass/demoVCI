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
