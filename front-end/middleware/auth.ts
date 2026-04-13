import { useAuthStore } from "~/stores/auth";

export default defineNuxtRouteMiddleware((to) => {
  const store = useAuthStore();

  if (!store.isAuthenticated) {
    return navigateTo(`/auth/login?redirect=${to.fullPath}`);
  }
});
