from storage.models import Order
from accounts.models import Customer

def custom_processor(request):
    order_amount = 0
    cart_amount = 0

    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
        except:
            customer = None
        if customer:
            order_amount = Order.objects.filter(customer=customer, creation_date=None).count()
            cart_amount = Order.objects.exclude(creation_date=None).filter(customer=customer).count()
    
    return {
        'order_amount': order_amount,
        'cart_amount': cart_amount,
    }