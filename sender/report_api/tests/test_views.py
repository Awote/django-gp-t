import os
import pytest
from django.urls import reverse
from adrf.test import AsyncAPIClient
from report_api.models import XlsxReport


@pytest.mark.django_db
class TestReportView:
    @pytest.fixture
    def api_client(self):
        return AsyncAPIClient()

    @pytest.fixture
    async def create_reports(self, db):
        await XlsxReport.objects.acreate(
            id="123",
            request_state="ДОБАВЛЕНИЕ",
            request_status="Обработка завершена",
            request_creation_date="2023-07-10 12:00:00",
            processing_end_date="2023-07-11 12:00:00",
            request_author="Автор",
            package_id="package_123",
        )

    @pytest.mark.asyncio
    async def test_post_report_success(self, api_client):
        file_path = os.path.join("report_api","tests","test_files","testing_data.xlsx")

        file = open(file_path, "rb")
        url = reverse("report")
        response = await api_client.post(url, {"file": file})
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_post_report_no_file(self, api_client):
        url = reverse("report")
        response = await api_client.post(url, {})
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_get_report_success(self, api_client, create_reports):
        url = reverse("report")
        response = await api_client.get(
            url,
            {"start_date": "10.07.2023 12:00:00", "end_date": "11.07.2023 12:00:00"},
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_report_invalid_dates(self, api_client):
        url = reverse("report")
        response = await api_client.get(url, {"start_date": "11.07.2023 12:00:00", "end_date": "10.07.2023 12:00:00"})
        assert response.status_code == 422
