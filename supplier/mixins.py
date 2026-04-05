from catalog.models import AutoParts
from rest_framework.views import APIView


class GetObjectMixin:
    def get_object(self, pk):
        auto_part = AutoParts.objects.select_related('supplier').get(pk=pk)

        self.check_object_permissions(self.request, auto_part)
        return auto_part
