import { defineStore } from "pinia";

interface User {
  id: string;
  email: string;
  name: string;
  phone: string;
  avatar_url: string | null;
  created_at: string;
}

interface AuthState {
  user: User | null;
  accessToken: string | null;
}

export const useAuthStore = defineStore("auth", {
  state: (): AuthState => ({
    user: null,
    accessToken: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken && !!state.user,
    currentUser: (state) => state.user,
  },

  actions: {
    setAuth(token: string, user: User) {
      this.accessToken = token;
      this.user = user;
    },

    clearAuth() {
      this.accessToken = null;
      this.user = null;
    },

    updateToken(token: string) {
      this.accessToken = token;
    },
  },
});
