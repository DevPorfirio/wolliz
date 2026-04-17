import mapboxgl from 'mapbox-gl'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  mapboxgl.accessToken = config.public.mapboxToken as string
  return {
    provide: { mapboxgl },
  }
})
