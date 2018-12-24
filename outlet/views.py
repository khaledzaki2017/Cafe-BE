from rest_framework.generics import ListAPIView, RetrieveAPIView


class ListOutletView(ListAPIView):
    """
    GET: Provides a list of all available outlets
    """

    from rest_framework.permissions import AllowAny
    from rest_framework.filters import SearchFilter

    from django_filters.rest_framework.backends import DjangoFilterBackend

    from .models import Outlet
    from .serializers import OutletSerializer

    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('city__name', 'building', 'area', 'name', 'pincode',
                     'unit')
    search_fields = ('city__name', 'building', 'area', 'name', 'pincode',
                     'unit')

    queryset = Outlet.objects.filter(is_active=True)
    serializer_class = OutletSerializer


class ListOutletProductView(ListAPIView):
    """
    get: Lists product available in a particular outlet

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from rest_framework.permissions import AllowAny
    from rest_framework.filters import SearchFilter

    from django_filters.rest_framework.backends import DjangoFilterBackend

    from .models import OutletProduct
    from .serializers import OutletProductSerializer

    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('product__name', 'product__category',
                     'product__category__name')
    search_fields = ('product__name', 'product__category__name', )

    queryset = OutletProduct.objects.filter(stock__gt=0)
    serializer_class = OutletProductSerializer

    def filter_queryset(self, queryset):
        from rest_framework.exceptions import NotFound

        from .models import Outlet

        queryset = super(ListOutletProductView, self).filter_queryset(
            queryset=queryset)
        outlet_id = self.kwargs.get('outlet__id')
        try:
            outlet = Outlet.objects.get(pk=outlet_id)
        except Outlet.DoesNotExist:
            raise NotFound("Invalid Outlet ID {} - object does not "
                           "exist.".format(outlet_id))
        else:
            return queryset.filter(outlet=outlet)


class RetrieveProductView(RetrieveAPIView):
    """
    get: List details of a specific product.
    """
    from rest_framework.permissions import AllowAny
    from rest_framework.filters import SearchFilter

    from django_filters.rest_framework.backends import DjangoFilterBackend

    from .models import OutletProduct
    from .serializers import OutletProductSerializer

    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, SearchFilter)

    queryset = OutletProduct.objects.filter(stock__gt=0)
    serializer_class = OutletProductSerializer

    lookup_field = 'product_id'

    def filter_queryset(self, queryset):
        from rest_framework.exceptions import NotFound

        from .models import Outlet

        queryset = super(RetrieveProductView, self).filter_queryset(
            queryset=queryset)
        outlet_id = self.kwargs.get('outlet_id')
        try:
            outlet = Outlet.objects.get(pk=outlet_id)
        except Outlet.DoesNotExist:
            raise NotFound("Invalid Outlet ID {} - object does not "
                           "exist.".format(outlet_id))
        else:
            return queryset.filter(outlet=outlet)


class ListManagerOutletView(ListAPIView):
    """
    get: Lists all the managers of an outlet.
    """
    from .permissions import OwnerOrManager
    from .filters import IsOwnerOrManagerFilterBackend
    from .models import Outlet
    from .serializers import OutletSerializer

    filter_backends = (IsOwnerOrManagerFilterBackend, )
    # permission_classes = (OwnerOrManager, )

    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer
