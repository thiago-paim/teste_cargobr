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
        try:
            r = requests.get(self.api_url + '?number=' + number)
            json = r.json()
            locality = json.get('results')[0]['locality']
            provider = json.get('results')[0]['provider']
            return self.render_to_response(self.get_context_data(form=form, locality=locality, provider=provider))
        except:
            return self.render_to_response(self.get_context_data(form=form, locality='Número não encontrado', provider='Número não encontrado'))


class UploadView(FormView):
    """
    Envia o arquivo para upload via API
    """
    template_name = "client/upload.html"
    form_class = AnatelUploadForm
    api_url = 'http://localhost:8000/api/upload/'
    local_file_path = 'media/anatel_file.txt'

    def form_valid(self, form):
        data_file = self.request.FILES['file']
        try:
            files = {'file': data_file}
            r = requests.post(self.api_url, files=files)
            json = r.json()
            message = json.get('message')
        except Exception as e:
            message = 'Erro ao processar o arquivo: {}'.format(e)

        return self.render_to_response(self.get_context_data(form=form, message=message))
