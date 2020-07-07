from rest_framework import generics
from rest_framework.response import Response
from deals.models import Deal
from deals.serializers import DealSerializer, DealBaseSerializer
from django.contrib import messages
import io, csv


class FileUploadView(generics.CreateAPIView):
    serializer_class = DealSerializer
    queryset = Deal.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data['file']

        if not file.name.endswith('.csv'):
            messages.error(request, 'Это не CSV файл, попробуйте загрузить файл с расширением CSV.')
            return Response('Error, Desc: TypeError - в процессе обработки файла произошла ошибка.')

        decoded_file = file.read().decode('UTF-8')

        io_string = io.StringIO(decoded_file)
        next(io_string)

        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            _, created = Deal.objects.update_or_create(
                customer=column[0],
                item=column[1],
                total=column[2],
                quantity=column[3],
                date=column[4]
            )

        return Response('OK - файл был обработан без ошибок')

    def get(self, request, format=None):
        """
        Не успел реализовать правильный вывод get запроса,
        Если честно, немного не понял, что именно нужно...
        """
        deals = Deal.objects.all()[:5]
        serializer = DealBaseSerializer(deals, many=True)
        return Response({"deals": serializer.data})
