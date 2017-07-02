from django.contrib import admin
from .models import Pictogram, ChemicalSubstance, PackagingProduct, \
    StoredChemicalProduct, Manufacturer, ManipulationProtocol, \
    Storage, ProductClass, Hazard, Preventive, FDS, ChemicalSubstanceName


class PackagingProductModelAdmin(admin.ModelAdmin):

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "cas":
            kwargs["queryset"] = ChemicalSubstance.objects.order_by('cas')
        return super().formfield_for_manytomany(db_field, request, **kwargs)


class ChemicalSubstanceNameInline(admin.TabularInline):
    model = ChemicalSubstanceName


class ChemicalSubstanceModelAdmin(admin.ModelAdmin):

    inlines = [
        ChemicalSubstanceNameInline,
    ]


admin.site.register(FDS)
admin.site.register(Hazard)
admin.site.register(Preventive)
admin.site.register(Pictogram)

admin.site.register(Manufacturer)
admin.site.register(ManipulationProtocol)
admin.site.register(Storage)
admin.site.register(ProductClass)

admin.site.register(PackagingProduct, PackagingProductModelAdmin)
admin.site.register(ChemicalSubstance, ChemicalSubstanceModelAdmin)
admin.site.register(StoredChemicalProduct)
