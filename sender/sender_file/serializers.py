from rest_framework import serializers

class CsvFileSerializer(serializers.Serializer):
    
    request_number = serializers.CharField(max_length=20)
    request_state = serializers.CharField(max_length=50)
    agreement = serializers.CharField(max_length=100)
    request_status = serializers.CharField(max_length=100)
    request_author = serializers.CharField(max_length=100)
    file_name = serializers.CharField(max_length=100)
    request_creation_date = serializers.DateTimeField()
    processing_end_date = serializers.DateTimeField(allow_null=True)
    time_to_process = serializers.CharField(max_length=100, allow_blank=True)
    initial_full_name = serializers.CharField(max_length=255)
    processed_full_name = serializers.CharField(max_length=255, allow_blank=True)
    material_code = serializers.CharField(max_length=50, allow_blank=True)
    similar_materials = serializers.CharField(allow_blank=True)
    bei = serializers.CharField(max_length=20, allow_blank=True)
    ntd = serializers.CharField(max_length=50, allow_blank=True)
    package_id = serializers.CharField(max_length=50)
