from django.db import models


# Create your models here.

class Company(models.Model):
    domain = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.domain


class CompanyEmail(models.Model):
    email = models.CharField(max_length=255, null=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.email


class CompanyWebLinks(models.Model):
    links = models.CharField(max_length=255, null=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.links


class Companylogo(models.Model):
    logo = models.CharField(max_length=255, null=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.logo
