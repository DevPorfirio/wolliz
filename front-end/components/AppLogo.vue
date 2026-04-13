<script setup lang="ts">
withDefaults(defineProps<{
  size?: 'sm' | 'md' | 'lg'
  inverted?: boolean
}>(), {
  size: 'md',
  inverted: false,
})
</script>

<template>
  <div class="app-logo" :class="[`app-logo--${size}`, { 'app-logo--inverted': inverted }]">
    <span class="app-logo__icon" aria-hidden="true">W</span>
    <span class="app-logo__name">Wolliz</span>
  </div>
</template>

<style scoped>
.app-logo {
  display: flex;
  align-items: center;
  gap: 9px;
  user-select: none;
}

.app-logo__icon {
  flex-shrink: 0;
  background: #006AFF;
  color: #fff;
  font-family: 'Fraunces', serif;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 7px;
}

.app-logo__name {
  font-weight: 600;
  letter-spacing: -.3px;
  color: var(--color-text);
}

/* Size variants */
.app-logo--sm .app-logo__icon  { width: 28px; height: 28px; font-size: 15px; }
.app-logo--sm .app-logo__name  { font-size: 15px; }

.app-logo--md .app-logo__icon  { width: 32px; height: 32px; font-size: 17px; }
.app-logo--md .app-logo__name  { font-size: 17px; }

.app-logo--lg .app-logo__icon  { width: 36px; height: 36px; font-size: 20px; border-radius: 8px; }
.app-logo--lg .app-logo__name  { font-size: 20px; }

/* Inverted: white text for dark hero backgrounds */
.app-logo--inverted .app-logo__name { color: #fff; }
</style>
