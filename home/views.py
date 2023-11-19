from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from home.forms import SearchForm, LoginForm, SignUpForm
from home.models import Setting, ContactForm, ContactFormMessage, UserProfileForm, UserProfile
from product.models import Product, Category, Images, Comment


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
def index(request):
    urunler = Product.objects.order_by('?')[:8]  # rastgele urunler getirmek içni
    category = Category.objects.all()
    slider = Product.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,
               'page': 'home',
               'slider': slider,
               'category': category,
               'urunler': urunler}
    return render(request, 'index.html', context)


# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)
# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)
# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)
def hakkimizda(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,
               'page': 'Hakkımızda',
               'category': category}
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'Referanslar',
               'category': category}
    return render(request, 'referanslar.html', context)


def iletisim(request):
    category = Category.objects.all()
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(request, "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)

    form = ContactForm
    context = {'setting': setting,
               'form': form,
               'category': category}
    return render(request, 'iletisim.html', context)


def categoryProducts(request, id, slug):
    urunKategori = Category.objects.get(pk=id)
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    urunler = list(Product.objects.filter(category_id=id))

    node = Category.objects.get(pk=id)
    children = Category.objects.add_related_count(node.get_children(), Product,
                                                  'category', 'product_counts')
    for dd in children:
        a = list(Product.objects.filter(category_id=dd.id))
        urunler.extend(a)

    context = {'setting': setting, 'page': 'Kategori',
               'category': category,
               'urunKategori': urunKategori,
               'urunler': urunler}
    return render(request, 'kategori_urunler.html', context)


def productDetail(request, id, slug):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    urun = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    # print(request.get_full_path())
    # print(request.get_host())
    # print(request.build_absolute_uri())
    comments = Comment.objects.filter(product_id=id)
    context = {'setting': setting,
               'page': 'Urun',
               'category': category,
               'urun': urun,
               'images': images,
               'comments': comments}
    return render(request, 'urun_detay.html', context)


def search(request):
    print(33)
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        print(35)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            print(query)
            # catid = form.cleaned_data['catid']
            # if catid==0:
            #     products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            # else:
            #     products = Product.objects.filter(title__icontains=query,category_id=catid)

            products = Product.objects.filter(title__icontains=query)
            category = Category.objects.all()
            setting = Setting.objects.get(pk = 1)
            print(36)
            context = {'urunler': products, 'query':query,
                       'category': category,
                       'setting' : setting}
            return render(request, 'product_search.html', context)

    return HttpResponseRedirect('/')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    category = Category.objects.all()
    if request.method == 'POST':  # check post
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Başarılı şekilde oturum açtınız {}".format(user.username))
                return HttpResponseRedirect('/login')
            else:
                messages.warning(request, "Girilen Bilgiler Hatalı Tekrar Deneyiniz {}".format(username))
                return HttpResponseRedirect('/login')

    setting = Setting.objects.get(pk=1)

    form = LoginForm
    context = {'setting': setting,
               'form': form,
               'category': category}
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.png"
            data.save()
            # sonradan eklenecek kısım
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/signup')


    form = SignUpForm()
    category = Category.objects.all()
    setting = Setting.objects.all()
    context = {'category': category,
               'form': form,
               'setting':setting
               }
    return render(request, 'signup_form.html', context)

def userProfile_view(request):
    category = Category.objects.all()
    if request.method == 'POST':  # check post
        form = UserProfileForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(request, "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/user_profile')

    setting = Setting.objects.get(pk=1)

    form = UserProfileForm
    context = {'setting': setting,
               'form': form,
               'category': category}
    return render(request, 'userprofile.html', context)