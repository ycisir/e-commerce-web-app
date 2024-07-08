from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.views import View
from app.models import Customer, Product, Cart, OrderPlaced
from app.forms import SignupForm, LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm, CustomerProfileForm
from django.views.generic.edit import FormView, UpdateView
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404

class HomeView(View):
    def get(self, request):
        items = 0
        top_wears = Product.objects.filter(category='TW')
        bottom_wears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        if request.user.is_authenticated:
            items = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'top_wears':top_wears, 'bottom_wears':bottom_wears, 'mobiles':mobiles, 'laptops':laptops, 'items':items})

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        in_cart = False
        if request.user.is_authenticated:
            items = len(Cart.objects.filter(user=request.user))
            in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            return render(request, 'app/product-detail.html', {'product':product, 'in_cart':in_cart, 'items':items})
        # print(in_cart)
        return render(request, 'app/product-detail.html', {'product':product, 'in_cart':in_cart})


class MyLoginView(SuccessMessageMixin, LoginView):
    template_name= 'app/login.html'
    authentication_form = LoginForm
    success_message = 'You were successfully logged in'


class MyLogoutView(SuccessMessageMixin, LogoutView):
    next_page = '/accounts/login/'
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, 'Successfully logged out.')
        return response


class SignupView(FormView):
    template_name = 'app/signup.html'
    form_class = SignupForm
    success_url = '/accounts/login/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'User created successfully!')
        return super().form_valid(form)


class MyPasswordChangeView(PasswordChangeView):
    items = 0
    template_name = 'app/password-change.html'
    form_class = MyPasswordChangeForm
    success_url = '/profile/'

    def get_queryset(self):
        items = len(Cart.objects.filter(user=self.request.user))
        return items
    

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been changed.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.get_queryset()
        return context
    
    
class MyPasswordResetView(PasswordResetView):
    template_name = 'app/password-reset.html'
    form_class = MyPasswordResetForm

class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'app/password-reset-done.html'

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'app/password-reset-confirm.html'
    form_class = MySetPasswordForm

class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'app/password-reset-complete.html'


@method_decorator(login_required, name='dispatch')
class ProfileView(FormView):
    template_name = 'app/profile.html'
    form_class = CustomerProfileForm
    success_url = '/address/'

    def get_queryset(self):
        items = len(Cart.objects.filter(user=self.request.user))
        return items

    def form_valid(self, form):
        user = self.request.user
        name = form.cleaned_data['name']
        locality = form.cleaned_data['locality']
        city = form.cleaned_data['city']
        state = form.cleaned_data['state']
        zipcode = form.cleaned_data['zipcode']
        update = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
        update.save()
        messages.success(self.request, 'Your details added successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'btn-primary'
        context['items'] = self.get_queryset()
        return context
    

class AddressView(TemplateView):
    template_name = 'app/address.html'
    def get_queryset(self):
        address = Customer.objects.filter(user=self.request.user)
        items = len(Cart.objects.filter(user=self.request.user))
        return[address, items]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_address'] = self.get_queryset()[0]
        context['active'] = 'btn-primary'
        context['items'] = self.get_queryset()[1]
        return context
    
    
@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    def get(self, request):
        user = request.user
        product_id = request.GET.get('product_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        return redirect('/cart')


@method_decorator(login_required, name='dispatch')
class ShowCartView(View):
    def get(self, request):
        items = 0
        if request.user.is_authenticated:
            user = request.user
            cart = Cart.objects.filter(user=user)
            # print(cart)
            amount = 0.0
            shipping_amount = 70.0
            total_amount = 0.0
            cart_product = [p for p in Cart.objects.all() if p.user == user]
            # print(cart_product)
            
            items = len(Cart.objects.filter(user=request.user))

            if cart_product:
                for p in cart_product:
                    temp_amount = (p.quantity * p.product.discount_price)
                    amount += temp_amount
                    total_amount = amount + shipping_amount
                return render(request, 'app/cart.html', {'carts':cart, 'total_amount':total_amount, 'amount':amount, 'items':items})
            else:
                return render(request, 'app/empty-cart.html', {'items':items})   

class BuyNowView(TemplateView):
    template_name = 'app/buy-now.html'

class PaymentSuccessView(View):
    def get(self, request):
        if request.user.is_authenticated:
            items = len(Cart.objects.filter(user=request.user))
            
        return render(request, 'app/payment-success.html', {'items':items})


@method_decorator(login_required, name='dispatch')
class OrdersView(TemplateView):
    template_name = 'app/orders.html'

    def get_queryset(self):
        order_placed = OrderPlaced.objects.filter(user=self.request.user)
        items = len(Cart.objects.filter(user=self.request.user))
        return[order_placed, items]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_placed'] = self.get_queryset()[0]
        context['items'] = self.get_queryset()[1]
        return context

@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, request):
        user = request.user
        address = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discount_price)
                amount += temp_amount
            
            total_amount = amount + shipping_amount

        items = 0
        if request.user.is_authenticated:
            items = len(Cart.objects.filter(user=request.user))

        return render(request, 'app/checkout.html', {'address':address, 'total_amount':total_amount, 'cart_items':cart_items, 'items':items})


class PaymentDoneView(View):
    def get(self, request):
        user = request.user
        customer_id = request.GET.get('customer_id')
        customer = Customer.objects.get(id=customer_id)
        cart = Cart.objects.filter(user=user)
        
        for item in cart:
            ordered = OrderPlaced(user=user, customer=customer, product=item.product, quantity=item.quantity)
            ordered.save()
            item.delete()
            messages.success(request, f'Your order has been placed!')
        return redirect('orders')


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Apple' or data == 'OnePlus' or data == 'Samsung' or data == 'Moto':
        mobiles = Product.objects.filter(category='M').filter(brand=data)

    items = 0
    if request.user.is_authenticated:
            items = len(Cart.objects.filter(user=request.user))
    
    return render(request, 'app/mobile.html', {'mobiles':mobiles, 'items':items})


def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Apple' or data == 'Lenovo' or data == 'Dell':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'under':
        laptops = Product.objects.filter(category='L').filter(discount_price__lt=500)


    items = 0
    if request.user.is_authenticated:
            items = len(Cart.objects.filter(user=request.user))
    
    return render(request, 'app/laptop.html', {'laptops':laptops, 'items':items})


def top_wear(request, data=None):
    if data == None:
        top_wears = Product.objects.filter(category='TW')
    elif data == 'under':
        top_wears = Product.objects.filter(category='TW').filter(discount_price__lt=15)

    items = 0
    if request.user.is_authenticated:
            items = len(Cart.objects.filter(user=request.user))
    
    return render(request, 'app/top-wear.html', {'top_wears':top_wears, 'items':items})


def bottom_wear(request, data=None):
    if data == None:
        bottom_wears = Product.objects.filter(category='BW')
    elif data == 'Wrangler' or data == 'Levis' or data == 'Lee':
        bottom_wears = Product.objects.filter(category='BW').filter(brand=data)
    elif data == 'under':
        bottom_wears = Product.objects.filter(category='BW').filter(discount_price__lt=50)

    
    items = 0
    if request.user.is_authenticated:
            items = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/bottom-wear.html', {'bottom_wears':bottom_wears, 'items':items})


def plus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount += temp_amount

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'total_amount':amount + shipping_amount
        }
        return JsonResponse(data)
        


def minus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount += temp_amount

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'total_amount':amount + shipping_amount
        }
        return JsonResponse(data)
        

def remove_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        # print(cart_product)
        msg = ''
        if not cart_product:
            msg = 'Your cart is empty!'

        items = 0
        if request.user.is_authenticated:
            items = len(Cart.objects.filter(user=request.user))

        # print(msg)

        
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount += temp_amount

        data = {

            'amount':amount,
            'total_amount':amount + shipping_amount,
            'msg':msg,
            'items':items,
        }
        return JsonResponse(data)
    

class SearchView(ListView):
    model = Product
    template_name = 'app/search-results.html'
    ordering = ['id']
    paginate_by = 10
    paginate_orphans = 1

    # msg = 'No results found!'
    # 
    def get_queryset(self):
        if 'q' in self.request.GET:
            q = self.request.GET['q']
            data = Product.objects.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
                | Q(brand__icontains=q) | Q(category__icontains=q)
                | Q(discount_price__icontains=q) | Q(selling_price__icontains=q)
                )
        else:
            data = Product.objects.all()

        return data


    def paginate_queryset(self, queryset, page_size):
        try:
            return super(SearchView, self).paginate_queryset(queryset, page_size)
        except Http404:
            self.kwargs['page'] = 1
            return super(SearchView, self).paginate_queryset(queryset, page_size)
        
    def cart_queryset(self, request):
        items = 0
        if request.user.is_authenticated:
            items = len(Cart.objects.filter(user=request.user))
        
        return items
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.cart_queryset(self.request)
        return context
    

def custom_404(request):
    return render(request, 'app/404.html', {}, status=404)