<script setup lang="ts">
const route = useRoute()

const {
  state,
  searchParams,
  fetchProperties,
  updatePage,
  setHovered,
} = usePropertySearch()

const showMap = ref(true)

const mapCenter = computed(() => ({
  lat: searchParams.value.lat,
  lng: searchParams.value.lng,
}))

useSeoMeta({
  title: () => `Imóveis em ${(route.query.local as string) || 'sua região'} — Wolliz`,
  description: () =>
    `Encontre casas e apartamentos para comprar e alugar em ${(route.query.local as string) || 'sua região'}.`,
})

// Initial data load — SSR renders the list, client hydrates from cache
const { data: initialData } = await useAsyncData(
  `search-${route.query.lat}-${route.query.lng}`,
  () => fetchProperties(),
)

// Populate state on client after hydration (state is fresh on client)
if (import.meta.client && initialData.value) {
  state.results = initialData.value.results
  state.total   = initialData.value.count
}
</script>

<template>
  <div class="busca">
    <header class="busca__header">
      <AppLogo />

      <SearchBar
        inline
        compact
        :initial-value="searchParams.local"
        class="busca__search"
      />

      <div class="view-toggle" role="tablist" aria-label="Modo de visualização">
        <button
          type="button"
          role="tab"
          :aria-selected="!showMap"
          class="view-toggle__btn"
          :class="{ 'view-toggle__btn--active': !showMap }"
          @click="showMap = false"
        >
          Lista
        </button>
        <button
          type="button"
          role="tab"
          :aria-selected="showMap"
          class="view-toggle__btn"
          :class="{ 'view-toggle__btn--active': showMap }"
          @click="showMap = true"
        >
          Mapa
        </button>
      </div>

      <AppUserMenu class="busca__user" />
    </header>

    <div class="busca__body" :class="{ 'busca__body--no-map': !showMap }">
      <!-- Lista (esquerda) -->
      <PropertyList
        :properties="state.results"
        :total="state.total"
        :page="state.page"
        :is-loading="state.isLoading"
        :with-map="showMap"
        class="busca__list"
        @page-change="updatePage"
        @hover="setHovered"
      />

      <!-- Mapa (direita) — client-only: Mapbox needs DOM/WebGL -->
      <ClientOnly v-if="showMap">
        <PropertyMap
          :properties="state.results"
          :center="mapCenter"
          :hovered-id="state.hoveredId"
          class="busca__map"

        />
        <template #fallback>
          <div class="busca__map-skeleton" aria-hidden="true" />
        </template>
      </ClientOnly>
    </div>

    <AppFooter compact />
  </div>
</template>

<style scoped>
.busca {
  height: 100dvh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--color-bg);
}

/* ── Header ────────────────────────────────────────────────────── */
.busca__header {
  height: 64px;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 0 20px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
  flex-shrink: 0;
}

.busca__search {
  flex: 1;
  min-width: 0;
  max-width: 480px;
}

.busca__user {
  flex-shrink: 0;
  margin-left: auto;
}

.view-toggle {
  display: inline-flex;
  background: #eef2f7;
  border-radius: 999px;
  padding: 4px;
  gap: 2px;
  flex-shrink: 0;
}

.view-toggle__btn {
  padding: 7px 22px;
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

.view-toggle__btn:hover:not(.view-toggle__btn--active) {
  color: #1a202c;
}

.view-toggle__btn--active {
  background: #fff;
  color: #1a202c;
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(0,0,0,.08), 0 0 0 1px rgba(0,0,0,.04);
}

/* ── Body ──────────────────────────────────────────────────────── */
.busca__body {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  overflow: hidden;
  min-height: 0;
}

.busca__body--no-map {
  grid-template-columns: 1fr;
  width: 100%;
}

.busca__list {
  overflow-y: auto;
  border-right: 1px solid var(--color-border);
}

.busca__body--no-map .busca__list {
  border-right: none;
}

.busca__map {
  height: 100%;
}

.busca__map-skeleton {
  height: 100%;
  background: linear-gradient(135deg, #f0f4f8 0%, #e8eef4 100%);
}

/* ── Mobile ────────────────────────────────────────────────────── */
@media (max-width: 768px) {
  .busca__body {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 360px;
  }
  .busca__list {
    border-right: none;
    border-bottom: 1px solid var(--color-border);
  }
  .busca__body--no-map {
    grid-template-rows: 1fr;
    max-width: 100%;
  }
}
</style>
