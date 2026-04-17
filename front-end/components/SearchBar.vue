<script setup lang="ts">
interface Suggestion {
  place_name: string
  center:     [number, number]
}

const props = defineProps<{
  // Quando true: atualiza params da rota atual em vez de navegar para /busca
  inline?:       boolean
  // Pré-preenche o input com o valor atual da busca
  initialValue?: string
  // Versão compacta para o header
  compact?:      boolean
}>()

const router  = useRouter()
const route   = useRoute()
const config  = useRuntimeConfig()

const inputValue     = ref(props.initialValue ?? '')
const suggestions    = ref<Suggestion[]>([])
const isLoadingGeo   = ref(false)
const showDropdown   = ref(false)
const selectedCoords = ref<{ lat: number; lng: number } | null>(null)

// Atualiza o input se o initialValue mudar (ex: navegação externa)
watch(() => props.initialValue, (val) => {
  if (val !== undefined) inputValue.value = val
})

let debounceTimer: ReturnType<typeof setTimeout> | null = null

function onInput() {
  selectedCoords.value = null
  const q = inputValue.value.trim()
  if (q.length < 3) {
    suggestions.value  = []
    showDropdown.value = false
    return
  }
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => fetchSuggestions(q), 300)
}

async function fetchSuggestions(q: string) {
  isLoadingGeo.value = true
  try {
    const token = config.public.mapboxToken as string
    const url   =
      `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(q)}.json` +
      `?access_token=${token}&country=BR&language=pt` +
      `&types=place,district,region,neighborhood&limit=5`
    const data = await $fetch<{ features: { place_name: string; center: [number, number] }[] }>(url)
    suggestions.value  = data.features.map(f => ({ place_name: f.place_name, center: f.center }))
    showDropdown.value = suggestions.value.length > 0
  } catch {
    suggestions.value = []
  } finally {
    isLoadingGeo.value = false
  }
}

function selectSuggestion(s: Suggestion) {
  inputValue.value     = s.place_name
  selectedCoords.value = { lat: s.center[1], lng: s.center[0] }
  showDropdown.value   = false
  suggestions.value    = []
}

async function search() {
  // Se não tiver coords selecionadas, busca sugestões e usa a primeira
  if (!selectedCoords.value) {
    const q = inputValue.value.trim()
    if (!q) return
    if (suggestions.value.length === 0) {
      await fetchSuggestions(q)
    }
    if (suggestions.value.length === 0) return
    selectSuggestion(suggestions.value[0])
  }

  if (props.inline) {
    // Atualiza os params da rota atual sem sair da página
    router.replace({
      query: {
        ...route.query,
        local: inputValue.value,
        lat:   selectedCoords.value.lat.toFixed(6),
        lng:   selectedCoords.value.lng.toFixed(6),
        page:  '1',
      },
    })
  } else {
    router.push({
      path:  '/search',
      query: {
        local: inputValue.value,
        lat:   selectedCoords.value.lat.toFixed(6),
        lng:   selectedCoords.value.lng.toFixed(6),
      },
    })
  }
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter') search()
  if (e.key === 'Escape') showDropdown.value = false
}

function onClickOutside(e: MouseEvent) {
  const target = e.target as HTMLElement
  if (!target.closest('.search-bar')) showDropdown.value = false
}

onMounted(() => document.addEventListener('click', onClickOutside))
onUnmounted(() => document.removeEventListener('click', onClickOutside))
</script>

<template>
  <div class="search-bar" :class="{ 'search-bar--compact': compact }">
    <div class="search-bar__field">
      <svg class="search-bar__icon" width="16" height="16" viewBox="0 0 18 18" fill="none">
        <circle cx="8" cy="8" r="5.5" stroke="currentColor" stroke-width="1.6"/>
        <path d="M12.5 12.5L16 16" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
      </svg>
      <input
        v-model="inputValue"
        type="text"
        class="search-bar__input"
        placeholder="Cidade, bairro ou região…"
        autocomplete="off"
        @input="onInput"
        @keydown="onKeydown"
      />
      <span v-if="isLoadingGeo" class="search-bar__spinner" aria-hidden="true" />
    </div>

    <ul v-if="showDropdown" class="search-bar__dropdown" role="listbox">
      <li
        v-for="s in suggestions"
        :key="s.place_name"
        class="search-bar__option"
        role="option"
        @mousedown.prevent="selectSuggestion(s)"
      >
        <svg width="13" height="13" viewBox="0 0 14 14" fill="none" class="search-bar__pin">
          <path
            d="M7 1a4 4 0 0 1 4 4c0 3-4 8-4 8S3 8 3 5a4 4 0 0 1 4-4Z"
            stroke="currentColor" stroke-width="1.4"
          />
          <circle cx="7" cy="5" r="1.2" fill="currentColor"/>
        </svg>
        {{ s.place_name }}
      </li>
    </ul>

    <button
      class="search-bar__btn"
      :disabled="!selectedCoords"
      @click="search"
    >
      Buscar
    </button>
  </div>
</template>

<style scoped>
.search-bar {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  max-width: 560px;
}

/* Versão compacta para o header da página de busca */
.search-bar--compact {
  max-width: 420px;
}

.search-bar__field {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--color-surface);
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 0 14px;
  height: 52px;
  transition: border-color .2s, box-shadow .2s;
}
.search-bar--compact .search-bar__field {
  height: 40px;
  padding: 0 12px;
  gap: 8px;
}
.search-bar__field:focus-within {
  border-color: var(--color-brand);
  box-shadow: 0 0 0 3px rgba(0,106,255,.12);
}

.search-bar__icon {
  color: var(--color-text-muted);
  flex-shrink: 0;
}

.search-bar__input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 15px;
  color: var(--color-text);
  font-family: inherit;
}
.search-bar--compact .search-bar__input {
  font-size: 14px;
}
.search-bar__input::placeholder {
  color: var(--color-text-muted);
}

.search-bar__spinner {
  width: 15px;
  height: 15px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-brand);
  border-radius: 50%;
  animation: spin .7s linear infinite;
  flex-shrink: 0;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.search-bar__dropdown {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  right: 80px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  z-index: 200;
  overflow: hidden;
  list-style: none;
  margin: 0;
  padding: 4px 0;
  animation: dropdown-in .12s ease;
}

@keyframes dropdown-in {
  from { opacity: 0; transform: translateY(-4px); }
  to   { opacity: 1; transform: translateY(0); }
}

.search-bar__option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  font-size: 14px;
  color: var(--color-text);
  cursor: pointer;
  transition: background .12s;
}
.search-bar__option:hover {
  background: var(--color-bg);
}

.search-bar__pin {
  color: var(--color-text-muted);
  flex-shrink: 0;
}

.search-bar__btn {
  height: 52px;
  padding: 0 20px;
  background: var(--color-brand);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  font-family: inherit;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background .2s, transform .1s;
  white-space: nowrap;
  flex-shrink: 0;
}
.search-bar--compact .search-bar__btn {
  height: 40px;
  padding: 0 16px;
  font-size: 13px;
}
.search-bar__btn:hover:not(:disabled) {
  background: var(--color-brand-dark);
}
.search-bar__btn:active:not(:disabled) {
  transform: scale(.98);
}
.search-bar__btn:disabled {
  opacity: .5;
  cursor: not-allowed;
}
</style>
