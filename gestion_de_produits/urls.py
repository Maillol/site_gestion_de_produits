from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    url(r'^$', login_required(views.ListProduct.as_view()), name='index'),
    url(r'^(?P<product_id>[0-9]+)/$',
        login_required(views.detail), name='detail'),
    url(r'^set_to_done/(?P<product_id>[0-9]+)/$', login_required(
        views.set_product_to_done), name='set_to_done'),
    url(r'^packaging/(?P<pk>[0-9]+)/$',
        login_required(views.PackagingProductDetailView.as_view()),
        name='packaging-product-detail'),
]
