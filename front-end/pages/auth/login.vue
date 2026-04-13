<script setup lang="ts">
import { useAuth } from '~/composables/useAuth'

definePageMeta({ layout: false, middleware: 'guest' })

const route = useRoute()
const router = useRouter()
const { login } = useAuth()

const email = ref((route.query.email as string) || '')
const password = ref('')
const loading = ref(false)
const error = ref('')
const showPassword = ref(false)

const emailError = ref('')
const passwordError = ref('')

function validateForm(): boolean {
  emailError.value = ''
  passwordError.value = ''
  let valid = true

  if (!email.value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    emailError.value = 'Insira um e-mail válido'
    valid = false
  }
  if (!password.value || password.value.length < 6) {
    passwordError.value = 'Senha deve ter pelo menos 6 caracteres'
    valid = false
  }
  return valid
}

async function handleSubmit() {
  if (!validateForm()) return
  loading.value = true
  error.value = ''

  try {
    await login(email.value, password.value)
    const redirect = (route.query.redirect as string) || '/'
    router.push(redirect)
  } catch (e: any) {
    error.value = e?.data?.message || e?.message || 'Credenciais inválidas. Tente novamente.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page">
    <!-- ── Left hero panel ─────────────────────────────────────── -->
    <div class="hero" aria-hidden="true">
      <div class="hero__gradient" />
      <div class="hero__grid" />

      <div class="hero__content">
        <AppLogo size="lg" inverted />

        <div class="hero__text">
          <p class="hero__eyebrow">Bem-vindo de volta</p>
          <h1 class="hero__headline">Seu próximo<br><em>lar ideal</em><br>te espera.</h1>
        </div>

        <!-- Floating property card -->
        <div class="prop-card">
          <div class="prop-card__img" />
          <div class="prop-card__body">
            <span class="prop-card__badge">Destaque</span>
            <p class="prop-card__price">R$ 1.240.000</p>
            <p class="prop-card__address">Rua das Palmeiras, 482 · Jardins, SP</p>
            <div class="prop-card__meta">
              <span>4 quartos</span>
              <span>·</span>
              <span>3 banheiros</span>
              <span>·</span>
              <span>210 m²</span>
            </div>
          </div>
        </div>

        <!-- Stats row -->
        <div class="hero__stats">
          <div class="stat">
            <strong>48k+</strong>
            <span>Imóveis</span>
          </div>
          <div class="stat__divider" />
          <div class="stat">
            <strong>120k</strong>
            <span>Famílias</span>
          </div>
          <div class="stat__divider" />
          <div class="stat">
            <strong>98%</strong>
            <span>Satisfação</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Right form panel ────────────────────────────────────── -->
    <div class="form-panel">
      <div class="form-panel__inner">
        <!-- Mobile logo -->
        <div class="mobile-logo">
          <AppLogo size="md" />
        </div>

        <header class="form-header">
          <h2 class="form-header__title">Entrar na sua conta</h2>
          <p class="form-header__sub">
            Sem conta?
            <NuxtLink to="/auth/register">Cadastre-se grátis</NuxtLink>
          </p>
        </header>

        <form class="form" @submit.prevent="handleSubmit" novalidate>

          <!-- Error banner -->
          <Transition name="fade">
            <div v-if="error" class="form__error-banner" role="alert">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <circle cx="8" cy="8" r="7.5" stroke="currentColor"/>
                <path d="M8 4.5v4M8 10.5v1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              {{ error }}
            </div>
          </Transition>

          <!-- Email -->
          <div class="field" :class="{ 'field--error': emailError }">
            <label class="field__label" for="email">E-mail</label>
            <div class="field__wrapper">
              <svg class="field__icon" width="18" height="18" viewBox="0 0 18 18" fill="none">
                <rect x="1.5" y="3.5" width="15" height="11" rx="1.5" stroke="currentColor" stroke-width="1.25"/>
                <path d="M1.5 5.5l7.5 5 7.5-5" stroke="currentColor" stroke-width="1.25" stroke-linecap="round"/>
              </svg>
              <input
                id="email"
                v-model="email"
                type="email"
                class="field__input"
                placeholder="voce@exemplo.com"
                autocomplete="email"
                autofocus
                :aria-invalid="!!emailError"
                :aria-describedby="emailError ? 'email-err' : undefined"
              />
            </div>
            <p v-if="emailError" id="email-err" class="field__message">{{ emailError }}</p>
          </div>

          <!-- Password -->
          <div class="field" :class="{ 'field--error': passwordError }">
            <div class="field__label-row">
              <label class="field__label" for="password">Senha</label>
              <NuxtLink to="/auth/forgot-password" class="field__forgot" tabindex="-1">Esqueceu a senha?</NuxtLink>
            </div>
            <div class="field__wrapper">
              <svg class="field__icon" width="18" height="18" viewBox="0 0 18 18" fill="none">
                <rect x="3.5" y="7.5" width="11" height="8" rx="1.5" stroke="currentColor" stroke-width="1.25"/>
                <path d="M6 7.5V5.5a3 3 0 1 1 6 0v2" stroke="currentColor" stroke-width="1.25" stroke-linecap="round"/>
              </svg>
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                class="field__input"
                placeholder="••••••••"
                autocomplete="current-password"
                :aria-invalid="!!passwordError"
                :aria-describedby="passwordError ? 'pw-err' : undefined"
              />
              <button
                type="button"
                class="field__toggle"
                tabindex="-1"
                @click="showPassword = !showPassword"
                :aria-label="showPassword ? 'Ocultar senha' : 'Mostrar senha'"
              >
                <svg v-if="!showPassword" width="18" height="18" viewBox="0 0 18 18" fill="none">
                  <path d="M1 9s3-6 8-6 8 6 8 6-3 6-8 6-8-6-8-6z" stroke="currentColor" stroke-width="1.25"/>
                  <circle cx="9" cy="9" r="2.5" stroke="currentColor" stroke-width="1.25"/>
                </svg>
                <svg v-else width="18" height="18" viewBox="0 0 18 18" fill="none">
                  <path d="M2 2l14 14M7.5 7.7A2.5 2.5 0 0 0 11.3 11.5M5.2 5.3C3.4 6.4 2 8 2 9s3 6 7 6c1.5 0 2.9-.5 4-1.3M9 3c4 0 7 3 7 6" stroke="currentColor" stroke-width="1.25" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
            <p v-if="passwordError" id="pw-err" class="field__message">{{ passwordError }}</p>
          </div>

          <!-- Submit -->
          <button type="submit" class="btn-submit" :disabled="loading">
            <span v-if="!loading">Entrar</span>
            <span v-else class="btn-submit__loading">
              <span class="spinner" />
              Entrando…
            </span>
          </button>

        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ── Layout ──────────────────────────────────────────────────── */
.page {
  display: flex;
  min-height: 100dvh;
  font-family: 'DM Sans', var(--font-sans);
}

/* ── Hero panel ──────────────────────────────────────────────── */
.hero {
  position: relative;
  flex: 0 0 60%;
  overflow: hidden;
  display: flex;
  align-items: stretch;
}

.hero__gradient {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 30% 70%, #0d3068 0%, transparent 60%),
    radial-gradient(ellipse 60% 80% at 80% 20%, #1a5fc8 0%, transparent 55%),
    linear-gradient(160deg, #0a1628 0%, #0d2550 40%, #061828 100%);
}

/* Blueprint grid overlay */
.hero__grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0,106,255,.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,106,255,.06) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(ellipse 100% 100% at 50% 50%, black 40%, transparent 100%);
}

.hero__content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  padding: 48px 56px;
  gap: 0;
  width: 100%;
}


.hero__text {
  margin-top: auto;
  padding-top: 80px;
}

.hero__eyebrow {
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: rgba(255,255,255,.5);
  margin-bottom: 16px;
}

.hero__headline {
  font-family: 'Fraunces', serif;
  font-size: clamp(36px, 4vw, 52px);
  font-weight: 600;
  font-style: italic;
  color: #fff;
  line-height: 1.1;
  letter-spacing: -.02em;
}

.hero__headline em {
  font-style: italic;
  background: linear-gradient(90deg, #60a5fa, #93c5fd);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Property card */
.prop-card {
  margin-top: 40px;
  background: rgba(255,255,255,.07);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255,255,255,.12);
  border-radius: 16px;
  overflow: hidden;
  width: min(340px, 90%);
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.prop-card__img {
  height: 140px;
  background:
    radial-gradient(ellipse 60% 80% at 30% 40%, rgba(37,99,235,.4), transparent),
    linear-gradient(135deg, #1a3a6c 0%, #0f2547 50%, #1e3a5f 100%);
  position: relative;
}

.prop-card__img::after {
  content: '';
  position: absolute;
  inset: 0;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='140'%3E%3Crect x='60' y='60' width='80' height='60' fill='%23ffffff10' rx='2'/%3E%3Crect x='80' y='40' width='40' height='20' fill='%23ffffff08' rx='1'/%3E%3Crect x='65' y='75' width='20' height='45' fill='%23ffffff15' rx='1'/%3E%3Crect x='115' y='80' width='20' height='40' fill='%23ffffff15' rx='1'/%3E%3Crect x='90' y='82' width='20' height='38' fill='%231a5fc8' rx='1'/%3E%3C/svg%3E") center/cover;
}

.prop-card__body {
  padding: 16px 20px;
}

.prop-card__badge {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #60a5fa;
  background: rgba(96,165,250,.15);
  border-radius: 4px;
  padding: 2px 8px;
}

.prop-card__price {
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  margin-top: 8px;
  letter-spacing: -.5px;
}

.prop-card__address {
  font-size: 12px;
  color: rgba(255,255,255,.55);
  margin-top: 4px;
}

.prop-card__meta {
  display: flex;
  gap: 6px;
  margin-top: 10px;
  font-size: 11px;
  color: rgba(255,255,255,.4);
}

/* Stats */
.hero__stats {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-top: auto;
  padding-top: 48px;
  padding-bottom: 4px;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat strong {
  font-size: 22px;
  font-weight: 700;
  color: #fff;
  letter-spacing: -.5px;
}

.stat span {
  font-size: 11px;
  color: rgba(255,255,255,.4);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.stat__divider {
  width: 1px;
  height: 32px;
  background: rgba(255,255,255,.12);
}

/* ── Form panel ──────────────────────────────────────────────── */
.form-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-surface);
  padding: 48px 24px;
}

.form-panel__inner {
  width: 100%;
  max-width: 380px;
}

.mobile-logo {
  display: none;
  align-items: center;
  gap: 10px;
  margin-bottom: 40px;
  justify-content: center;
}

/* Form header */
.form-header {
  margin-bottom: 36px;
}

.form-header__title {
  font-family: 'Fraunces', serif;
  font-size: 30px;
  font-weight: 600;
  font-style: italic;
  color: var(--color-text);
  letter-spacing: -.03em;
  line-height: 1.1;
  margin-bottom: 10px;
}

.form-header__sub {
  font-size: 14px;
  color: var(--color-text-muted);
}

.form-header__sub a {
  color: var(--color-brand);
  font-weight: 500;
}

/* Form */
.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form__error-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: var(--radius-md);
  color: var(--color-error);
  font-size: 13px;
  padding: 12px 14px;
}

/* Fields */
.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field__label-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.field__label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text);
}

.field__forgot {
  font-size: 12px;
  color: var(--color-brand);
}

.field__wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.field__icon {
  position: absolute;
  left: 14px;
  color: #9ca3af;
  pointer-events: none;
  transition: color .2s;
  flex-shrink: 0;
}

.field__input {
  width: 100%;
  height: 48px;
  padding: 0 44px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 14px;
  color: var(--color-text);
  background: var(--color-surface);
  transition: border-color .2s, box-shadow .2s;
  outline: none;
}

.field__input::placeholder {
  color: #d1d5db;
}

.field__input:focus {
  border-color: var(--color-brand);
  box-shadow: 0 0 0 3px rgba(0,106,255,.12);
}

.field__input:focus + .field__icon,
.field__wrapper:focus-within .field__icon {
  color: var(--color-brand);
}

.field--error .field__input {
  border-color: var(--color-error);
}

.field--error .field__input:focus {
  box-shadow: 0 0 0 3px rgba(220,38,38,.1);
}

.field__toggle {
  position: absolute;
  right: 14px;
  background: none;
  border: none;
  padding: 4px;
  color: #9ca3af;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: color .2s;
  border-radius: 4px;
}

.field__toggle:hover { color: var(--color-text); }

.field__message {
  font-size: 12px;
  color: var(--color-error);
  padding-left: 2px;
}

/* Submit button */
.btn-submit {
  height: 50px;
  background: var(--color-brand);
  color: #fff;
  border: none;
  border-radius: var(--radius-md);
  font-size: 15px;
  font-weight: 600;
  font-family: 'DM Sans', sans-serif;
  letter-spacing: -.1px;
  cursor: pointer;
  transition: background .2s, transform .1s, box-shadow .2s;
  box-shadow: 0 4px 14px rgba(0,106,255,.35);
}

.btn-submit:hover:not(:disabled) {
  background: var(--color-brand-dark);
  box-shadow: 0 6px 20px rgba(0,106,255,.45);
  transform: translateY(-1px);
}

.btn-submit:active:not(:disabled) {
  transform: translateY(0);
}

.btn-submit:disabled {
  opacity: .7;
  cursor: not-allowed;
}

.btn-submit__loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,.35);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin .65s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity .25s, transform .25s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

/* ── Responsive ──────────────────────────────────────────────── */
@media (max-width: 768px) {
  .page {
    flex-direction: column;
  }

  .hero {
    display: none;
  }

  .form-panel {
    align-items: flex-start;
    padding: 40px 24px;
  }

  .form-panel__inner {
    max-width: 100%;
  }

  .mobile-logo {
    display: flex;
  }

}
</style>
