export default defineNuxtConfig({
  // SSR ativo — servidor Node renderiza e envia HTML pro cliente
  ssr: true,

  devtools: { enabled: true },

  modules: ["@pinia/nuxt"],

  // URL do CDN/MinIO para assets estáticos (JS/CSS bundles)
  // Em produção aponta para o bucket MinIO público
  app: {
    cdnURL: process.env.NUXT_PUBLIC_CDN_URL || "",
    head: {
      title: "Wolliz — Encontre seu imóvel",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        {
          name: "description",
          content: "Wolliz é o marketplace para você comprar, vender e alugar imóveis.",
        },
      ],
      link: [
        { rel: "preconnect", href: "https://fonts.googleapis.com" },
        { rel: "preconnect", href: "https://fonts.gstatic.com", crossorigin: "" },
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=Fraunces:ital,opsz,wght@1,9..144,600&display=swap",
        },
        { rel: "icon", type: "image/x-icon", href: "/favicon.ico" },
        { rel: "icon", type: "image/svg+xml", href: "/favicon.svg" },
        { rel: "apple-touch-icon", href: "/apple-touch-icon.png" },
        {
          rel:  "stylesheet",
          href: "https://api.mapbox.com/mapbox-gl-js/v3.10.0/mapbox-gl.css",
        },
      ],
    },
  },

  // Runtime config — exposto ao servidor e ao cliente conforme necessário
  runtimeConfig: {
    // Apenas server-side: URL interna do Docker para o backend
    apiBaseUrl: process.env.NUXT_API_BASE_URL || "http://backend:8000",

    // Público: acessível no browser também
    public: {
      apiBaseUrl:  process.env.NUXT_PUBLIC_API_BASE_URL || "http://localhost:8000",
      cdnUrl:      process.env.NUXT_PUBLIC_CDN_URL      || "http://localhost:9000/wolliz-static",
      mapboxToken: process.env.NUXT_PUBLIC_MAPBOX_TOKEN || "",
    },
  },

  nitro: {
    // Em produção, o output do servidor fica em .output/server
    // Os assets estáticos (.output/public/_nuxt/) são enviados pro MinIO
  },

  typescript: {
    strict: true,
  },
});
