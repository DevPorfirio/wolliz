export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const authorization = getHeader(event, "authorization");

  if (!authorization) {
    throw createError({ statusCode: 401, message: "Não autenticado." });
  }

  const user = await $fetch<any>(`${config.apiBaseUrl}/api/auth/me`, {
    headers: { Authorization: authorization },
  }).catch((err) => {
    throw createError({
      statusCode: err?.response?.status ?? 401,
      message: "Token inválido.",
    });
  });

  return { user: fixAvatarUrl(user) };
});
