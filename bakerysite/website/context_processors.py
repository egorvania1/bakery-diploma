from storage.models import Order, OrderItem
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
            try:
                cart = Order.objects.get(customer=customer, is_ordered=False)
                cart_amount = OrderItem.objects.filter(order=cart).count()
            except:
                pass
            order_amount = Order.objects.filter(customer=customer, is_ordered=True).count()
            #cart_amount = Order.objects.exclude(creation_date=None).filter(customer=customer).count()
    
    return {
        'order_amount': order_amount,
        'cart_amount': cart_amount,
    }