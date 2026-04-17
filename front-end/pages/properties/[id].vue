<script setup lang="ts">
const route  = useRoute()
const config = useRuntimeConfig()

interface PropertyImage {
  id:        string
  image_url: string | null
  is_cover:  boolean
  order:     number
}

interface PropertyDetail {
  id:             string
  title:          string
  description:    string
  property_type:  'house' | 'apartment' | 'commercial' | 'land'
  listing_type:   'sale' | 'rent'
  price:          number
  price_formatted: string
  area_m2:        number
  bedrooms:       number
  bathrooms:      number
  parking_spots:  number
  latitude:       number
  longitude:      number
  address_line:   string
  city:           string
  state:          string
  zipcode:        string
  images:         PropertyImage[]
  owner_name:     string | null
  created_at:     string
  updated_at:     string
}

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

const { data: property, error } = await useAsyncData<PropertyDetail>(
  `property-${route.params.id}`,
  async () => {
    const baseUrl = import.meta.server ? config.apiBaseUrl : config.public.apiBaseUrl
    return $fetch<PropertyDetail>(`${baseUrl}/api/properties/${route.params.id}`)
  },
)

if (error.value || !property.value) {
  throw createError({ statusCode: 404, message: 'Imóvel não encontrado.' })
}

const title = computed(() =>
  property.value ? property.value.title.replace('[MOCK] ', '') : '',
)

useSeoMeta({
  title:       () => `${title.value} — Wolliz`,
  description: () => property.value?.description || `${title.value} em ${property.value?.city}/${property.value?.state}.`,
})

const activeImage = ref(0)

const allImages = computed(() => property.value?.images ?? [])
const hasImages = computed(() => allImages.value.length > 0)

function nextImage() {
  if (!allImages.value.length) return
  activeImage.value = (activeImage.value + 1) % allImages.value.length
}
function prevImage() {
  if (!allImages.value.length) return
  activeImage.value = (activeImage.value - 1 + allImages.value.length) % allImages.value.length
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' })
}

const locationView = ref<'map' | 'street'>('map')
const showWipModal = ref(false)

const mapUrl = computed(() => {
  if (!property.value) return ''
  const { latitude, longitude, address_line, city, state } = property.value
  const q = encodeURIComponent(`${address_line}, ${city}, ${state}, Brasil`)
  return `https://maps.google.com/maps?q=${q}&z=16&output=embed`
})

const streetViewUrl = computed(() => {
  if (!property.value) return ''
  const { latitude, longitude } = property.value
  // Pure Street View embed: `layer=c` + `cbll` + `output=svembed`.
  // Adding `q=` would override and revert Google to the map view.
  return `https://maps.google.com/maps?layer=c&cbll=${latitude},${longitude}&cbp=11,0,0,0,0&output=svembed`
})
</script>

<template>
  <div class="detail-page">
    <header class="detail-header">
      <AppLogo />
      <AppUserMenu />
    </header>

    <main v-if="property" class="detail-main">
      <!-- Gallery -->
      <div class="detail-gallery">
        <div class="detail-gallery__main">
          <img
            v-if="hasImages && allImages[activeImage]?.image_url"
            :src="allImages[activeImage].image_url!"
            :alt="title"
            class="detail-gallery__img"
          />
          <div v-else class="detail-gallery__placeholder">
            <svg width="48" height="48" viewBox="0 0 32 32" fill="none">
              <path d="M4 28V14L16 4l12 10v14H20v-8h-8v8H4Z" stroke="#a0aec0" stroke-width="1.5" stroke-linejoin="round"/>
            </svg>
          </div>

          <template v-if="allImages.length > 1">
            <button
              type="button"
              class="gallery-nav gallery-nav--prev"
              aria-label="Foto anterior"
              @click="prevImage"
            >
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <path d="M15 18l-6-6 6-6" stroke="#1a202c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
            <button
              type="button"
              class="gallery-nav gallery-nav--next"
              aria-label="Próxima foto"
              @click="nextImage"
            >
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <path d="M9 18l6-6-6-6" stroke="#1a202c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
            <div class="gallery-counter">
              {{ activeImage + 1 }} / {{ allImages.length }}
            </div>
          </template>
        </div>
        <div v-if="allImages.length > 1" class="detail-gallery__thumbs">
          <button
            v-for="(img, i) in allImages"
            :key="img.id"
            class="detail-gallery__thumb"
            :class="{ 'detail-gallery__thumb--active': i === activeImage }"
            @click="activeImage = i"
          >
            <img v-if="img.image_url" :src="img.image_url" :alt="`Foto ${i + 1}`" />
          </button>
        </div>
      </div>

      <!-- Content -->
      <div class="detail-content">
        <!-- Left: property info -->
        <div class="detail-info">
          <!-- Badges + price -->
          <div class="detail-info__top">
            <div class="detail-badges">
              <span class="detail-badge detail-badge--type">
                {{ typeLabel[property.property_type] }}
              </span>
              <span class="detail-badge" :class="`detail-badge--${property.listing_type}`">
                {{ listingLabel[property.listing_type] }}
              </span>
            </div>
            <p class="detail-price">{{ property.price_formatted }}</p>
            <h1 class="detail-title">{{ title }}</h1>
            <p class="detail-address">
              <svg width="13" height="13" viewBox="0 0 14 14" fill="none">
                <path d="M7 1a4 4 0 0 1 4 4c0 3-4 8-4 8S3 8 3 5a4 4 0 0 1 4-4Z" stroke="currentColor" stroke-width="1.3"/>
                <circle cx="7" cy="5" r="1.3" stroke="currentColor" stroke-width="1.3"/>
              </svg>
              {{ property.address_line }}, {{ property.city }} — {{ property.state }}
              <span v-if="property.zipcode" class="detail-address__zip">{{ property.zipcode }}</span>
            </p>
          </div>

          <!-- Stats -->
          <div class="detail-stats">
            <div class="detail-stat">
              <svg width="16" height="16" viewBox="0 0 14 14" fill="none">
                <rect x="1" y="4" width="12" height="9" rx="1" stroke="currentColor" stroke-width="1.3"/>
                <path d="M4 4V2.5A1.5 1.5 0 0 1 7 2.5V4" stroke="currentColor" stroke-width="1.3"/>
              </svg>
              <span class="detail-stat__value">{{ property.area_m2 }}</span>
              <span class="detail-stat__label">m²</span>
            </div>
            <div v-if="property.bedrooms" class="detail-stat">
              <svg width="16" height="16" viewBox="0 0 14 14" fill="none">
                <rect x="1" y="6" width="12" height="6" rx="1" stroke="currentColor" stroke-width="1.3"/>
                <path d="M1 9V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v5" stroke="currentColor" stroke-width="1.3"/>
                <path d="M5 6V4h4v2" stroke="currentColor" stroke-width="1.3"/>
              </svg>
              <span class="detail-stat__value">{{ property.bedrooms }}</span>
              <span class="detail-stat__label">quarto{{ property.bedrooms > 1 ? 's' : '' }}</span>
            </div>
            <div v-if="property.bathrooms" class="detail-stat">
              <svg width="16" height="16" viewBox="0 0 14 14" fill="none">
                <path d="M2 7h10v2a4 4 0 0 1-8 0V7Z" stroke="currentColor" stroke-width="1.3"/>
                <path d="M4 7V3a1 1 0 0 1 2 0" stroke="currentColor" stroke-width="1.3"/>
              </svg>
              <span class="detail-stat__value">{{ property.bathrooms }}</span>
              <span class="detail-stat__label">banheiro{{ property.bathrooms > 1 ? 's' : '' }}</span>
            </div>
            <div v-if="property.parking_spots" class="detail-stat">
              <svg width="16" height="16" viewBox="0 0 14 14" fill="none">
                <rect x="1" y="3" width="12" height="8" rx="1.5" stroke="currentColor" stroke-width="1.3"/>
                <path d="M1 7h12" stroke="currentColor" stroke-width="1.3"/>
                <path d="M4 11v2M10 11v2" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
              </svg>
              <span class="detail-stat__value">{{ property.parking_spots }}</span>
              <span class="detail-stat__label">vaga{{ property.parking_spots > 1 ? 's' : '' }}</span>
            </div>
          </div>

          <!-- Description -->
          <div v-if="property.description" class="detail-section">
            <h2 class="detail-section__title">Descrição</h2>
            <p class="detail-description">{{ property.description }}</p>
          </div>

          <!-- Publication info -->
          <div class="detail-meta">
            <span>Publicado em {{ formatDate(property.created_at) }}</span>
            <span v-if="property.updated_at !== property.created_at">
              · Atualizado em {{ formatDate(property.updated_at) }}
            </span>
          </div>
        </div>

        <!-- Right: contact only -->
        <div class="detail-sidebar">
          <div class="detail-contact">
            <p class="detail-contact__price">{{ property.price_formatted }}</p>
            <p v-if="property.owner_name" class="detail-contact__name">
              Anunciante: {{ property.owner_name }}
            </p>
            <p v-else class="detail-contact__name">Anunciado pela Wolliz</p>
            <button
              type="button"
              class="detail-contact__btn detail-contact__btn--primary"
              @click="showWipModal = true"
            >
              Entrar em contato
            </button>
            <button
              type="button"
              class="detail-contact__btn detail-contact__btn--secondary"
              @click="showWipModal = true"
            >
              Agendar visita
            </button>
          </div>
        </div>
      </div>

      <!-- Location section — toggle between map view and street view -->
      <section class="detail-streetview">
        <div class="detail-streetview__head">
          <div>
            <h2 class="detail-section__title">Veja o local</h2>
            <p class="detail-streetview__sub">
              {{ property.address_line }}, {{ property.city }}/{{ property.state }}
            </p>
          </div>

          <div class="location-toggle" role="tablist" aria-label="Modo de visualização do local">
            <button
              type="button"
              role="tab"
              :aria-selected="locationView === 'map'"
              class="location-toggle__btn"
              :class="{ 'location-toggle__btn--active': locationView === 'map' }"
              @click="locationView = 'map'"
            >
              Mapa
            </button>
            <button
              type="button"
              role="tab"
              :aria-selected="locationView === 'street'"
              class="location-toggle__btn"
              :class="{ 'location-toggle__btn--active': locationView === 'street' }"
              @click="locationView = 'street'"
            >
              Street View
            </button>
          </div>
        </div>

        <ClientOnly>
          <iframe
            :key="locationView"
            :src="locationView === 'map' ? mapUrl : streetViewUrl"
            class="detail-streetview__frame"
            allowfullscreen
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade"
          />
          <template #fallback>
            <div class="detail-streetview__frame detail-streetview__frame--skeleton" />
          </template>
        </ClientOnly>
      </section>
    </main>

    <AppFooter />

    <!-- Work-in-progress modal -->
    <Teleport to="body">
      <Transition name="wip-fade">
        <div
          v-if="showWipModal"
          class="wip-overlay"
          role="dialog"
          aria-modal="true"
          aria-labelledby="wip-title"
          @click.self="showWipModal = false"
        >
          <div class="wip-modal">
            <div class="wip-modal__icon" aria-hidden="true">
              <svg width="34" height="34" viewBox="0 0 24 24" fill="none">
                <path d="M12 8v4M12 16h.01" stroke="#006aff" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="12" r="9" stroke="#006aff" stroke-width="2"/>
              </svg>
            </div>
            <h3 id="wip-title" class="wip-modal__title">Em desenvolvimento</h3>
            <p class="wip-modal__text">
              Esta funcionalidade ainda está sendo construída e estará disponível em breve.
            </p>
            <button type="button" class="wip-modal__btn" @click="showWipModal = false">
              Entendi
            </button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.detail-page {
  min-height: 100dvh;
  background: var(--color-bg);
  display: flex;
  flex-direction: column;
}

/* ── Header ────────────────────────────────────────────────────── */
.detail-header {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 0 24px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
  flex-shrink: 0;
  position: sticky;
  top: 0;
  z-index: 10;
}

/* ── Main ──────────────────────────────────────────────────────── */
.detail-main {
  max-width: 1120px;
  width: 100%;
  margin: 0 auto;
  padding: 32px 24px 64px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

/* ── Gallery ───────────────────────────────────────────────────── */
.detail-gallery {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.detail-gallery__main {
  position: relative;
  aspect-ratio: 16 / 7;
  background: #f0f4f8;
  border-radius: 16px;
  overflow: hidden;
}

/* Prev/next arrows */
.gallery-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255,255,255,.92);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 10px rgba(0,0,0,.18);
  transition: background .15s, transform .15s;
}
.gallery-nav:hover {
  background: #fff;
  transform: translateY(-50%) scale(1.06);
}
.gallery-nav--prev { left: 16px; }
.gallery-nav--next { right: 16px; }

.gallery-counter {
  position: absolute;
  bottom: 16px;
  right: 16px;
  background: rgba(0,0,0,.6);
  color: #fff;
  padding: 5px 12px;
  border-radius: 14px;
  font-size: 12px;
  font-weight: 500;
  backdrop-filter: blur(4px);
}

.detail-gallery__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.detail-gallery__placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.detail-gallery__thumbs {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  scrollbar-width: thin;
}

.detail-gallery__thumb {
  flex-shrink: 0;
  width: 80px;
  height: 56px;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid transparent;
  cursor: pointer;
  padding: 0;
  background: #f0f4f8;
  transition: border-color .15s;
}
.detail-gallery__thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.detail-gallery__thumb--active {
  border-color: #006aff;
}

/* ── Content ───────────────────────────────────────────────────── */
.detail-content {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 32px;
  align-items: start;
}

/* ── Info (left) ───────────────────────────────────────────────── */
.detail-info {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.detail-info__top {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-badges {
  display: flex;
  gap: 8px;
}

.detail-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 6px;
  letter-spacing: .02em;
}
.detail-badge--type {
  background: #f0f4f8;
  color: #4a5568;
}
.detail-badge--sale {
  background: #ebf4ff;
  color: #006aff;
}
.detail-badge--rent {
  background: #e6fcf5;
  color: #0d9f6e;
}

.detail-price {
  font-size: 32px;
  font-weight: 800;
  color: #1a202c;
  letter-spacing: -.04em;
  line-height: 1;
}

.detail-title {
  font-size: 22px;
  font-weight: 600;
  color: #1a202c;
  line-height: 1.3;
}

.detail-address {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
  color: #718096;
}
.detail-address__zip {
  color: #a0aec0;
  margin-left: 4px;
}

/* ── Stats ─────────────────────────────────────────────────────── */
.detail-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  padding: 20px;
  background: #f7fafc;
  border-radius: 12px;
}

.detail-stat {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #4a5568;
}

.detail-stat__value {
  font-size: 18px;
  font-weight: 700;
  color: #1a202c;
}

.detail-stat__label {
  font-size: 13px;
  color: #718096;
}

/* ── Section ───────────────────────────────────────────────────── */
.detail-section__title {
  font-size: 16px;
  font-weight: 600;
  color: #1a202c;
  margin-bottom: 10px;
}

.detail-description {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.7;
  white-space: pre-line;
}

.detail-meta {
  font-size: 12px;
  color: #a0aec0;
  padding-top: 16px;
  border-top: 1px solid #edf2f7;
}

/* ── Sidebar (right) ───────────────────────────────────────────── */
.detail-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: sticky;
  top: 84px;
}

.detail-contact {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-contact__price {
  font-size: 24px;
  font-weight: 800;
  color: #1a202c;
  letter-spacing: -.04em;
}

.detail-contact__name {
  font-size: 13px;
  color: #718096;
}

.detail-contact__btn {
  display: block;
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  text-align: center;
  cursor: pointer;
  text-decoration: none;
  transition: opacity .15s;
}
.detail-contact__btn:hover { opacity: .9; }
.detail-contact__btn--primary {
  background: #006aff;
  color: #fff;
  border: none;
}
.detail-contact__btn--secondary {
  background: #fff;
  color: #1a202c;
  border: 1px solid #e2e8f0;
}

/* ── Street View (large, full-width) ───────────────────────────── */
.detail-streetview {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-streetview__head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.detail-streetview__sub {
  font-size: 13px;
  color: #718096;
  margin-top: 4px;
}

.location-toggle {
  display: inline-flex;
  background: #eef2f7;
  border-radius: 999px;
  padding: 4px;
  gap: 2px;
  flex-shrink: 0;
}
.location-toggle__btn {
  padding: 7px 18px;
  border: none;
  background: transparent;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 500;
  font-family: inherit;
  color: #718096;
  cursor: pointer;
  transition: background .15s, color .15s, box-shadow .15s;
  line-height: 1;
}
.location-toggle__btn:hover:not(.location-toggle__btn--active) {
  color: #1a202c;
}
.location-toggle__btn--active {
  background: #fff;
  color: #1a202c;
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(0,0,0,.08), 0 0 0 1px rgba(0,0,0,.04);
}

.detail-streetview__frame {
  width: 100%;
  height: 520px;
  border: none;
  border-radius: 16px;
  display: block;
  background: #f0f4f8;
}

.detail-streetview__frame--skeleton {
  background: linear-gradient(135deg, #f0f4f8 0%, #e8eef4 100%);
}

/* ── Mobile ────────────────────────────────────────────────────── */
@media (max-width: 768px) {
  .detail-content {
    grid-template-columns: 1fr;
  }
  .detail-sidebar {
    position: static;
  }
  .detail-gallery__main {
    aspect-ratio: 4 / 3;
  }
  .detail-streetview__frame {
    height: 320px;
  }
  .gallery-nav {
    width: 36px;
    height: 36px;
  }
}
</style>

<style>
/* Unscoped: <Teleport> renders outside the page's scoped CSS context */
.wip-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, .55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  backdrop-filter: blur(2px);
}

.wip-modal {
  background: #fff;
  border-radius: 16px;
  padding: 28px 28px 24px;
  width: 100%;
  max-width: 380px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, .25);
  font-family: inherit;
}

.wip-modal__icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #ebf4ff;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 4px;
}

.wip-modal__title {
  font-size: 19px;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
}

.wip-modal__text {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.5;
  margin: 0;
}

.wip-modal__btn {
  margin-top: 12px;
  width: 100%;
  padding: 11px;
  border: none;
  border-radius: 10px;
  background: #006aff;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: background .15s;
}
.wip-modal__btn:hover { background: #0055cc; }

.wip-fade-enter-active,
.wip-fade-leave-active {
  transition: opacity .18s ease;
}
.wip-fade-enter-from,
.wip-fade-leave-to {
  opacity: 0;
}
.wip-fade-enter-active .wip-modal,
.wip-fade-leave-active .wip-modal {
  transition: transform .18s ease;
}
.wip-fade-enter-from .wip-modal,
.wip-fade-leave-to .wip-modal {
  transform: scale(.96);
}
</style>
