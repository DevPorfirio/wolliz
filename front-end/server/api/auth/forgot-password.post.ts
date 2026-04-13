// BFF: recebe e-mail, repassa ao Django.
// Por segurança, sempre retorna 200 independente de o e-mail existir.

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const body = await readBody(event)

  await $fetch(`${config.apiBaseUrl}/api/auth/forgot-password`, {
    method: 'POST',
    body: { email: body.email },
  }).catch(() => {
    // Silencia erros — não vaza se o e-mail existe ou não
  })

  return { message: 'Se este e-mail estiver cadastrado, você receberá as instruções em breve.' }
})
