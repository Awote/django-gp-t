from adrf.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from .models import XlsxReport


class CsvFileSerializer(ModelSerializer):
    request_creation_date = serializers.DateTimeField(
        input_formats=["%d.%m.%Y %H:%M:%S"]
    )
    processing_end_date = serializers.DateTimeField(
        input_formats=["%d.%m.%Y %H:%M:%S"], allow_null=True
    )

    class Meta:
        model = XlsxReport
        fields = "__all__"


class XlsxReportQuery(Serializer):
    start_date = serializers.DateTimeField(input_formats=["%d.%m.%Y %H:%M:%S"])
    end_date = serializers.DateTimeField(input_formats=["%d.%m.%Y %H:%M:%S"])

    def validate(self, data):
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date >= end_date:
            raise serializers.ValidationError(
                "Start date must be earlier than end date."
            )

        return data
