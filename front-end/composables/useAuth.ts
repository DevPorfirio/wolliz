import { useAuthStore } from "~/stores/auth";

export const useAuth = () => {
  const store = useAuthStore();
  const router = useRouter();

  async function login(email: string, password: string) {
    const data = await $fetch<{ access_token: string; user: any }>(
      "/api/auth/login",
      {
        method: "POST",
        body: { email, password },
      }
    );
    store.setAuth(data.access_token, data.user);
    return data;
  }

  async function register(payload: {
    email: string;
    name: string;
    password: string;
    phone?: string;
  }) {
    // Cria a conta
    await $fetch("/api/auth/register", {
      method: "POST",
      body: payload,
    });
    // Já loga com as mesmas credenciais — sem precisar ir para /login
    return await login(payload.email, payload.password);
  }

  async function logout() {
    try {
      await $fetch("/api/auth/logout", { method: "POST" });
    } finally {
      store.clearAuth();
      router.push("/auth/login");
    }
  }

  async function refreshToken() {
    try {
      const data = await $fetch<{ access_token: string }>(
        "/api/auth/refresh",
        { method: "POST" }
      );
      store.updateToken(data.access_token);
      return data.access_token;
    } catch {
      store.clearAuth();
      throw new Error("Sessão expirada.");
    }
  }

  async function fetchMe() {
    if (!store.accessToken) return null;
    const data = await $fetch<{ user: any }>("/api/auth/me", {
      headers: { Authorization: `Bearer ${store.accessToken}` },
    });
    if (data.user) store.user = data.user;
    return data.user;
  }

  return {
    login,
    register,
    logout,
    refreshToken,
    fetchMe,
    isAuthenticated: computed(() => store.isAuthenticated),
    user: computed(() => store.currentUser),
  };
};
