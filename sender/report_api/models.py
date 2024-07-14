from django.db import models
from asgiref.sync import sync_to_async
from django.db.models import Count, Q

xlsx_report_columns = [
    "Номер заявки",
    "Состояние заявки",
    "Статус заявки",
    "Автор заявки",
    "Дата создания заявки",
    "Дата окончания обработки",
    "ID пакета",
]
xlslx_report_convert_column = {
    "Номер заявки": "id",
    "Состояние заявки": "request_state",
    "Статус заявки": "request_status",
    "Автор заявки": "request_author",
    "Дата создания заявки": "request_creation_date",
    "Дата окончания обработки": "processing_end_date",
    "ID пакета": "package_id",
}


class XlsxReport(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    request_state = models.CharField(max_length=50)
    request_status = models.TextField()
    request_creation_date = models.DateTimeField()
    processing_end_date = models.DateTimeField(null=True, blank=True)
    request_author = models.TextField()
    package_id = models.CharField(max_length=50)


async def get_report_data(start_date=None, end_date=None):
    # Создание базового запроса без фильтра по датам
    queryset = XlsxReport.objects.all()

    # Если даты указаны, применяем фильтр по диапазону дат
    if start_date and end_date:
        queryset = queryset.filter(request_creation_date__range=(start_date, end_date))

    # Выполнение агрегатного запроса асинхронно
    report_data = await sync_to_async(queryset.aggregate)(
        total_rows=Count("id"),
        count_duplicate=Count("id", filter=Q(request_state="ДУБЛИКАТ")),
        count_addition=Count("id", filter=Q(request_state="ДОБАВЛЕНИЕ")),
        count_expansion=Count("id", filter=Q(request_state="РАСШИРЕНИЕ")),
        count_processing_completed=Count(
            "id", filter=Q(request_status="Обработка завершена")
        ),
        count_return_for_revision=Count(
            "id", filter=Q(request_status="Возвращение на уточнение")
        ),
        count_sent_for_processing=Count(
            "id", filter=Q(request_status="Отправлена в обработку")
        ),
        unique_package_ids=Count("package_id", distinct=True),
        unique_request_authors=Count("request_author", distinct=True),
    )
    return report_data
