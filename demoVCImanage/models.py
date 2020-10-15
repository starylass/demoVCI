from django.db import models
from simple_history.models import HistoricalRecords


class SalesPersonDelphi(models.Model):
    idSalesPerson = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.IntegerField()
    street = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    postal = models.CharField(max_length=200, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name + " " + self.surname



class Distributor(models.Model):
    idDistributor = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    postal = models.CharField(max_length=200)
    history = HistoricalRecords()
    salesPersonDelphi = models.ForeignKey(SalesPersonDelphi, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Subsidiary(models.Model):
    idSubsidiary = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    postal = models.CharField(max_length=200)
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.name



class SalesPersonDistributor(models.Model):
    idSalesPersonDistributor = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.IntegerField()
    subsidiary = models.ForeignKey(Subsidiary, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.name + " " + self.surname + " - " + self.subsidiary.name


class Workshop(models.Model):
    idWorkshop = models.AutoField(primary_key=True)
    workshopName = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    postal = models.CharField(max_length=200)
    contacName = models.CharField(max_length=200)
    contactSurname = models.CharField(max_length=200)
    phone = models.IntegerField()
    email = models.EmailField()
    history = HistoricalRecords()

    def __str__(self):
        return self.workshopName



class VCI(models.Model):
    VCInumber = models.IntegerField(primary_key=True)
    Car = models.BooleanField(default=True)
    Truck = models.BooleanField(default=True)
    salesPersonDelphi = models.ForeignKey(SalesPersonDelphi, null=True, on_delete=models.SET_NULL)
    salesPersonDistributor = models.ForeignKey(SalesPersonDistributor, null=True, on_delete=models.SET_NULL, blank=True)
    workshop = models.ForeignKey(Workshop, null=True, on_delete=models.SET_NULL, blank=True)
    lent = models.BooleanField(default=True)
    lendDate = models.DateField(blank=True, null=True)
    returnDate = models.DateField(blank=True, null=True)
    issues = models.CharField(max_length=2000, default="Brak problemów")
    history = HistoricalRecords()

    def __str__(self):
        return str(self.VCInumber)
