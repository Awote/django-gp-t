import pytest
from report_api.models import XlsxReport

@pytest.mark.django_db
def test_create_xlsx_report():
    report = XlsxReport.objects.create(
        id="123",
        request_state="ДОБАВЛЕНИЕ",
        request_status="Обработка завершена",
        request_creation_date="2023-07-10 12:00:00",
        processing_end_date="2023-07-11 12:00:00",
        request_author="Автор",
        package_id="package_123"
    )
    assert report.id == "123"
    assert report.request_state == "ДОБАВЛЕНИЕ"
    assert report.request_status == "Обработка завершена"
    assert report.request_author == "Автор"
    assert report.package_id == "package_123"