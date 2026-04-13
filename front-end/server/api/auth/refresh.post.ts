export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const refreshToken = getCookie(event, "refresh_token");

  if (!refreshToken) {
    throw createError({ statusCode: 401, message: "Sem refresh token." });
  }

  const response = await $fetch<{ access: string }>(
    `${config.apiBaseUrl}/api/token/refresh`,
    {
      method: "POST",
      body: { refresh: refreshToken },
    }
  ).catch((err) => {
    // Token expirado ou inválido — limpa o cookie
    deleteCookie(event, "refresh_token");
    throw createError({ statusCode: 401, message: "Sessão expirada. Faça login novamente." });
  });

  return { access_token: response.access };
});
