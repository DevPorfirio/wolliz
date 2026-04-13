// BFF: browser → Nuxt server → Django
// O Nuxt server recebe as credenciais, chama o Django,
// seta o refresh token em HttpOnly cookie e devolve apenas o access token.

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const body = await readBody(event);

  const response = await $fetch<{ access: string; refresh: string }>(
    `${config.apiBaseUrl}/api/auth/token`,
    {
      method: "POST",
      body: { email: body.email, password: body.password },
    }
  ).catch((err) => {
    const status = err?.response?.status ?? 401;
    const detail = err?.data?.detail ?? "Credenciais inválidas.";
    throw createError({ statusCode: status, message: detail });
  });

  // Refresh token em HttpOnly cookie — o browser nunca vê esse token
  setCookie(event, "refresh_token", response.refresh, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    maxAge: 60 * 60 * 24 * 7, // 7 dias
    path: "/",
  });

  // Busca dados do usuário
  const user = await $fetch<any>(`${config.apiBaseUrl}/api/auth/me`, {
    headers: { Authorization: `Bearer ${response.access}` },
  }).catch(() => null);

  return {
    access_token: response.access,
    user: fixAvatarUrl(user),
  };
});
