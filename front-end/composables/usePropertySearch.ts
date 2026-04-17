export interface Property {
  id:              string
  title:           string
  property_type:   'house' | 'apartment' | 'commercial' | 'land'
  listing_type:    'sale' | 'rent'
  price:           number
  price_formatted: string
  area_m2:         number
  bedrooms:        number
  bathrooms:       number
  parking_spots:   number
  latitude:        number
  longitude:       number
  address_line:    string
  city:            string
  state:           string
  cover_image_url: string | null
  distance_km:     number
}

interface SearchApiResponse {
  count:    number
  next:     string | null
  previous: string | null
  results:  Property[]
}

interface SearchState {
  results:   Property[]
  total:     number
  page:      number
  isLoading: boolean
  error:     string | null
  hoveredId: string | null
}

export const usePropertySearch = () => {
  const route  = useRoute()
  const router = useRouter()
  const config = useRuntimeConfig()

  const state = reactive<SearchState>({
    results:   [],
    total:     0,
    page:      1,
    isLoading: false,
    error:     null,
    hoveredId: null,
  })

  const searchParams = computed(() => ({
    lat:       parseFloat(route.query.lat as string),
    lng:       parseFloat(route.query.lng as string),
    local:     (route.query.local as string) || '',
    page:      parseInt((route.query.page as string) || '1', 10),
    radius_km: parseFloat((route.query.radius_km as string) || '10'),
  }))

  async function fetchProperties(params = searchParams.value): Promise<SearchApiResponse | null> {
    if (isNaN(params.lat) || isNaN(params.lng)) return null

    const baseUrl = import.meta.server ? config.apiBaseUrl : config.public.apiBaseUrl

    state.isLoading = true
    state.error     = null

    try {
      const data = await $fetch<SearchApiResponse>(`${baseUrl}/api/properties/search`, {
        query: {
          lat:       params.lat,
          lng:       params.lng,
          radius_km: params.radius_km,
          page:      params.page,
        },
      })
      state.results = data.results
      state.total   = data.count
      state.page    = params.page
      return data
    } catch (err: unknown) {
      const e = err as { data?: { detail?: string } }
      state.error = e?.data?.detail ?? 'Erro ao buscar imóveis.'
      return null
    } finally {
      state.isLoading = false
    }
  }

  function updatePage(page: number) {
    router.replace({ query: { ...route.query, page: String(page) } })
  }

  function setHovered(id: string | null) {
    state.hoveredId = id
  }

  // Reacts to URL changes: new search (lat/lng) or pagination
  watch(
    () => [route.query.lat, route.query.lng, route.query.page],
    () => fetchProperties(),
  )

  return {
    state,
    searchParams,
    fetchProperties,
    updatePage,
    setHovered,
  }
}
