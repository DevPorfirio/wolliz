<script setup lang="ts">
const year = new Date().getFullYear()

withDefaults(defineProps<{
  compact?: boolean
}>(), {
  compact: false,
})
</script>

<template>
  <footer class="app-footer" :class="{ 'app-footer--compact': compact }">
    <div class="app-footer__inner">
      <div class="app-footer__brand">
        <AppLogo size="sm" />
        <p class="app-footer__tag">Encontre seu imóvel ideal.</p>
      </div>

      <nav class="app-footer__nav" aria-label="Rodapé">
        <NuxtLink to="/" class="app-footer__link">Início</NuxtLink>
        <NuxtLink to="/search" class="app-footer__link">Buscar imóveis</NuxtLink>
        <NuxtLink to="/privacy" class="app-footer__link">Privacidade</NuxtLink>
        <NuxtLink to="/terms" class="app-footer__link">Termos</NuxtLink>
      </nav>

      <p class="app-footer__copy">
        © {{ year }} Wolliz · Todos os direitos reservados
      </p>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  border-top: 1px solid var(--color-border);
  background: var(--color-surface);
  padding: 24px;
  flex-shrink: 0;
}

.app-footer__inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}

.app-footer__brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.app-footer__tag {
  font-size: 13px;
  color: var(--color-text-muted);
  border-left: 1px solid var(--color-border);
  padding-left: 12px;
  line-height: 1;
}

.app-footer__nav {
  display: flex;
  gap: 18px;
  flex-wrap: wrap;
}

.app-footer__link {
  font-size: 13px;
  color: var(--color-text-muted);
  text-decoration: none;
  transition: color .15s;
}
.app-footer__link:hover {
  color: var(--color-text);
}

.app-footer__copy {
  font-size: 12px;
  color: var(--color-text-muted);
  white-space: nowrap;
}

/* Compact variant — used on app-shell pages like /search */
.app-footer--compact {
  padding: 12px 24px;
}
.app-footer--compact .app-footer__tag {
  display: none;
}

@media (max-width: 768px) {
  .app-footer__inner {
    flex-direction: column;
    align-items: flex-start;
    gap: 14px;
  }
  .app-footer__tag {
    display: none;
  }
}
</style>
