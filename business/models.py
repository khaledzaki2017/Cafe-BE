from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


class Business(CreateUpdateModel):
    """
    Represents business i.e. entity owning outlet

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from django.contrib.auth import get_user_model

    from location.models import State

    from OfficeCafe.variables import BUSINESS_TYPE_CHOICES, PRIVATE_LIMITED

    name = models.CharField(verbose_name=_("Business Name"), unique=True,
                            max_length=254)
    business_type = models.CharField(verbose_name=_("Business Type"),
                                     max_length=5,
                                     choices=BUSINESS_TYPE_CHOICES,
                                     default=PRIVATE_LIMITED)
    owners = models.ManyToManyField(verbose_name=_("Owners"),
                                    related_name=_("owns_businesses"),
                                    to=get_user_model(), blank=True)
    managers = models.ManyToManyField(verbose_name=_("Managers"),
                                      related_name=_("manages_businesses"),
                                      to=get_user_model(), blank=True)
    gst = models.CharField(verbose_name=_("GST Number"), blank=True,
                           null=True, max_length=15)
    pan = models.CharField(verbose_name=_("PAN Number"), unique=True,
                           max_length=10)
    state = models.ForeignKey(verbose_name=_("Home State"), to=State,
                              on_delete=models.PROTECT)
    fssai = models.CharField(verbose_name=_("FSSAI License Number"),
                             max_length=150, null=True, blank=True)
    is_active = models.BooleanField(verbose_name=_("Is Active?"),
                                    default=True)

    @property
    def legal_name(self):
        return self.name + ' ' + self.get_business_type_display()

    def clean_fields(self, exclude=None):
        """
        Validates GST Number
        Parameters
        ----------
        exclude

        Raises
        ------
        ValidationError

        Author: Himanshu Shankar (https://himanshus.com)
        """

        from django.core.exceptions import ValidationError

        error = {}
        if 'gst' not in exclude and self.gst:
            pass
        # TODO: Validate GST Number
        # TODO: Validate PAN Number
        if len(error) > 0:
            raise ValidationError(error)

        return super(Business, self).clean_fields(exclude=exclude)

    def is_owner(self, user):
        if user.is_authenticated:
            return user in self.owners or user.is_superuser
        return False

    def has_permission(self, user):
        if user.is_authenticated:
            return self.is_owner(user=user) or user in self.owners
        return False

    def __str__(self):
        return self.legal_name

    class Meta:
        verbose_name = _("Business")
        verbose_name_plural = _("Businesses")


class BusinessDocument(CreateUpdateModel):
    """
    Represents documents related to a business

    Author: Himanshu Shankar
    """

    from OfficeCafe.variables import PENDING, DOCUMENT_STATUS_CHOICES
    from OfficeCafe.variables import BUSINESS_DOCUMENT_CHOICES

    business = models.ForeignKey(to=Business, on_delete=models.PROTECT,
                                 verbose_name=_("Business"))
    doc_type = models.CharField(verbose_name=_("Document Type"),
                                choices=BUSINESS_DOCUMENT_CHOICES,
                                max_length=5)
    value = models.CharField(verbose_name=_("Doc Value"), null=True,
                             blank=True, max_length=254)
    status = models.CharField(verbose_name=_("Verification Status"),
                              choices=DOCUMENT_STATUS_CHOICES,
                              default=PENDING, max_length=5)

    def __str__(self):
        return "{business}'s {doc}".format(business=self.business.name,
                                           doc=self.get_doc_type_display())

    def is_owner(self, user):
        return self.business.has_permission(user=user)

    def has_permission(self, user):
        return self.business.has_permission(user=user)

    class Meta:
        verbose_name = _("Business Document")
        verbose_name_plural = _("Business Documents")
