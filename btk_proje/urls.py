"""
URL configuration for btk_proje project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# adminde resim dosyalarının görüntülenmesi için
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import home
from btk_proje import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')), # herhangi bir url belirtmeden home url gitmesi için
    path('home/', include('home.urls')),
    path('product/', include('product.urls')),
    path('user/', include('user.urls')),
    path('order/', include('order.urls')),

    # blog sayfaları
    path("hakkimizda", home.views.hakkimizda, name="hakkimizda"),
    path("referanslar", home.views.referanslar, name="referanslar"),
    path("iletisim", home.views.iletisim, name="iletisim"),

#     ckeditor için
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# resimlerin veya static dosyaların admin tarafında gösterilmesi için
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)