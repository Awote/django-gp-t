from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from .serializers import CsvFileSerializer
import pandas as pd
from .producer import ProducerReportSave

produser_report_save = ProducerReportSave()

class UploadCsvView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Парсинг CSV файла при помощи pandas
        try:
            df = pd.read_excel(file)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Пример: преобразование данных в JSON
        data = df.to_dict(orient='records')
        produser_report_save.publish("user_created_method",data)
        pass
        # Отправка каждого сообщения в RabbitMQ

        
        return Response({"status": "Messages processed"}, status=status.HTTP_201_CREATED)