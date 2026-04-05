from django.template.defaultfilters import filesizeformat
from rest_framework import serializers


class ImageValidator:
    def __init__(self, max_file_size):
        self.max_file_size = max_file_size

    def __call__(self, value):
        if value.size > self.max_file_size:
            raise serializers.ValidationError(
                f"Максимальный размер файла {filesizeformat(self.max_file_size)}. "
                f"Ваш файл: {filesizeformat(value.size)}."
            )
