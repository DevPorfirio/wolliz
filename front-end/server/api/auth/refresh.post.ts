export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const refreshToken = getCookie(event, "refresh_token");

  if (!refreshToken) {
    throw createError({ statusCode: 401, message: "Sem refresh token." });
  }

  // Django rotates refresh tokens (ROTATE_REFRESH_TOKENS=True), so the
  // response includes a new `refresh` and the old one gets blacklisted.
  // We must save the new one back to the cookie or the next refresh 401s.
  const response = await $fetch<{ access: string; refresh?: string }>(
    `${config.apiBaseUrl}/api/auth/token/refresh`,
    {
      method: "POST",
      body: { refresh: refreshToken },
    }
  ).catch(() => {
    deleteCookie(event, "refresh_token");
    throw createError({ statusCode: 401, message: "Sessão expirada. Faça login novamente." });
  });

  if (response.refresh) {
    setCookie(event, "refresh_token", response.refresh, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      maxAge: 60 * 60 * 24 * 7,
      path: "/",
    });
  }

  return { access_token: response.access };
});
