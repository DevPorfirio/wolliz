<script setup lang="ts">
import type { Property } from '~/composables/usePropertySearch'

const props = withDefaults(defineProps<{
  properties: Property[]
  total:      number
  page:       number
  isLoading:  boolean
  withMap?:   boolean
}>(), {
  withMap: true,
})

const emit = defineEmits<{
  (e: 'pageChange', page: number): void
  (e: 'hover', id: string | null): void
}>()

const totalPages = computed(() => Math.ceil(props.total / 20))

const activeType    = ref<string>('all')
const activeListing = ref<string>('all')

const typeOptions = [
  { value: 'all',        label: 'Todos' },
  { value: 'house',      label: 'Casa' },
  { value: 'apartment',  label: 'Apartamento' },
  { value: 'commercial', label: 'Comercial' },
  { value: 'land',       label: 'Terreno' },
]

const listingOptions = [
  { value: 'all',  label: 'Comprar e alugar' },
  { value: 'sale', label: 'Comprar' },
  { value: 'rent', label: 'Alugar' },
]

const filtered = computed(() => {
  let list = props.properties
  if (activeType.value    !== 'all') list = list.filter(p => p.property_type === activeType.value)
  if (activeListing.value !== 'all') list = list.filter(p => p.listing_type  === activeListing.value)
  return list
})
</script>

<template>
  <div class="property-list" :class="withMap ? 'property-list--with-map' : 'property-list--list-only'">
    <!-- Filter bar -->
    <div class="property-list__filters">
      <div class="filter-group">
        <button
          v-for="opt in listingOptions"
          :key="opt.value"
          class="filter-chip"
          :class="{ 'filter-chip--active': activeListing === opt.value }"
          @click="activeListing = opt.value"
        >
          {{ opt.label }}
        </button>
      </div>
      <div class="filter-group">
        <button
          v-for="opt in typeOptions"
          :key="opt.value"
          class="filter-chip"
          :class="{ 'filter-chip--active': activeType === opt.value }"
          @click="activeType = opt.value"
        >
          {{ opt.label }}
        </button>
      </div>
    </div>

    <div class="property-list__header">
      <span class="property-list__count">
        <template v-if="!isLoading">
          {{ filtered.length.toLocaleString('pt-BR') }}
          imóve{{ filtered.length !== 1 ? 'is' : 'l' }} encontrado{{ filtered.length !== 1 ? 's' : '' }}
        </template>
      </span>
    </div>

    <!-- Loading skeleton -->
    <div v-if="isLoading" class="property-list__grid">
      <div v-for="n in 6" :key="n" class="property-list__skeleton">
        <div class="skeleton skeleton--image" />
        <div class="skeleton-body">
          <div class="skeleton skeleton--price" />
          <div class="skeleton skeleton--title" />
          <div class="skeleton skeleton--meta" />
        </div>
      </div>
    </div>

    <!-- Results grid -->
    <div v-else-if="filtered.length" class="property-list__grid">
      <PropertyCard
        v-for="p in filtered"
        :key="p.id"
        :property="p"
        @mouseenter="emit('hover', $event)"
        @mouseleave="emit('hover', null)"
      />
    </div>

    <!-- Empty state -->
    <div v-else class="property-list__empty">
      <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
        <path d="M8 36V16L20 6l12 10v20H26v-10h-8v10H8Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
        <circle cx="30" cy="30" r="8" fill="var(--color-bg)" stroke="var(--color-border)" stroke-width="1.5"/>
        <path d="M27 30h6M30 27v6" stroke="var(--color-text-muted)" stroke-width="1.5" stroke-linecap="round"/>
      </svg>
      <p>Nenhum imóvel encontrado.</p>
      <p class="property-list__empty-sub">Tente ampliar a área ou mudar os filtros.</p>
    </div>

    <!-- Pagination -->
    <div v-if="!isLoading && totalPages > 1" class="property-list__pagination">
      <button
        class="pagination__btn"
        :disabled="page <= 1"
        @click="emit('pageChange', page - 1)"
      >
        ← Anterior
      </button>
      <span class="pagination__info">{{ page }} / {{ totalPages }}</span>
      <button
        class="pagination__btn"
        :disabled="page >= totalPages"
        @click="emit('pageChange', page + 1)"
      >
        Próxima →
      </button>
    </div>
  </div>
</template>

<style scoped>
.property-list {
  padding: 16px 16px 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* ── Filters ───────────────────────────────────────────────────── */
.property-list__filters {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-border);
}

.filter-group {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.filter-chip {
  font-size: 12px;
  font-weight: 500;
  font-family: inherit;
  padding: 5px 12px;
  border: 1px solid var(--color-border);
  border-radius: 20px;
  background: #fff;
  color: var(--color-text-muted);
  cursor: pointer;
  transition: background .12s, border-color .12s, color .12s;
  white-space: nowrap;
}
.filter-chip:hover {
  border-color: #c0c9d6;
  color: var(--color-text);
}
.filter-chip--active {
  background: #1a202c;
  border-color: #1a202c;
  color: #fff;
}

/* ── Header ────────────────────────────────────────────────────── */
.property-list__header {
  padding: 0;
}

.property-list__count {
  font-size: 13px;
  color: var(--color-text-muted);
  font-weight: 500;
}

/* ── Grid ──────────────────────────────────────────────────────── */
.property-list__grid {
  display: grid;
  gap: 14px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

/* With map: panel ≈ 50% of viewport. 3 cols when panel can give ≥300px per card */
@media (min-width: 1900px) {
  .property-list--with-map .property-list__grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
@media (min-width: 2600px) {
  .property-list--with-map .property-list__grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

/* List-only: full viewport, scales 2 → 3 → 4 → 5 → 6 cols */
.property-list--list-only .property-list__grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}
@media (min-width: 1300px) {
  .property-list--list-only .property-list__grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
@media (min-width: 1700px) {
  .property-list--list-only .property-list__grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}
@media (min-width: 2100px) {
  .property-list--list-only .property-list__grid {
    grid-template-columns: repeat(5, minmax(0, 1fr));
  }
}
@media (min-width: 2500px) {
  .property-list--list-only .property-list__grid {
    grid-template-columns: repeat(6, minmax(0, 1fr));
  }
}

/* ── Skeleton ──────────────────────────────────────────────────── */
.property-list__skeleton {
  border: 1px solid var(--color-border);
  border-radius: 12px;
  overflow: hidden;
}

.skeleton {
  background: linear-gradient(90deg, #f0f4f8 25%, #e2e8f0 50%, #f0f4f8 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
  border-radius: 4px;
}

@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton--image {
  aspect-ratio: 4 / 3;
  border-radius: 0;
}

.skeleton-body {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton--price  { height: 18px; width: 120px; }
.skeleton--title  { height: 13px; width: 80%; }
.skeleton--meta   { height: 12px; width: 60%; }

/* ── Empty state ───────────────────────────────────────────────── */
.property-list__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 48px 24px;
  color: var(--color-text-muted);
  text-align: center;
  font-size: 14px;
}

.property-list__empty-sub {
  font-size: 13px;
  opacity: .7;
}

/* ── Pagination ───────────────────────────────────────────────── */
.property-list__pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0 4px;
  margin-top: 4px;
  border-top: 1px solid var(--color-border);
}

.pagination__btn {
  font-size: 13px;
  font-weight: 500;
  font-family: inherit;
  color: var(--color-brand);
  background: none;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 7px 14px;
  cursor: pointer;
  transition: background .15s, border-color .15s;
}
.pagination__btn:hover:not(:disabled) {
  background: var(--color-bg);
  border-color: #c0c9d6;
}
.pagination__btn:disabled {
  opacity: .4;
  cursor: not-allowed;
}

.pagination__info {
  font-size: 13px;
  color: var(--color-text-muted);
}

/* ── Mobile ────────────────────────────────────────────────────── */
@media (max-width: 900px) {
  .property-list__grid,
  .property-list--with-map .property-list__grid,
  .property-list--list-only .property-list__grid {
    grid-template-columns: 1fr;
  }
}
</style>
