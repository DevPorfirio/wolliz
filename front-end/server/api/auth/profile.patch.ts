export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const body = await readBody(event)
  const authHeader = getHeader(event, 'authorization')

  if (!authHeader) throw createError({ statusCode: 401, message: 'Não autenticado.' })

  const data = await $fetch(`${config.apiBaseUrl}/api/auth/profile`, {
    method: 'PATCH',
    headers: { Authorization: authHeader },
    body,
  }).catch((err) => {
    throw createError({ statusCode: err?.response?.status ?? 400, message: err?.data?.detail ?? 'Erro ao atualizar perfil.' })
  })

  return fixAvatarUrl(data)
})
