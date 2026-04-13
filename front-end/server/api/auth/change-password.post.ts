export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const body = await readBody(event)
  const auth = getHeader(event, 'authorization') ?? ''

  const data = await $fetch<{ message: string }>(
    `${config.apiBaseUrl}/api/auth/change-password`,
    {
      method: 'POST',
      headers: { Authorization: auth },
      body: {
        current_password: body.current_password,
        new_password:     body.new_password,
      },
    }
  ).catch((err) => {
    const status  = err?.response?.status ?? 400
    const message = err?.data?.detail ?? 'Erro ao alterar senha.'
    throw createError({ statusCode: status, message })
  })

  return data
})
