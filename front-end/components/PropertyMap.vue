<script setup lang="ts">
import type mapboxglLib from 'mapbox-gl'
import type { Property } from '~/composables/usePropertySearch'

const props = defineProps<{
  properties: Property[]
  center:     { lat: number; lng: number }
  hoveredId:  string | null
}>()

const nuxtApp  = useNuxtApp()
const mapboxgl = nuxtApp.$mapboxgl as typeof mapboxglLib

const mapContainer = ref<HTMLDivElement | null>(null)
let map:         mapboxglLib.Map   | null = null
let activePopup: mapboxglLib.Popup | null = null
const markers: Record<string, mapboxglLib.Marker> = {}

onMounted(() => {
  if (!mapContainer.value) return

  map = new mapboxgl.Map({
    container: mapContainer.value,
    style:     'mapbox://styles/mapbox/light-v11',
    center:    [props.center.lng, props.center.lat],
    zoom:      13,
  })

  // Aguarda o mapa carregar antes de adicionar marcadores
  map.on('load', () => {
    syncMarkers(props.properties)
  })
})

function syncMarkers(properties: Property[]) {
  if (!map) return

  // Remove marcadores que não estão mais na lista
  for (const id of Object.keys(markers)) {
    if (!properties.find(p => p.id === id)) {
      markers[id].remove()
      delete markers[id]
    }
  }

  // Adiciona novos marcadores
  for (const p of properties) {
    if (markers[p.id]) continue
    const el = createPriceEl(p)
    el.addEventListener('click', (e) => {
      e.stopPropagation()
      showPopup(p)
    })
    markers[p.id] = new mapboxgl.Marker({ element: el })
      .setLngLat([Number(p.longitude), Number(p.latitude)])
      .addTo(map!)
  }
}

watch(
  () => props.properties,
  (newProps) => {
    if (!map) return
    if (!map.loaded()) {
      // Se o mapa ainda não carregou, espera o evento load
      map.once('load', () => syncMarkers(newProps))
      return
    }
    syncMarkers(newProps)
  },
  { deep: false },
)

watch(
  () => props.hoveredId,
  (id, prevId) => {
    if (prevId && markers[prevId]) {
      markers[prevId].getElement().classList.remove('map-dot-wrap--active')
    }
    if (id && markers[id]) {
      markers[id].getElement().classList.add('map-dot-wrap--active')
    }
  },
)

function createPriceEl(p: Property): HTMLDivElement {
  const wrap = document.createElement('div')
  wrap.className = 'map-dot-wrap'
  wrap.title     = p.price_formatted

  const dot = document.createElement('div')
  dot.className = `map-dot map-dot--${p.listing_type}`

  wrap.appendChild(dot)
  return wrap
}

function showPopup(p: Property) {
  if (!map) return
  activePopup?.remove()

  const cleanTitle = p.title.replace('[MOCK] ', '')
  const stats: string[] = [`${p.area_m2} m²`]
  if (p.bedrooms)  stats.push(`${p.bedrooms} qto${p.bedrooms > 1 ? 's' : ''}`)
  if (p.bathrooms) stats.push(`${p.bathrooms} ban${p.bathrooms > 1 ? 'h' : ''}`)

  activePopup = new mapboxgl.Popup({ offset: 18, closeButton: false, maxWidth: '340px', className: 'wz-popup' })
    .setLngLat([Number(p.longitude), Number(p.latitude)])
    .setHTML(`
      <div class="map-popup">
        ${p.cover_image_url
          ? `<img src="${p.cover_image_url}" class="map-popup__img" alt="${cleanTitle}" />`
          : `<div class="map-popup__img map-popup__img--placeholder"></div>`}
        <div class="map-popup__body">
          <p class="map-popup__price">${p.price_formatted}</p>
          <p class="map-popup__title">${cleanTitle}</p>
          <p class="map-popup__meta">${stats.join(' · ')}</p>
          <p class="map-popup__addr">${p.city}/${p.state}</p>
          <p class="map-popup__cta-q">Quer ver mais detalhes desse imóvel?</p>
          <a href="/properties/${p.id}" target="_blank" rel="noopener" class="map-popup__cta">Acessar imóvel →</a>
        </div>
      </div>
    `)
    .addTo(map)
}

onUnmounted(() => {
  activePopup?.remove()
  map?.remove()
})
</script>

<template>
  <div ref="mapContainer" class="property-map" />
</template>

<style>
.map-dot-wrap {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: transparent;
}
.map-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2.5px solid #fff;
  box-shadow: 0 1px 5px rgba(0,0,0,.35);
  transition: transform .15s;
  pointer-events: none;
}
.map-dot--sale { background: #006aff; }
.map-dot--rent { background: #0d9f6e; }
.map-dot-wrap:hover .map-dot,
.map-dot-wrap--active .map-dot {
  transform: scale(1.6);
}
.map-dot-wrap:hover,
.map-dot-wrap--active {
  z-index: 10;
}

/* Override default Mapbox popup styles to match card design */
.wz-popup .mapboxgl-popup-content {
  border-radius: 12px;
  padding: 0;
  overflow: hidden;
  box-shadow: 0 6px 24px rgba(0,0,0,.18);
  border: none;
}
.wz-popup .mapboxgl-popup-tip {
  border-top-color: #fff;
}

.map-popup { font-family: inherit; width: 340px; }
.map-popup__img {
  width: 100%;
  aspect-ratio: 16 / 10;
  object-fit: cover;
  display: block;
  background: #f0f4f8;
}
.map-popup__img--placeholder { aspect-ratio: 16 / 10; }
.map-popup__body { padding: 14px 14px 14px; }
.map-popup__price {
  font-size: 17px;
  font-weight: 800;
  color: #1a202c;
  margin: 0 0 2px;
  letter-spacing: -.02em;
}
.map-popup__title {
  font-size: 13px;
  font-weight: 500;
  color: #1a202c;
  margin: 0 0 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.map-popup__meta,
.map-popup__addr {
  font-size: 12px;
  color: #718096;
  margin: 0 0 2px;
}
.map-popup__cta-q {
  font-size: 12px;
  color: #4a5568;
  margin: 10px 0 6px;
  padding-top: 8px;
  border-top: 1px solid #edf2f7;
}
.map-popup__cta {
  display: block;
  text-align: center;
  background: #006aff;
  color: #fff !important;
  font-size: 13px;
  font-weight: 600;
  padding: 8px 12px;
  border-radius: 8px;
  text-decoration: none;
  transition: background .15s;
}
.map-popup__cta:hover {
  background: #0055cc;
}
</style>

<style scoped>
.property-map {
  width: 100%;
  height: 100%;
}
</style>
