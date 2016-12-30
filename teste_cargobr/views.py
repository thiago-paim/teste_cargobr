# coding: utf-8

import requests

from django.views.generic import FormView, TemplateView

from .forms import AnatelUploadForm, ConsultNumberForm


class HomeView(TemplateView):
    template_name = "client/index.html"


class ConsultView(FormView):
    """
    Envia requisição para a API para consultar localidade e operadora de um número enviado
    """
    template_name = "client/consult.html"
    form_class = ConsultNumberForm
    api_url = 'http://localhost:8000/api/consult'

    def form_valid(self, form):
        number = form.cleaned_data['number']
        r = requests.get(self.api_url + '?number=' + number)
        json = r.json()
        locality = json.get('results')[0]['locality']
        provider = json.get('results')[0]['provider']
        return self.render_to_response(self.get_context_data(form=form, locality=locality, provider=provider))


class UploadView(FormView):
    """
    Envia o arquivo para upload via API
    """
    template_name = "client/upload.html"
    form_class = AnatelUploadForm
    api_url = 'http://localhost:8000/api/upload'

    def form_valid(self, form):
        data_file = self.request.FILES['file']
        self.copy_uploaded_file(data_file)

        print('returning')
        return self.render_to_response(self.get_context_data(form=form))

    def copy_uploaded_file(self, f):
        print('copy_uploaded_file')
        with open('media/anatel_file.txt', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
