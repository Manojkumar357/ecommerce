from django.shortcuts import render, redirect
from django.views import View
from store.models import Products

class Cart(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        product_ids = cart.keys()
        products = Products.get_products_by_id(product_ids)
        cart_items = []   # ✅ change variable name
        total_price = 0

        for product in products:
            quantity = cart[str(product.id)]
            total = product.price * quantity
            total_price += total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'get_total_price': total
            })

        return render(request, 'cart.html', {
            'cart_items': cart_items,    # ✅ match template variable
            'total_price': total_price
        })



def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})

    # If the product exists in the cart, remove it
    if str(item_id) in cart:
        del cart[str(item_id)]

    # Save the updated cart
    request.session['cart'] = cart

    return redirect('cart')


