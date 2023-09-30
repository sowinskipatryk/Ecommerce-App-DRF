from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from permissions import IsSeller
from .filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer
from .utils import create_thumbnail


@permission_classes([])
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    ordering_fields = ('name', 'category', 'price')
    ordering = ('name',)

    def list(self, request, *args, **kwargs):
        ordering = request.query_params.get('ordering', 'name')

        if ordering not in ('name', 'category', 'price'):
            ordering = 'name'

        queryset = self.filter_queryset(self.get_queryset().order_by(ordering))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        product = serializer.save()
        create_thumbnail(product, self.request.data)

    def perform_update(self, serializer):
        product = serializer.save()
        create_thumbnail(product, self.request.data)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsSeller()]
        return super().get_permissions()