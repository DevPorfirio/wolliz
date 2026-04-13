export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const authHeader = getHeader(event, 'authorization')

  if (!authHeader) throw createError({ statusCode: 401, message: 'Não autenticado.' })

  // Forward the multipart/form-data directly to Django
  const body = await readRawBody(event, false)
  const contentType = getHeader(event, 'content-type') ?? ''

  const data = await $fetch(`${config.apiBaseUrl}/api/auth/avatar`, {
    method: 'POST',
    headers: {
      Authorization: authHeader,
      'content-type': contentType,
    },
    body,
  }).catch((err) => {
    throw createError({ statusCode: err?.response?.status ?? 400, message: err?.data?.detail ?? 'Erro ao fazer upload.' })
  })

  return fixAvatarUrl(data)
})
