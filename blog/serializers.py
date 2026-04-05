from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from auto_parts_store import settings
from blog.models import Article, Image
from blog.validators import ImageValidator


class ImageUploadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None,
        use_url=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png']),
            ImageValidator(max_file_size=settings.MAX_UPLOAD_SIZE)
        ]
    )

    class Meta:
        model = Image
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    images = ImageUploadSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        exclude = ('id', 'author',)
