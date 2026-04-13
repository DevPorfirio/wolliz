export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const refreshToken = getCookie(event, "refresh_token");

  if (refreshToken) {
    // Invalida o refresh token no backend (blacklist)
    await $fetch(`${config.apiBaseUrl}/api/auth/logout`, {
      method: "POST",
      body: { refresh_token: refreshToken },
    }).catch(() => {
      // Ignora erro — limpa o cookie de qualquer forma
    });
  }

  deleteCookie(event, "refresh_token");
  return { message: "Logout realizado com sucesso." };
});
