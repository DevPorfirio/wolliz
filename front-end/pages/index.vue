<script setup lang="ts"></script>

<template>
  <div class="home">
    <header class="header">
      <div class="header__inner">
        <AppLogo />
        <AppUserMenu />
      </div>
    </header>

    <main class="hero">
      <h1 class="hero__title">Encontre seu imóvel ideal</h1>
      <p class="hero__sub">Milhares de imóveis para comprar, vender e alugar em todo o Brasil.</p>
      <SearchBar />
    </main>

    <AppFooter />
  </div>
</template>

<style scoped>
.home {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
}

.header {
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
}

.header__inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* ── Hero ─────────────────────────────────────────────────────── */
.hero {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 64px 24px;
  gap: 20px;
}

.hero__title {
  font-size: clamp(36px, 5vw, 64px);
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -.04em;
  line-height: 1.1;
  max-width: 700px;
}

.hero__sub {
  font-size: 18px;
  color: var(--color-text-muted);
  max-width: 480px;
}
</style>
