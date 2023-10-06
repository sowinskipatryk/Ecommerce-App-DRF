from datetime import datetime
from decimal import Decimal
from django.core.mail import send_mail
from django.core.mail.backends.console import EmailBackend
from django.db.models import Sum
from django.utils import timezone
from permissions import IsClient, IsSeller
from products.models import Product
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderItem
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by('-date_ordered')
    permission_classes = [IsClient]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):

        serializer.validated_data['client'] = self.request.user
        due_date = serializer.validated_data['due_date'] = timezone.now() + timezone.timedelta(days=5)

        # Calculating summary price
        products_data = serializer.validated_data.get('items')
        summary_price = Decimal(0)
        for product_data in products_data:
            product = product_data['product']
            quantity = product_data['quantity']
            summary_price += product.price * quantity

        serializer.validated_data['summary_price'] = summary_price
        serializer.save()
    
        # Sending confirmation email
        subject = "Order Confirmation"
        message = f"Your order has been placed successfully.\nSummary Price: {summary_price}\nDue Date: {due_date.strftime('%d-%m-%Y %H:%M:%S')}"
        from_email = "shopping@ecommerce.com"
        recipient_list = [serializer.validated_data['client'].email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False, connection=EmailBackend())

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Adding user credentials to User instance
        user = request.user
        user.first_name = request.data['first_name'] or user.first_name
        user.last_name = request.data['last_name'] or user.last_name
        user.save()

        response_data = {
            "summary_price": serializer.validated_data["summary_price"],
            "due_date": serializer.validated_data["due_date"].strftime('%d-%m-%Y %H:%M:%S')
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class MostSoldProductsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSeller]

    def get(self, request):
        date_from_str = request.query_params.get('date_from')
        date_to_str = request.query_params.get('date_to')
        num_products = int(request.query_params.get('num_products', 10))

        date_from = datetime.strptime(date_from_str, '%Y-%m-%d')
        date_to = datetime.strptime(date_to_str, '%Y-%m-%d')

        most_sold_products = OrderItem.objects.filter(order__date_ordered__range=(date_from, date_to)) \
            .values('product') \
            .annotate(total_sold=Sum('quantity')) \
            .order_by('-total_sold')[:num_products]

        product_ids = [item['product'] for item in most_sold_products]
        products = Product.objects.filter(pk__in=product_ids)

        results = []
        for product in products:
            total_sold = next(item['total_sold'] for item in most_sold_products if item['product'] == product.id)
            results.append({
                'product_id': product.id,
                'product_name': product.name,
                'total_sold': total_sold,
            })

        return Response(results)
