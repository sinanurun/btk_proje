from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from home.models import Setting, UserProfile
from order.models import Order, OrderProduct
from product.models import Category, Comment, Product
from user.forms import UserUpdateForm, ProfileUpdateForm, ProductForm


def index(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    profile = UserProfile.objects.get(user_id=request.user.pk)
    context = {'setting': setting,
               'category': category,
               'profile': profile}
    return render(request, 'user_profile.html', context)


@login_required(login_url='/login')  # Check login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(
            instance=request.user.userprofile)  # "userprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')  # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html', {'form': form, 'category': category
                                                      })


@login_required(login_url='/login')  # Check login
def user_orders(request):
    category = Category.objects.all()
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'orders': orders,
               }
    return render(request, 'user_orders.html', context)


@login_required(login_url='/login')  # Check login
def user_orderdetail(request, id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url='/login')  # Check login
def user_order_product(request):
    category = Category.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
    context = {'category': category,
               'order_product': order_product,
               }
    return render(request, 'user_order_products.html', context)


@login_required(login_url='/login')  # Check login
def user_order_product_detail(request, id, oid):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id, user_id=current_user.id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url='/login')
def user_comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')  # Check login
def user_deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login')  # Check login
def user_products(request):
    category = Category.objects.all()
    current_user = request.user
    products = Product.objects.filter(user_id=current_user.id)
    setting = Setting.objects.get(pk=1)
    context = {'category': category,
               'setting': setting,
               'products': products,
               }
    return render(request, 'user_products.html', context)


@login_required(login_url='/login')  # Check login
def user_product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            current_user = request.user
            data = Product()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.detail = form.cleaned_data['detail']
            data.category = form.cleaned_data['category']
            data.price = form.cleaned_data['price']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.slug = form.cleaned_data['slug']
            data.save()
            messages.success(request, "Your Product is Added")
            return HttpResponseRedirect('/user/products')
        else:
            messages.success(request, "Productl Form Error : " + str(form.errors))
            return HttpResponseRedirect('/user/products')

    form = ProductForm
    category = Category.objects.all()
    current_user = request.user
    products = Product.objects.filter(user_id=current_user.id)
    setting = Setting.objects.get(pk=1)
    context = {'category': category,
               'products': products,
               'setting': setting,
               'form': form,
               }
    return render(request, 'user_products_add.html', context)


@login_required(login_url='/login')  # Check login
def user_delete_product(request, id):
    current_user = request.user
    Product.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Ürününüz deleted..')
    return HttpResponseRedirect('/user/products')


#
#
@login_required(login_url='/login')  # Check login
def user_update_product(request, id):
    pass
    otomobil = Otomobil.objects.get(id=id)
    if request.method == 'POST':
        form = OtomobilForm(request.POST, request.FILES, instance=otomobil)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Otomobil ise Updateded")
            return HttpResponseRedirect('/user/user_otomobils')
        else:
            messages.success(request, "Otomobil Form Error : " + str(form.errors))
            return HttpResponseRedirect('/user/user_otomobils')

    form = OtomobilForm(instance=otomobil)
    category = Category.objects.all()
    current_user = request.user
    otomobils = Otomobil.objects.filter(user_id=current_user.id)
    setting = Setting.objects.get(pk=1)
    sform1 = SearchForm1()
    context = {'category': category,
               'setting': setting,
               'otomobils': otomobils,
               'form': form,
               'sform1': sform1,
               }
    return render(request, 'user_otomobil_update.html', context)
