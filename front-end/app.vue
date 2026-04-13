<template>
  <div>
    <NuxtPage />
  </div>
</template>

<style>
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

:root {
  --color-brand: #006AFF;
  --color-brand-dark: #0052CC;
  --color-brand-light: #E8F0FE;
  --color-text: #1A1A2E;
  --color-text-muted: #6B7280;
  --color-border: #E5E7EB;
  --color-surface: #FFFFFF;
  --color-bg: #F9FAFB;
  --color-error: #DC2626;
  --color-success: #16A34A;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --shadow-sm: 0 1px 3px rgba(0,0,0,.08);
  --shadow-md: 0 4px 16px rgba(0,0,0,.10);
  --shadow-lg: 0 8px 32px rgba(0,0,0,.12);
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
}

html, body {
  font-family: var(--font-sans);
  font-size: 16px;
  color: var(--color-text);
  background: var(--color-bg);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

a {
  color: var(--color-brand);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

button {
  font-family: inherit;
  cursor: pointer;
}

input, textarea, select {
  font-family: inherit;
}
</style>
