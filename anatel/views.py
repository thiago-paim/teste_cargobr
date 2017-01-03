# coding: utf-8

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR

from .models import Entry
from .serializers import EntrySerializer, EntryFileSerializer


class ConsultNumberView(generics.ListAPIView):
    """
    Recebe um número como parâmetro GET, busca o Entry relacionado e retorna a operadora e a localidade do número
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    def get_queryset(self):
        number = self.request.query_params.get('number', None)
        prefix = number[0:6]
        sufix = number[6:]
        if number is not None:
            queryset = Entry.objects.filter(prefix=prefix, initial_interval_number__lte=sufix, final_interval_number__gte=sufix)
        return queryset


class UploadAPIView(generics.CreateAPIView):
    """
    Recebe um arquivo .txt contendo os dados CNL e popula o banco de dados
    """
    queryset = Entry.objects.all()
    serializer_class = EntryFileSerializer
    local_file_path = 'media/anatel_file.txt'

    def post(self, request, *args, **kwargs):
        try:
            data_file = request.data['file']
            self.copy_uploaded_file(data_file)
            self.create_entries()

            content = {'message': 'Upload realizado com sucesso'}
            return Response(content, status=HTTP_201_CREATED)
        except Exception as e:
            content = {'message': e}
            return Response(content, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def copy_uploaded_file(self, f):
        """
        Cria uma cópia local do arquivo para que ele possa ser lido aos poucos enquanto se popula o banco
        """
        with open(self.local_file_path, 'wb') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def create_entries(self):
        """
        Processa o arquivo enviado. Como o arquivo é grande, ele é lido linha por linha.
        """
        with open(self.local_file_path, 'r', encoding='latin1') as data_file:
            entries = []
            for line in data_file:

                entry = Entry(
                    uf=line[0:2].strip(),
                    cnl=line[2:6].strip(),
                    cnl_code=line[6:11].strip(),
                    locality=line[11:61].strip(),
                    municipality=line[61:111].strip(),
                    tax_area_code=line[111:116].strip(),
                    prefix=line[116:123].strip(),
                    provider=line[123:153].strip(),
                    initial_interval_number=line[153:157].strip(),
                    final_interval_number=line[157:161].strip(),
                    latitude=line[161:169].strip(),
                    hemisphere=line[169:174].strip(),
                    longitude=line[174:182].strip(),
                    local_area_cnl=line[182:188].strip(),
                )
                entries.append(entry)

            Entry.objects.bulk_create(entries, batch_size=100)
