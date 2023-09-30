from django.core.mail import send_mail
from django.core.mail.backends.console import EmailBackend
from django.utils import timezone
from django.db.models import Sum, F
from permissions import IsClient
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsClient]

    # def perform_create(self, serializer):
    #     due_date = timezone.now() + timezone.timedelta(days=5)
    #     serializer.save(due_date=due_date)
    #
    #     subject = "Order Confirmation"
    #     message = f"Your order has been placed successfully.\nSummary Price: {summary_price}\nDue Date: {due_date}"
    #     from_email = "your@email.com"
    #     recipient_list = [serializer.validated_data['email']]
    #     send_mail(subject, message, from_email, recipient_list, fail_silently=False, connection=EmailBackend())
    #
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #
    #     current_datetime = timezone.now()
    #     instance.due_date = current_datetime + timezone.timedelta(days=5)
    #
    #     summary_price = instance.orderitem_set.aggregate(
    #         total_price=Sum(F('product__price') * F('quantity'))
    #     )['total_price'] or 0.00
    #
    #     instance.summary_price = summary_price
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
