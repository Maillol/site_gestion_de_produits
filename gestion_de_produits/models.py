from datetime import date

from django.utils.translation import ugettext_lazy as _
from django.db import models

from django.utils.translation import get_language


class TranslatedFieldMixin:
    """
    return any value of field defined in translated_fields 
    class attribute prefixed with current language.

    Ask description field return en_description field value
    if active language is 'en'.

    If field is empty value of default_lang is used.
    """

    default_lang = 'en'
    translated_fields = ('description',)

    def __getattr__(self, attr_name):
        if attr_name in type(self).translated_fields:
            lang = get_language()
            value = getattr(self, '{}_{}'.format(lang, attr_name))
            if not value:
                value = getattr(self, 'en_{}'.format(lang, attr_name))
            return value

        raise AttributeError("'{!r}' object has no attribute '{}'".
                             format(self, attr_name))


class Hazard(models.Model, TranslatedFieldMixin):
    """
    Hazard statements – standardized phrases which describe the nature of the
    hazard of a hazardous substance.
    """

    name = models.CharField(max_length=32, primary_key=True)
    fr_description = models.TextField(blank=True)
    en_description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Hazard'
        verbose_name_plural = 'Hazard'

    def __str__(self):
        return self.name


class Preventive(models.Model, TranslatedFieldMixin):
    name = models.CharField(max_length=32, primary_key=True)
    fr_description = models.TextField(blank=True)
    en_description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Preventive'
        verbose_name_plural = 'Preventive'

    def __str__(self):
        return self.name


class Pictogram(models.Model, TranslatedFieldMixin):
    """
    Pictograms of the international Globally Harmonized System of 
    Classification and Labelling of Chemicals (GHS).
    """

    translated_fields = ('description', 'note')

    name = models.CharField(max_length=5, primary_key=True)
    picture = models.ImageField(blank=True, null=True, upload_to='pictogram/')
    fr_description = models.TextField(blank=True)
    en_description = models.TextField(blank=True)
    fr_note = models.TextField(blank=True)
    en_note = models.TextField(blank=True)

    def __str__(self):
        return '{} - {}'.format(self.name, self.description)


class ProductClass(models.Model):
    """
    This model manage group of product.
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField('description', blank=True)

    class Meta:
        verbose_name = _('product group')
        verbose_name_plural = _('product groups')

    def __str__(self):
        return self.name


class ChemicalSubstanceName(models.Model):
    """
    A chemical substance can have several name.
    """
    name = models.CharField(_('name or synonym'), max_length=200)
    product_type = models.ForeignKey('ChemicalSubstance',
                                     models.CASCADE,
                                     related_name='names')

    def __str__(self):
        return self.name


class ChemicalSubstance(models.Model):
    """
    Chemical Substance CAS and formulas.
    """

    MENTIONS = (
        (0, _('Warning')),
        (1, _('Danger'))
    )

    cas = models.CharField(_('CAS number'), max_length=200, unique=True)
    chemical_formulas = models.CharField(
        _('Chemical formula'), max_length=2000)
    classification = models.ManyToManyField(ProductClass, blank=True)
    pictogram = models.ManyToManyField(Pictogram, blank=True)
    mention = models.IntegerField(_('mention'), choices=MENTIONS, default=0)

    class Meta:
        verbose_name = _('chemical substance')
        verbose_name_plural = _('chemical substances')

    def __str__(self):
        return '{} {}'.format(self.cas, self.names.first() or '-')


class ManipulationProtocol(models.Model):
    name = models.CharField(_('name'), max_length=200, unique=True)
    description = models.CharField(max_length=20000, blank=True)
    protocol = models.TextField(blank=True)

    class Meta:
        verbose_name = _('manipulation protocol')
        verbose_name_plural = _('manipulation protocols')

    def __str__(self):
        return self.name


class Storage(models.Model):
    storage_name = models.CharField(_('stockage'), max_length=200)
    laboratory_name = models.CharField(_('laboratory name'), max_length=200)
    floor = models.CharField(_('floor'), max_length=20)
    room = models.CharField(_('room'), max_length=40)
    storage_description = models.TextField(_('description'), blank=True)
    temperature_min = models.IntegerField(
        _('minimum temperature (Celsius degree)'))
    temperature_max = models.IntegerField(
        _('maximum temperature (Celsius degree)'))
    ventilated_cupboard = models.BooleanField(_('ventilated cupboard'))
    air = models.BooleanField(_("protect from air"))
    moisture = models.BooleanField(_("protect from moisture"))
    light = models.BooleanField(_("protect from light"))

    class Meta:
        unique_together = ('storage_name', 'laboratory_name', 'floor')
        verbose_name = _('stockage')
        verbose_name_plural = _('stockages')

    def __str__(self):
        return '{} ({} {} {})'.format(self.storage_name,
                                      self.laboratory_name,
                                      self.floor,
                                      self.room)


class PackagingProduct(models.Model):
    """
    Packaging of chemical substance.

    Each `Manufacturer` provide chemical severals packaging
    for chemical substance.
    """

    FORMS_CHOICES = (
        (0, _('liquid')),
        (1, _('tablet')),
        (2, _('capsule')),
        (3, _('powder'))
    )

    cas = models.ManyToManyField(ChemicalSubstance, blank=True)
    name = models.CharField(_('name'), max_length=200)
    manufacturer = models.ForeignKey(
        'Manufacturer', models.SET_NULL, blank=True, null=True)
    manufacturer_reference = models.CharField(
        _("manufacturer's reference"), max_length=200, blank=True)
    form = models.IntegerField(_('forms'), choices=FORMS_CHOICES, default=0)
    packaging = models.CharField(_('Packaging'), max_length=200, blank=True)
    incompatible_product = models.ManyToManyField(ProductClass, blank=True)

    fds = models.ForeignKey('FDS', models.SET_NULL, blank=True, null=True)
    fds_exact = models.BooleanField(_('is exact FDS'), default=False)

    temperature_min = models.IntegerField(
        _('minimum temperature (Celsius degree)'))
    temperature_max = models.IntegerField(
        _('maximum temperature (Celsius degree)'))
    ventilated_cupboard = models.BooleanField(_('ventilated cupboard'))
    air = models.BooleanField(_("air sensitive"))
    moisture = models.BooleanField(_("moisture sensitive"))
    light = models.BooleanField(_("light sensitive"))

    manipulation_protocol = models.ForeignKey(ManipulationProtocol, models.SET_NULL,
                                              blank=True, null=True)

    hazard = models.ManyToManyField(Hazard, blank=True)
    preventive = models.ManyToManyField(Preventive, blank=True)

    gloves = models.CharField(_('protective gloves'),
                              max_length=200, blank=True)
    protection = models.CharField(_('protection'), max_length=200, blank=True)
    target_organ = models.CharField(
        _('target organ'), max_length=200, blank=True)

    polluant = models.BooleanField(_('polluant'), default=False)
    isolate_can = models.BooleanField(_('isolate can'), default=False)
    specific_transport = models.BooleanField(
        _('specific transport'), default=False)

    class Meta:
        verbose_name = _('brand and packaging')
        verbose_name_plural = _('brands and packaging')

    def __str__(self):
        return '{} {} {}'.format(self.manufacturer or '',
                                 self.name or '',
                                 self.manufacturer_reference or '')


class StoredChemicalProduct(models.Model):
    """
    Chemical product bought and stored.
    """
    number = models.CharField("numéro d'inventaire", max_length=200,
                              blank=True, null=True, unique=True)
    packaging_product = models.ForeignKey(PackagingProduct, models.SET_NULL,
                                          blank=True, null=True)
    date_of_purchase = models.DateField(
        _("date of purchase"), blank=True, null=True)
    expiration_date = models.DateField(
        _("expiration date"), blank=True, null=True)
    storage_area = models.ForeignKey(
        Storage, models.SET_NULL, blank=True, null=True)
    done_date = models.DateField(_("done date"), blank=True, null=True)
    destroy_date = models.DateField(_("destroy date"), blank=True, null=True)

    class Meta:
        verbose_name = _('product purchased')
        verbose_name_plural = _('products purchased')

    def __str__(self):
        return '[{}] {}'.format(self.number, self.packaging_product.name)

    @property
    def is_expired(self):
        if self.expiration_date is None:
            return False
        return self.expiration_date < date.today()

    @property
    def is_safe_stored(self):
        if self.storage_area is None:
            return False

        if self.destroy_date is not None and self.destroy_date >= date.today():
            return True

        if self.packaging_product.ventilated_cupboard and not self.storage_area.ventilated_cupboard:
            return False

        if self.packaging_product.air and not self.storage_area.air:
            return False

        if self.packaging_product.moisture and not self.storage_area.moisture:
            return False

        if self.packaging_product.light and not self.storage_area.light:
            return False

        if self.packaging_product.temperature_max < self.storage_area.temperature_max:
            return False

        if self.packaging_product.temperature_min > self.storage_area.temperature_min:
            return False

        return True


class Manufacturer(models.Model):
    name = models.CharField(_('name'), max_length=200, unique=True)
    web_site = models.URLField(_('web site'), blank=True)
    phone = models.CharField(_('phone'), blank=True, max_length=60)
    email = models.EmailField(_('e-mail'), blank=True)

    class Meta:
        verbose_name = _('manufacturer')
        verbose_name_plural = _('manufacturers')

    def __str__(self):
        return self.name


class FDS(models.Model):
    """
    File Data Security

    Each Manufacturer provide a file containing
    security information on `PackagingProduct`.
    """
    name = models.CharField(_('name'), blank=True, max_length=200)
    reference = models.CharField(_('ref number'), blank=True, max_length=60)
    date = models.DateField(_('update date'), blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, models.SET_NULL,
                                     blank=True, null=True)
    file = models.FileField(blank=True, null=True, upload_to='fds-pdf/')

    class Meta:
        verbose_name = _('FDS')
        verbose_name_plural = _('FDS')

    def __str__(self):
        return '{} {}'.format(self.name, self.reference)
