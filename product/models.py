from django.db import models
from django.utils.text import gettext_lazy as _

from decimal import Decimal

from drfaddons.models import CreateUpdateModel


class Category(CreateUpdateModel):
    """
    Represents product category in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from stock.models import UnitOfMeasurementMaster

    name = models.CharField(verbose_name=_("Category Name"), max_length=254,
                            unique=True)
    sku_prefix = models.CharField(verbose_name=_("SKU Prefix"), max_length=4,
                                  unique=True)
    hsn = models.CharField(verbose_name=_("HSN Code"), max_length=6)
    d_uom = models.ForeignKey(verbose_name=_("Default Unit of Measurement"),
                              to=UnitOfMeasurementMaster,
                              on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self)->str:
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Product(CreateUpdateModel):
    """
    Represents product's in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from stock.models import UnitOfMeasurementMaster

    from taxation.models import Tax

    name = models.CharField(verbose_name=_("Product Name"), max_length=254,
                            unique=True)
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT,
                                 verbose_name=_("Category"))
    price = models.DecimalField(verbose_name=_("Price"), max_digits=10,
                                decimal_places=3)
    interstate_tax = models.ManyToManyField(to=Tax, blank=True,
                                            verbose_name=_("Inter-State Tax"),
                                            related_name=_(
                                                "productinterstate"))
    instate_tax = models.ManyToManyField(to=Tax, blank=True,
                                         verbose_name=_("In-State Tax"),
                                         related_name=_("productinstate"))
    is_inclusive = models.BooleanField(verbose_name=_("Price inclusive of "
                                                      "Tax?"), default=True)
    sku = models.CharField(verbose_name=_("SKU Code"), max_length=28,
                           unique=True)
    o_hsn = models.CharField(verbose_name=_("Override HSN Code"),
                             max_length=6, null=True, blank=True)

    uom = models.ForeignKey(verbose_name=_("Unit of Measurement"),
                            to=UnitOfMeasurementMaster,
                            on_delete=models.PROTECT)

    @property
    def hsn(self)->str:
        """
        Provides hsn code of the product
        Category's HSN if HSN has not been override

        Returns
        -------
        str

        Author: Himanshu Shankar (https://himanshus.com)
        """
        return self.o_hsn or self.category.hsn

    @property
    def sku_code(self)->str:
        """
        Provides full SKU code by adding sku prefix from category

        Returns
        -------
        str

        Author: Himanshu Shankar (https://himanshus.com)
        """
        return self.category.sku_prefix + self.sku

    @property
    def total_interstate_tax(self)->Decimal:
        """
        Provides total interstate tax

        Returns
        -------
        Decimal

        Author: Himanshu Shankar (https://himanshus.com)
        """
        from django.db.models.aggregates import Sum

        total = self.interstate_tax.aggregate(Sum('percentage'))
        total = total.get('percentage__sum')

        if self.is_inclusive:
            total = self.price - (self.price / (1 + (total/100)))
        else:
            total = (total * self.price) / 100
        return round(total, 2)

    @property
    def total_instate_tax(self)->Decimal:
        """
        Returns total instate tax
        Returns
        -------
        Decimal

        Author: Himanshu Shankar (https://himanshus.com)
        """
        from django.db.models.aggregates import Sum

        total = self.instate_tax.aggregate(Sum('percentage'))
        total = total.get('percentage__sum')

        if self.is_inclusive:
            total = self.price - (self.price / (1 + (total/100)))
        else:
            total = (total * self.price) / 100
        return round(total, 2)

    def __str__(self)->str:
        return self.name

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class ProductImage(CreateUpdateModel):
    """
    Represents Product's images in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from .utils import product_image_upload

    name = models.CharField(verbose_name=_("Name"), max_length=154)
    product = models.ForeignKey(verbose_name=_("Product"), to=Product,
                                on_delete=models.PROTECT)
    image = models.ImageField(verbose_name=_("Image"),
                              upload_to=product_image_upload)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
