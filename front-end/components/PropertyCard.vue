<script setup lang="ts">
import type { Property } from '~/composables/usePropertySearch'

const props = defineProps<{
  property:   Property
  isHovered?: boolean
}>()

const emit = defineEmits<{
  (e: 'mouseenter', id: string): void
  (e: 'mouseleave'): void
}>()

const typeLabel: Record<string, string> = {
  house:      'Casa',
  apartment:  'Apartamento',
  commercial: 'Comercial',
  land:       'Terreno',
}

const listingLabel: Record<string, string> = {
  sale: 'Venda',
  rent: 'Aluguel',
}
</script>

<template>
  <NuxtLink
    :to="`/properties/${property.id}`"
    target="_blank"
    rel="noopener"
    class="property-card"
    :class="{ 'property-card--hovered': isHovered }"
    @mouseenter="emit('mouseenter', property.id)"
    @mouseleave="emit('mouseleave')"
  >
    <div class="property-card__image-wrap">
      <img
        v-if="property.cover_image_url"
        :src="property.cover_image_url"
        :alt="property.title"
        class="property-card__image"
        loading="lazy"
      />
      <div v-else class="property-card__image-placeholder">
        <svg width="36" height="36" viewBox="0 0 32 32" fill="none">
          <path d="M4 28V14L16 4l12 10v14H20v-8h-8v8H4Z" stroke="#a0aec0" stroke-width="1.5" stroke-linejoin="round"/>
        </svg>
      </div>
      <span class="property-card__badge property-card__badge--type">
        {{ typeLabel[property.property_type] }}
      </span>
      <span class="property-card__badge property-card__badge--listing">
        {{ listingLabel[property.listing_type] }}
      </span>
    </div>

    <div class="property-card__body">
      <p class="property-card__price">{{ property.price_formatted }}</p>
      <h3 class="property-card__title">{{ property.title.replace('[MOCK] ', '') }}</h3>
      <p class="property-card__address">{{ property.city }}/{{ property.state }}</p>

      <div class="property-card__stats">
        <span class="property-card__stat">
          <svg width="13" height="13" viewBox="0 0 14 14" fill="none">
            <rect x="1" y="4" width="12" height="9" rx="1" stroke="currentColor" stroke-width="1.3"/>
            <path d="M4 4V2.5A1.5 1.5 0 0 1 7 2.5V4" stroke="currentColor" stroke-width="1.3"/>
          </svg>
          {{ property.area_m2 }} m²
        </span>
        <span v-if="property.bedrooms" class="property-card__stat">
          <svg width="13" height="13" viewBox="0 0 14 14" fill="none">
            <rect x="1" y="6" width="12" height="6" rx="1" stroke="currentColor" stroke-width="1.3"/>
            <path d="M1 9V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v5" stroke="currentColor" stroke-width="1.3"/>
            <path d="M5 6V4h4v2" stroke="currentColor" stroke-width="1.3"/>
          </svg>
          {{ property.bedrooms }} qto{{ property.bedrooms > 1 ? 's' : '' }}
        </span>
        <span v-if="property.bathrooms" class="property-card__stat">
          <svg width="13" height="13" viewBox="0 0 14 14" fill="none">
            <path d="M2 7h10v2a4 4 0 0 1-8 0V7Z" stroke="currentColor" stroke-width="1.3"/>
            <path d="M4 7V3a1 1 0 0 1 2 0" stroke="currentColor" stroke-width="1.3"/>
          </svg>
          {{ property.bathrooms }} ban{{ property.bathrooms > 1 ? 'heiros' : 'heiro' }}
        </span>
        <span v-if="property.distance_km" class="property-card__stat property-card__stat--distance">
          {{ property.distance_km < 1 ? `${Math.round(property.distance_km * 1000)} m` : `${property.distance_km.toFixed(1)} km` }}
        </span>
      </div>
    </div>
  </NuxtLink>
</template>

<style scoped>
.property-card {
  display: block;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow .2s, border-color .2s;
  text-decoration: none;
  color: inherit;
}
.property-card:hover,
.property-card--hovered {
  box-shadow: 0 4px 16px rgba(0,0,0,.1);
  border-color: #c0c9d6;
  text-decoration: none;
}

/* Proporção 4:3 — mais quadrado, como fotos de imóveis reais */
.property-card__image-wrap {
  position: relative;
  aspect-ratio: 4 / 3;
  background: #f7fafc;
  overflow: hidden;
}

.property-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform .3s;
}
.property-card:hover .property-card__image {
  transform: scale(1.03);
}

.property-card__image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f4f8;
}

.property-card__badge {
  position: absolute;
  font-size: 11px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 6px;
  line-height: 1.3;
  letter-spacing: .02em;
}
.property-card__badge--type {
  top: 10px;
  left: 10px;
  background: rgba(0,0,0,.52);
  color: #fff;
  backdrop-filter: blur(4px);
}
.property-card__badge--listing {
  top: 10px;
  right: 10px;
  background: #006aff;
  color: #fff;
}
.property-card__badge--listing[data-type="rent"] {
  background: #0d9f6e;
}

.property-card__body {
  padding: 14px 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 3px;
  background: #fff;
}

.property-card__price {
  font-size: 19px;
  font-weight: 800;
  color: #1a202c;
  letter-spacing: -.03em;
  line-height: 1.1;
}

.property-card__title {
  font-size: 13px;
  font-weight: 500;
  color: #2d3748;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: 2px;
}

.property-card__address {
  font-size: 12px;
  color: #718096;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.property-card__stats {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #edf2f7;
}

.property-card__stat {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #718096;
}
.property-card__stat--distance {
  margin-left: auto;
  color: #006aff;
  font-weight: 600;
}
</style>
