from django.contrib import messages
from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from home.models import Setting, ContactForm, ContactFormMessage
from product.models import Product, Category


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
def index(request):
    category = Category.objects.all()
    slider = Product.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,
               'page': 'home',
               'slider': slider,
               'category': category}
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
               'category':category}
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'Referanslar',
               'category':category}
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
               'category':category}
    return render(request, 'iletisim.html', context)



def categoryProducts(request, id, slug):
    urunKategori = Category.objects.get(pk= id)
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    urunler = list(Product.objects.filter(category_id=id))

    node = Category.objects.get(pk = id)
    children = Category.objects.add_related_count(node.get_children(), Product,
                                                  'category', 'product_counts')
    for dd in children:
        a = list(Product.objects.filter(category_id=dd.id))
        urunler.extend(a)

    print(urunler)

    context = {'setting': setting, 'page': 'Kategori',
               'category':category,
               'urunKategori':urunKategori,
               'urunler' : urunler}



    return render(request, 'urunler.html', context)