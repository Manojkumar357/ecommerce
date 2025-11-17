from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from store.models import Customer
from django.views import View
from django.http import JsonResponse


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None

        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['login_success'] = True  #  Set the flag

                #  Redirect back to the same page to trigger popup
                return redirect('/login?success=true')

            else:
                error_message = 'Invalid credentials!'
        else:
            error_message = 'Invalid credentials!'

        return render(request, 'login.html', {'error': error_message})


def logout(request):
    #  Remove only the customer session key
    if 'customer' in request.session:
        del request.session['customer']

    #  Set logout success flag (keep session alive)
    request.session['logout_success'] = True

    return redirect('homepage')


def clear_login_success(request):
    request.session.pop('login_success', None)
    return JsonResponse({'status': 'cleared'})
