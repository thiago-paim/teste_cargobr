# coding: utf-8

from rest_framework import generics
from rest_framework.response import Response

from .models import Entry
from .serializers import EntrySerializer, EntryFileSerializer


class ConsultNumberView(generics.ListAPIView):
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
    queryset = Entry.objects.all()
    serializer_class = EntryFileSerializer

    def post(self, request, *args, **kwargs):
        data_file = request.data['file']
        self.import_anatel_data(data_file)
        # Retornar

    def import_anatel_data(self, data_file):
        """
        Processa o arquivo enviado. Como o arquivo é bem grande, ele é lido em blocos para não ocupar toda a memória. Como todos os campos tem temanho fixo, não há necessidade de separar as palavras.
        """
        for chunk in data_file.chunks():
            lines = chunk.splitlines()

            for line in lines:

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

                entry.save()
