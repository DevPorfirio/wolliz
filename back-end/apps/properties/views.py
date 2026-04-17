import math

from django.core.cache import cache
from django.db.models import ExpressionWrapper, F, FloatField, Value
from django.db.models.functions import ACos, Cos, Radians, Sin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Property
from .serializers import PropertyCardSerializer, PropertyDetailSerializer


class PropertyPagination(PageNumberPagination):
    page_size             = 20
    page_size_query_param = "page_size"
    max_page_size         = 50


def _haversine_expr(lat: float, lng: float):
    R = 6371.0
    return ExpressionWrapper(
        Value(R) * ACos(
            Cos(Radians(Value(lat))) * Cos(Radians(F("latitude")))
            * Cos(Radians(F("longitude")) - Radians(Value(lng)))
            + Sin(Radians(Value(lat))) * Sin(Radians(F("latitude")))
        ),
        output_field=FloatField(),
    )


class PropertySearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            lat       = float(request.query_params["lat"])
            lng       = float(request.query_params["lng"])
            radius_km = float(request.query_params.get("radius_km", 10))
        except (KeyError, ValueError):
            return Response(
                {"detail": "Parâmetros lat e lng são obrigatórios e devem ser números."},
                status=400,
            )

        radius_km = min(radius_km, 100)
        page_num  = request.query_params.get("page", "1")
        cache_key = f"prop_search:{lat:.2f}:{lng:.2f}:{radius_km:.0f}:p{page_num}"

        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        # Bounding box pre-filter: uses B-tree index before computing Haversine
        lat_delta = radius_km / 111.0
        lng_delta = radius_km / (111.0 * math.cos(math.radians(lat)))

        qs = (
            Property.objects
            .filter(
                is_active=True,
                latitude__range=(lat - lat_delta, lat + lat_delta),
                longitude__range=(lng - lng_delta, lng + lng_delta),
            )
            .annotate(distance_km=_haversine_expr(lat, lng))
            .filter(distance_km__lte=radius_km)
            .prefetch_related("images")
            .order_by("distance_km")
        )

        paginator      = PropertyPagination()
        page           = paginator.paginate_queryset(qs, request)
        serializer     = PropertyCardSerializer(page, many=True)
        response_data  = paginator.get_paginated_response(serializer.data).data

        cache.set(cache_key, response_data, timeout=120)
        return Response(response_data)


class PropertyDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            prop = Property.objects.prefetch_related("images").get(pk=pk, is_active=True)
        except Property.DoesNotExist:
            return Response({"detail": "Imóvel não encontrado."}, status=404)
        serializer = PropertyDetailSerializer(prop)
        return Response(serializer.data)
