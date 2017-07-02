from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView, ListView

from .forms import SearchProductForm
from .models import StoredChemicalProduct, PackagingProduct, Storage


def detail(request, product_id):
    product = get_object_or_404(StoredChemicalProduct, pk=product_id)
    return render(request, 'gestion_de_produits/detail.html', {'product': product})


class PackagingProductDetailView(DetailView):
    model = PackagingProduct


class ListProduct(ListView):

    model = StoredChemicalProduct
    template_name = 'gestion_de_produits/index.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        storages = [(storage.id, str(storage))
                    for storage
                    in Storage.objects.all()]

        self.form = SearchProductForm(storages, self.request.GET)
        if not self.request.user.is_superuser:
            self.form.destroy_for_superuser_fields()

        def use_to_filter(value):
            if isinstance(value, str):
                if value == '' or value.isspace():
                    return False
            if value is None:
                return False
            if value == []:
                return False
            return True

        self.form.is_valid()
        query_parameters = {k: v for k, v
                            in self.form.cleaned_data.items()
                            if use_to_filter(v)}

        return super().get_queryset().filter(**query_parameters). \
            order_by('number')

    def render_to_response(self, context, **response_kwargs):
        context['form'] = self.form  # SearchProductForm(self.request.GET)
        return super().render_to_response(context, **response_kwargs)


def set_product_to_done(request, product_id):
    if not request.user.is_authenticated():
        raise PermissionDenied()

    product = get_object_or_404(StoredChemicalProduct, pk=product_id)
    set_to_done = product.done_date is None
    if set_to_done:
        product.done_date = datetime.now()
        product.save()

    return redirect('detail', product_id=product_id)
