import uuid
from django.db import models
from django.conf import settings


class PropertyType(models.TextChoices):
    HOUSE      = "house",      "Casa"
    APARTMENT  = "apartment",  "Apartamento"
    COMMERCIAL = "commercial", "Comercial"
    LAND       = "land",       "Terreno"


class ListingType(models.TextChoices):
    SALE = "sale", "Venda"
    RENT = "rent", "Aluguel"


class Property(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner         = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="properties",
        null=True,
        blank=True,
    )
    title         = models.CharField(max_length=255)
    description   = models.TextField(blank=True, default="")
    property_type = models.CharField(max_length=20, choices=PropertyType.choices)
    listing_type  = models.CharField(max_length=10, choices=ListingType.choices)
    price         = models.DecimalField(max_digits=14, decimal_places=2)
    area_m2       = models.DecimalField(max_digits=8, decimal_places=2)
    bedrooms      = models.PositiveSmallIntegerField(default=0)
    bathrooms     = models.PositiveSmallIntegerField(default=0)
    parking_spots = models.PositiveSmallIntegerField(default=0)
    latitude      = models.DecimalField(max_digits=9, decimal_places=6, db_index=True)
    longitude     = models.DecimalField(max_digits=9, decimal_places=6, db_index=True)
    address_line  = models.CharField(max_length=512)
    city          = models.CharField(max_length=100, db_index=True)
    state         = models.CharField(max_length=2)
    zipcode       = models.CharField(max_length=10, blank=True, default="")
    is_active     = models.BooleanField(default=True, db_index=True)
    created_at    = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = "properties"
        ordering            = ["-created_at"]
        verbose_name        = "Imóvel"
        verbose_name_plural = "Imóveis"

    def __str__(self) -> str:
        return f"{self.title} ({self.city})"


class PropertyImage(models.Model):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property   = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image      = models.ImageField(upload_to="properties/")
    is_cover   = models.BooleanField(default=False)
    order      = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "property_images"
        ordering = ["order", "created_at"]
