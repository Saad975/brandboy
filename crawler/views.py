from django.shortcuts import render
from django.views.generic import FormView
from .form import DoaminName
from .models import Company, CompanyEmail, Companylogo, CompanyWebLinks
from bs4 import BeautifulSoup
import requests
import re
import urllib.parse
import tldextract
import datetime


# Create your views here.
class HomeView(FormView):
    template_name = 'crawler/home.html'
    form_class = DoaminName

    def post(self, request, *args, **kwargs):

        domain = self.get_form()

        search = domain.data['post']

        date_from = datetime.datetime.now() - datetime.timedelta(days=1)

        if Company.objects.filter(domain=search, created_at__gt=date_from).count() == 0:

            response = requests.get(search)

            data = response.text

            soup = BeautifulSoup(data, features='html.parser')

            text_of_webpage = soup.get_text()

            domain_name = tldextract.extract(str(search))

            email_in_string = re.findall(r'[a-zA-Z]+[\w\-.]+@[\w-]+\.[\w.-]+[a-zA-Z]', text_of_webpage)

            email = soup.find_all('a', {'href': re.compile(r'[a-zA-Z]+[\w\-.]+@[\w-]+\.[\w.-]+[a-zA-Z]')})

            all_links = soup.find_all('a')

            logos = soup.find_all('img')

            favicons = soup.find_all('link')

            context = {
                'logo': '',
                'firstimg': '',
                'favicon': '',
                'curr_web_links': [],
                'email': []
            }

            favicon = []
            logo = []

            for link in all_links:
                if link.has_attr('href'):
                    if domain_name.domain in link['href'] and 'https://' in link['href'] and link['href'] not in \
                            context['curr_web_links']:
                        print(link['href'])
                        context['curr_web_links'].append(link['href'])

            for img in logos:
                if img.has_attr('data-orig-src'):
                    if 'logo' in img['data-orig-src']:
                        logo = img
                        break
                elif 'logo' in img['src']:
                    logo = img
                    break

            for fav in favicons:
                if 'fav' in fav['href']:
                    favicon = fav
                    break

            if logo:
                if logo.has_attr('data-orig-src'):
                    context['logo'] = urllib.parse.urljoin(search, logo['data-orig-src'])
                else:
                    context['logo'] = urllib.parse.urljoin(search, logo['src'])

                context['firstimg'] = urllib.parse.urljoin(search, logos[0]['src'])

            if favicon:
                context['favicon'] = urllib.parse.urljoin(search, favicon['href'])

            print('LOGO :: ' + context['logo'] + ' ' + context['favicon'] + ' ' + context['firstimg'])

            if email or email_in_string:
                if email:
                    for e in email:
                        context['email'].append(e['href'])

                if email_in_string:
                    for e in email_in_string:
                        context['email'].append(e)

            for link in context['curr_web_links']:
                print(context['email'])
                try:
                    child_response = requests.get(link)

                    child_data = child_response.text

                    child_soup = BeautifulSoup(child_data, features='html.parser')

                    child_links_text_of_webpage = child_soup.get_text()

                    child_email_in_string = re.findall(r'[a-zA-Z]+[\w\-.]+@[\w-]+\.[\w.-]+[a-zA-Z]',
                                                       child_links_text_of_webpage)

                    child_email = child_soup.find_all('a', {
                        'href': re.compile(r'[a-zA-Z]+[\w\-.]+@[\w-]+\.[\w.-]+[a-zA-Z]')})

                    if child_email or child_email_in_string:
                        if child_email:
                            for e in child_email:
                                if context['email']:
                                    for em in context['email']:
                                        if e not in em:
                                            context['email'].append(e['href'])
                                else:
                                    context['email'].append(e['href'])

                        if child_email_in_string:
                            for e in child_email_in_string:
                                if e not in context['email']:
                                    if context['email']:
                                        for em in context['email']:
                                            if e not in em:
                                                context['email'].append(e)
                                    else:
                                        context['email'].append(e)

                except:

                    pass

            if not context['email']:
                context['email'].append('Data Not Avaliable')

            company = Company(domain=search)

            company.save()

            if logo:
                c_logo = context['logo']
            elif favicon:
                c_logo = context['favicon']
            else:
                c_logo = context['firstimg']

            context['logo'] = c_logo

            company_logo = Companylogo(logo=c_logo, company=company)

            company_logo.save()

            for e in context['email']:
                company_email = CompanyEmail(email=e, company=company)

                company_email.save()

            for link in context['curr_web_links']:
                company_weblinks = CompanyWebLinks(links=link, company=company)

                company_weblinks.save()

        else:
            company = Company.objects.filter(domain=search).order_by('-id')[0]
            logo = company.companylogo_set.all().first()
            email = company.companyemail_set.all()
            context = {
                'logo': logo,
                'email': email
            }

        return self.render_to_response(context)
