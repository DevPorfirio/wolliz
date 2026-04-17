<script setup lang="ts">
import { useAuth } from '~/composables/useAuth'

const { isAuthenticated, user, logout } = useAuth()

const menuOpen = ref(false)

function getInitials(name: string) {
  return name.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase()
}

function closeMenu(e: MouseEvent) {
  const target = e.target as HTMLElement
  if (!target.closest('.user-menu')) menuOpen.value = false
}

onMounted(() => document.addEventListener('click', closeMenu))
onUnmounted(() => document.removeEventListener('click', closeMenu))
</script>

<template>
  <div class="user-nav">
    <!-- Visitante -->
    <template v-if="!isAuthenticated">
      <NuxtLink to="/auth/login" class="btn-link">Entrar</NuxtLink>
      <NuxtLink to="/auth/register" class="btn-primary">Criar conta</NuxtLink>
    </template>

    <!-- Logado -->
    <div v-else class="user-menu">
      <button class="user-menu__trigger" @click.stop="menuOpen = !menuOpen">
        <img v-if="user?.avatar_url" :src="user.avatar_url" class="user-menu__avatar user-menu__avatar--photo" alt="Foto de perfil" />
        <span v-else class="user-menu__avatar">{{ getInitials(user?.name ?? '') }}</span>
        <span class="user-menu__email">{{ user?.email }}</span>
        <svg class="user-menu__chevron" :class="{ 'user-menu__chevron--open': menuOpen }"
             width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M3 5l4 4 4-4" stroke="currentColor" stroke-width="1.5"
                stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>

      <div v-if="menuOpen" class="user-menu__dropdown">
        <div class="user-menu__header">
          <img v-if="user?.avatar_url" :src="user.avatar_url" class="user-menu__avatar user-menu__avatar--lg user-menu__avatar--photo" alt="Foto de perfil" />
          <span v-else class="user-menu__avatar user-menu__avatar--lg">{{ getInitials(user?.name ?? '') }}</span>
          <div class="user-menu__header-text">
            <p class="user-menu__full-name">{{ user?.name }}</p>
            <p class="user-menu__full-email">{{ user?.email }}</p>
          </div>
        </div>

        <div class="user-menu__divider" />

        <NuxtLink to="/profile" class="user-menu__item" @click="menuOpen = false">
          <svg width="15" height="15" viewBox="0 0 15 15" fill="none">
            <circle cx="7.5" cy="5" r="2.5" stroke="currentColor" stroke-width="1.4"/>
            <path d="M2 13c0-3 2.5-5 5.5-5s5.5 2 5.5 5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
          </svg>
          Meu perfil
        </NuxtLink>

        <div class="user-menu__divider" />

        <button class="user-menu__item user-menu__item--danger" @click="logout">
          <svg width="15" height="15" viewBox="0 0 15 15" fill="none">
            <path d="M6 13H3a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1h3M10 10l3-2.5L10 5M13 7.5H6"
                  stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Sair da conta
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.user-nav {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-link {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text);
  padding: 8px 14px;
  border-radius: var(--radius-sm);
  transition: background .2s;
  text-decoration: none;
}
.btn-link:hover {
  background: var(--color-bg);
  text-decoration: none;
}

.btn-primary {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  background: var(--color-brand);
  padding: 8px 18px;
  border-radius: var(--radius-sm);
  transition: background .2s;
  text-decoration: none;
}
.btn-primary:hover {
  background: var(--color-brand-dark);
  text-decoration: none;
}

/* ── User menu ──────────────────────────────────────────────── */
.user-menu {
  position: relative;
}

.user-menu__trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  padding: 5px 12px 5px 5px;
  cursor: pointer;
  transition: border-color .2s, box-shadow .2s;
  color: var(--color-text);
  font-family: inherit;
}
.user-menu__trigger:hover {
  border-color: #c0c9d6;
  box-shadow: var(--shadow-sm);
}

.user-menu__avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--color-brand);
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  letter-spacing: .3px;
}

.user-menu__avatar--lg {
  width: 38px;
  height: 38px;
  font-size: 14px;
  flex-shrink: 0;
}

.user-menu__avatar--photo {
  object-fit: cover;
  background: none;
  font-size: 0;
}

.user-menu__email {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text);
  white-space: nowrap;
}

.user-menu__chevron {
  color: var(--color-text-muted);
  transition: transform .2s;
  flex-shrink: 0;
}
.user-menu__chevron--open {
  transform: rotate(180deg);
}

.user-menu__dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 260px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  z-index: 100;
  overflow: hidden;
  animation: dropdown-in .15s ease;
}

@keyframes dropdown-in {
  from { opacity: 0; transform: translateY(-6px); }
  to   { opacity: 1; transform: translateY(0); }
}

.user-menu__header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
}

.user-menu__header-text {
  min-width: 0;
  flex: 1;
}

.user-menu__full-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-menu__full-email {
  font-size: 12px;
  color: var(--color-text-muted);
  margin-top: 2px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-menu__divider {
  height: 1px;
  background: var(--color-border);
  margin: 0;
}

.user-menu__item {
  display: flex;
  align-items: center;
  gap: 9px;
  width: 100%;
  padding: 11px 16px;
  background: none;
  border: none;
  font-size: 14px;
  color: var(--color-text);
  cursor: pointer;
  text-align: left;
  transition: background .15s;
  font-family: inherit;
  text-decoration: none;
}
.user-menu__item:hover {
  background: var(--color-bg);
}
.user-menu__item--danger {
  color: var(--color-error);
}
.user-menu__item--danger:hover {
  background: #fef2f2;
}

/* On narrow viewports, hide the email and only show avatar + chevron */
@media (max-width: 600px) {
  .user-menu__email {
    display: none;
  }
  .user-menu__trigger {
    padding: 5px 10px 5px 5px;
  }
}
</style>
