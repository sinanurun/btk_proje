from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    path('search/', views.search, name='search'),
    path('logout',views.logout_view, name= 'logout_view'),
    path('login', views.login_view, name='login_view'),
    path('signup', views.signup_view, name='signup_view'),
    path("category/<int:id>/<slug:slug>", views.categoryProducts, name="categoryProducts"),
    path("product_detail/<int:id>/<slug:slug>", views.productDetail, name="productDetail"),

    # ex: /polls/5/
    # path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    # path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    # path("<int:question_id>/vote/", views.vote, name="vote"),
]
