from django import forms
from .models import *
from bootstrap_modal_forms.forms import BSModalModelForm
from django.contrib.auth.forms import AuthenticationForm



class VCIModelForm(forms.ModelForm):
    subsidiary = forms.ModelChoiceField(queryset=Subsidiary.objects.all(),
                                        widget = forms.Select(attrs={'class': 'form-control'}),
                                        label = 'Wybierz filię',
                                        )
    distributor = forms.ModelChoiceField(queryset=Distributor.objects.all(),
                                        widget = forms.Select(attrs={'class': 'form-control'}),
                                        label = 'Wybierz dystrybutora',
                                        )

    class Meta:
        model = VCI
        labels = {
            'salesPersonDistributor': "Wybierz przedstawiciela"
        }
        fields = (
            'salesPersonDistributor',
            'lent',
            'workshop'
            )

        widgets = {
            'lent': forms.HiddenInput(),
            'workshop': forms.HiddenInput(),
            'salesPersonDistributor': forms.Select(attrs={'class': 'form-control'})
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['salesPersonDistributor'].queryset = SalesPersonDistributor.objects.all()
        self.fields['subsidiary'].queryset = Subsidiary.objects.all()


    field_order = ['distributor', 'subsidiary', 'salesPersonDistributor']


class VCIworkshopModelForm(forms.ModelForm):
    class Meta:
        model = VCI
        fields = (
            'salesPersonDistributor',
            'lent',
            'workshop',
            )
        widgets = {
            'lent': forms.HiddenInput(),
            'salesPersonDistributor': forms.HiddenInput(),
            'workshop': forms.Select(attrs={'class': 'form-control'})
        }


class VCIReturnModelForm(forms.ModelForm):
    class Meta:
        model = VCI
        fields = (
            'salesPersonDistributor',
            'lent',
            'workshop',
            )
        widgets = {
            'lent': forms.HiddenInput(),
            'salesPersonDistributor': forms.HiddenInput(),
            'workshop': forms.HiddenInput(),
        }

class NewWorkshopFrom(forms.ModelForm):
    class Meta:
        model = Workshop
        exclude = ['idWorkshop']



class NewSalesPersonDistributor(BSModalModelForm):
    class Meta:
        model = SalesPersonDistributor
        exclude = ('idSalesPersonDistributor',)

    def __init__(self, *args, **kwargs):
        super(NewSalesPersonDistributor, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



class NewSubsidiary(BSModalModelForm):
    class Meta:
        model = Subsidiary
        exclude = ('idSubsidiary',)

    def __init__(self, *args, **kwargs):
        super(NewSubsidiary, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Use format: "Distributor name - City or District"'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'type' :'text', 'id' : 'username'}))
    password = forms.CharField(label="Password", max_length=30,
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'type' :'password', 'id' : 'password'}))
