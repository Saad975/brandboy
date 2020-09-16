from django.contrib import admin
from .models import CompanyEmail, Company, Companylogo, CompanyWebLinks
# Register your models here.

admin.site.register(Company)
admin.site.register(CompanyEmail)
admin.site.register(CompanyWebLinks)
admin.site.register(Companylogo)