import pytest
from report_api.serializers import CsvFileSerializer, XlsxReportQuery

@pytest.mark.django_db
def test_csv_file_serializer():
    data = {
        "id": "123",
        "request_state": "ДОБАВЛЕНИЕ",
        "request_status": "Обработка завершена",
        "request_creation_date": "10.07.2023 12:00:00",
        "processing_end_date": "11.07.2023 12:00:00",
        "request_author": "Автор",
        "package_id": "package_123"
    }
    serializer = CsvFileSerializer(data=data)
    assert serializer.is_valid()
    validated_data = serializer.validated_data
    assert validated_data["id"] == "123"
    assert validated_data["request_state"] == "ДОБАВЛЕНИЕ"

def test_xlsx_report_query_serializer_valid():
    data = {
        "start_date": "10.07.2023 12:00:00",
        "end_date": "11.07.2023 12:00:00"
    }
    serializer = XlsxReportQuery(data=data)
    assert serializer.is_valid()

def test_xlsx_report_query_serializer_invalid():
    data = {
        "start_date": "11.07.2023 12:00:00",
        "end_date": "10.07.2023 12:00:00"
    }
    serializer = XlsxReportQuery(data=data)
    assert not serializer.is_valid()