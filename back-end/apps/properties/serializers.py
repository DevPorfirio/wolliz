from django.conf import settings
from rest_framework import serializers
from .models import Property, PropertyImage


def _public_url(image_field):
    """
    Returns the image URL with the internal MinIO hostname rewritten to the
    publicly reachable one — Django storage builds URLs using the Docker
    network hostname (`minio:9000`), which the browser can't reach.
    """
    if not image_field:
        return None
    try:
        url = image_field.url
    except Exception:
        return None

    internal = getattr(settings, "MINIO_INTERNAL_ENDPOINT", None)
    public = getattr(settings, "MINIO_PUBLIC_ENDPOINT", None)
    if internal and public and internal != public:
        url = url.replace(f"http://{internal}", f"http://{public}")
    return url


class PropertyImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model  = PropertyImage
        fields = ["id", "image_url", "is_cover", "order"]

    def get_image_url(self, obj):
        return _public_url(obj.image)


class PropertyCardSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()
    price_formatted = serializers.SerializerMethodField()
    distance_km     = serializers.FloatField(read_only=True, required=False)

    class Meta:
        model  = Property
        fields = [
            "id", "title", "property_type", "listing_type",
            "price", "price_formatted", "area_m2",
            "bedrooms", "bathrooms", "parking_spots",
            "latitude", "longitude",
            "address_line", "city", "state",
            "cover_image_url", "distance_km",
        ]

    def get_cover_image_url(self, obj):
        cache = getattr(obj, "_prefetched_objects_cache", {})
        images = list(cache.get("images") or [])
        if not images:
            images = list(obj.images.all())
        cover = next((img for img in images if img.is_cover), None) or (images[0] if images else None)
        return _public_url(cover.image) if cover else None

    def get_price_formatted(self, obj):
        value = int(obj.price)
        formatted = f"R$ {value:,.0f}".replace(",", ".")
        if obj.listing_type == "rent":
            return f"{formatted}/mês"
        return formatted


class PropertyDetailSerializer(serializers.ModelSerializer):
    images          = PropertyImageSerializer(many=True, read_only=True)
    price_formatted = serializers.SerializerMethodField()
    owner_name      = serializers.SerializerMethodField()

    class Meta:
        model  = Property
        fields = [
            "id", "title", "description", "property_type", "listing_type",
            "price", "price_formatted", "area_m2",
            "bedrooms", "bathrooms", "parking_spots",
            "latitude", "longitude",
            "address_line", "city", "state", "zipcode",
            "images", "owner_name", "created_at", "updated_at",
        ]

    def get_price_formatted(self, obj):
        value = int(obj.price)
        formatted = f"R$ {value:,.0f}".replace(",", ".")
        if obj.listing_type == "rent":
            return f"{formatted}/mês"
        return formatted

    def get_owner_name(self, obj):
        return obj.owner.name if obj.owner else None
