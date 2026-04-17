import { deleteCookie, getCookie, setCookie } from "h3";
import { useAuthStore } from "~/stores/auth";

interface DjangoRefreshResponse {
  access: string;
  refresh?: string;
}

/**
 * On app init, restores the session from the HttpOnly `refresh_token` cookie.
 * Without this, opening a new tab leaves the Pinia store empty and the user
 * appears logged out.
 *
 * SSR vs client:
 * - Server: calls Django directly and writes the rotated refresh token back
 *   to the response cookie. We can't go through `/api/auth/refresh` here
 *   because cookies set by an internal API handler don't propagate to the
 *   outer page response — so the browser would never see the new token,
 *   and the next request would 401 (since rotation blacklists the old one).
 * - Client: rare path (state usually hydrates from SSR); calls our BFF route.
 */
export default defineNuxtPlugin(async () => {
  const store = useAuthStore();
  if (store.isAuthenticated) return;

  if (import.meta.server) {
    const event = useRequestEvent();
    if (!event) return;

    const refreshToken = getCookie(event, "refresh_token");
    if (!refreshToken) return;

    const config = useRuntimeConfig();

    try {
      const tokens = await $fetch<DjangoRefreshResponse>(
        `${config.apiBaseUrl}/api/auth/token/refresh`,
        { method: "POST", body: { refresh: refreshToken } }
      );

      // Rotation: persist the new refresh token to the browser cookie.
      if (tokens.refresh) {
        setCookie(event, "refresh_token", tokens.refresh, {
          httpOnly: true,
          secure: process.env.NODE_ENV === "production",
          sameSite: "lax",
          maxAge: 60 * 60 * 24 * 7,
          path: "/",
        });
      }

      const user = await $fetch<any>(`${config.apiBaseUrl}/api/auth/me`, {
        headers: { Authorization: `Bearer ${tokens.access}` },
      });

      // Normalize avatar URL from Docker-internal hostname to public CDN.
      if (user?.avatar_url && typeof user.avatar_url === "string") {
        const cdn = (process.env.NUXT_PUBLIC_CDN_URL ?? "")
          .replace(/\/wolliz-static.*$/, "");
        user.avatar_url = user.avatar_url.replace(
          "http://minio:9000",
          cdn || "http://localhost:9000"
        );
      }

      store.setAuth(tokens.access, user);
    } catch {
      // Old/blacklisted/missing — clear the bad cookie so future requests don't loop.
      deleteCookie(event, "refresh_token");
    }
    return;
  }

  // Client (cold start without SSR state) — uses the BFF route.
  try {
    const refreshResp = await $fetch<{ access_token: string }>(
      "/api/auth/refresh",
      { method: "POST" }
    );
    const meResp = await $fetch<{ user: any }>("/api/auth/me", {
      headers: { Authorization: `Bearer ${refreshResp.access_token}` },
    });
    store.setAuth(refreshResp.access_token, meResp.user);
  } catch {
    // Visitor stays unauthenticated.
  }
});
