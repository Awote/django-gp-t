from adrf.views import APIView
from django.http import HttpResponse
import pandas as pd
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.report_generate import ExcelReportGenerator
from .serializers import CsvFileSerializer, XlsxReportQuery
from utils.wrappers import run_in_thread_pool
from utils.async_file import ReadCsv
from .models import get_report_data, xlsx_report_columns, xlslx_report_convert_column

# produser_report_save = ProducerReportSave()


class ReportView(APIView):
    parser_classes = [MultiPartParser]
    csv_reader = ReadCsv()

    @swagger_auto_schema(
        operation_description="Upload a CSV file",
        manual_parameters=[
            openapi.Parameter(
                "file",
                openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="XLSX to be uploaded",
            ),
        ],
        responses={
            201: openapi.Response(description="CSV file successfully processed"),
            400: openapi.Response(description="Invalid input"),
            422: openapi.Response(description="Unprocessable entity"),
        },
    )
    async def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            df = await self.csv_reader.read_file(file)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        missing_columns = [col for col in xlsx_report_columns if col not in df.columns]
        if missing_columns:
            return Response(
                {"error": f"Missing required fields: {', '.join(missing_columns)}"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        df = df[xlsx_report_columns]

        df.rename(
            columns=xlslx_report_convert_column,
            inplace=True,
        )

        df["request_state"] = df["request_state"].str.replace(
            r"^Дубликат.*", "ДУБЛИКАТ", regex=True
        )

        data = df.to_dict(orient="records")
        csv_file_serializer = CsvFileSerializer(data=data, many=True)
        is_valid = await run_in_thread_pool(csv_file_serializer.is_valid)
        if is_valid:
            await csv_file_serializer.asave()
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": csv_file_serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

    @swagger_auto_schema(
        operation_description="Generate an Excel report",
        manual_parameters=[
            openapi.Parameter(
                "start_date",
                openapi.IN_QUERY,
                description="Start date for the report",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "end_date",
                openapi.IN_QUERY,
                description="End date for the report",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Excel report generated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_FILE, description="Generated Excel report"
                ),
            ),
            422: openapi.Response(description="Invalid date range"),
        },
    )
    async def get(self, request):
        xlsx_report_query_serializer = XlsxReportQuery(data=request.query_params.dict())
        if xlsx_report_query_serializer.is_valid():
            pass
        else:
            return Response(
                {"error": xlsx_report_query_serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        start_date = xlsx_report_query_serializer.validated_data["start_date"]
        end_date = xlsx_report_query_serializer.validated_data["end_date"]
        report_data_period = await get_report_data(start_date, end_date)
        report_data_all_time = await get_report_data()

        def replace_zeros_with_dash(data):
            return {k: (v if v != 0 else "-") for k, v in data.items()}

        report_data_period = replace_zeros_with_dash(report_data_period)
        report_data_all_time = replace_zeros_with_dash(report_data_all_time)
        data = {
            "Название": [
                "Загруженных заявок",
                "Дубли",
                "На создание",
                "На расширение",
                "Обработка завершена",
                "Возвращена на уточнение",
                "Отправлена в обработку",
                "Пакетов",
                "Пользователей",
            ],
            "За указанный период": [
                report_data_period["total_rows"],
                report_data_period["count_duplicate"],
                report_data_period["count_addition"],
                report_data_period["count_expansion"],
                report_data_period["count_processing_completed"],
                report_data_period["count_return_for_revision"],
                report_data_period["count_sent_for_processing"],
                report_data_period["unique_package_ids"],
                report_data_period["unique_request_authors"],
            ],
            "За все время": [
                report_data_all_time["total_rows"],
                report_data_all_time["count_duplicate"],
                report_data_all_time["count_addition"],
                report_data_all_time["count_expansion"],
                report_data_all_time["count_processing_completed"],
                report_data_all_time["count_return_for_revision"],
                report_data_all_time["count_sent_for_processing"],
                report_data_all_time["unique_package_ids"],
                report_data_all_time["unique_request_authors"],
            ],
        }

        excel_report = ExcelReportGenerator(pd.DataFrame(data))
        excel_report.add_header()
        excel_report.add_data()
        excel_report.apply_borders_and_alignment()
        excel_report.adjust_column_widths()
        response_data = await run_in_thread_pool(excel_report.prepare_file)

        response = HttpResponse(
            response_data,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=report.xlsx"
        return response
