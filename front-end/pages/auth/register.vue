<script setup lang="ts">
import { useAuth } from '~/composables/useAuth'
import { isLocalPhoneValid, fullToLocal } from '~/composables/usePhoneInput'

definePageMeta({ layout: false, middleware: 'guest' })

const router = useRouter()
const { register } = useAuth()

const name = ref('')
const email = ref('')
const phoneFull  = ref('')
const phoneValid = computed(() =>
  !phoneFull.value || isLocalPhoneValid(fullToLocal(phoneFull.value))
)
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')
const emailExists = ref(false)
const showPassword = ref(false)
const showConfirm = ref(false)

// Field errors
const errors = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
})

// Password strength
const passwordStrength = computed(() => {
  const p = password.value
  if (!p) return 0
  let score = 0
  if (p.length >= 8) score++
  if (p.length >= 12) score++
  if (/[A-Z]/.test(p)) score++
  if (/[0-9]/.test(p)) score++
  if (/[^A-Za-z0-9]/.test(p)) score++
  return Math.min(score, 3)
})

const strengthLabel = computed(() => ['', 'Fraca', 'Média', 'Forte'][passwordStrength.value])
const strengthClass = computed(() => ['', 'weak', 'medium', 'strong'][passwordStrength.value])

function validate(): boolean {
  errors.name = ''
  errors.email = ''
  errors.password = ''
  errors.confirmPassword = ''
  let ok = true

  if (!name.value.trim() || name.value.trim().length < 2) {
    errors.name = 'Insira seu nome completo'
    ok = false
  }
  if (!email.value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    errors.email = 'Insira um e-mail válido'
    ok = false
  }
  if (!password.value || password.value.length < 8) {
    errors.password = 'Senha deve ter pelo menos 8 caracteres'
    ok = false
  }
  if (password.value !== confirmPassword.value) {
    errors.confirmPassword = 'As senhas não coincidem'
    ok = false
  }
  if (!phoneValid.value) ok = false
  return ok
}

async function handleSubmit() {
  if (!validate()) return
  loading.value = true
  error.value = ''
  emailExists.value = false

  try {
    await register({
      name: name.value.trim(),
      email: email.value,
      password: password.value,
      phone: phoneFull.value || undefined,
    })
    router.push('/')
  } catch (e: any) {
    const msg: string = e?.data?.message || e?.message || ''
    if (msg.toLowerCase().includes('já existe') || msg.toLowerCase().includes('email')) {
      emailExists.value = true
    } else {
      error.value = msg || 'Erro ao criar conta. Tente novamente.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page">

    <!-- ── Left hero ─────────────────────────────────────────── -->
    <div class="hero" aria-hidden="true">
      <div class="hero__bg" />
      <div class="hero__noise" />

      <div class="hero__content">
        <AppLogo size="lg" inverted />

        <div class="hero__text">
          <p class="hero__eyebrow">Comece hoje mesmo</p>
          <h1 class="hero__headline">Encontre o lugar<br>que vai chamar<br><em>de lar.</em></h1>
        </div>

        <!-- Stacked listing cards -->
        <div class="cards-stack">
          <div class="listing-card listing-card--back2">
            <div class="listing-card__thumb listing-card__thumb--c" />
            <div class="listing-card__info">
              <p class="listing-card__price">R$ 680.000</p>
              <p class="listing-card__loc">Vila Mariana, SP</p>
            </div>
          </div>

          <div class="listing-card listing-card--back1">
            <div class="listing-card__thumb listing-card__thumb--b" />
            <div class="listing-card__info">
              <p class="listing-card__price">R$ 890.000</p>
              <p class="listing-card__loc">Moema, SP</p>
            </div>
          </div>

          <div class="listing-card listing-card--front">
            <div class="listing-card__thumb listing-card__thumb--a" />
            <div class="listing-card__info">
              <p class="listing-card__badge">Novo</p>
              <p class="listing-card__price">R$ 1.450.000</p>
              <p class="listing-card__loc">Itaim Bibi, SP · 3 quartos · 180 m²</p>
              <div class="listing-card__tags">
                <span>Piscina</span>
                <span>Varanda</span>
                <span>Garagem</span>
              </div>
            </div>
          </div>
        </div>

        <p class="hero__note">
          Mais de <strong>48.000 imóveis</strong> em todo o Brasil
        </p>
      </div>
    </div>

    <!-- ── Right form panel ───────────────────────────────────── -->
    <div class="form-panel">
      <div class="form-panel__inner">

        <div class="mobile-logo">
          <AppLogo size="md" />
        </div>

        <header class="form-header">
          <h2 class="form-header__title">Criar sua conta</h2>
          <p class="form-header__sub">
            Já tem conta?
            <NuxtLink to="/auth/login">Entrar</NuxtLink>
          </p>
        </header>

        <form class="form" @submit.prevent="handleSubmit" novalidate>

          <!-- Email já existe — banner com ações -->
          <Transition name="fade">
            <div v-if="emailExists" class="form__email-exists-banner" role="alert">
              <div class="form__email-exists-banner__top">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                  <circle cx="8" cy="8" r="7.5" stroke="currentColor"/>
                  <path d="M8 4.5v4M8 10.5v1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
                <span>Já existe uma conta com o e-mail <strong>{{ email }}</strong>.</span>
              </div>
              <div class="form__email-exists-banner__actions">
                <NuxtLink :to="`/auth/login?email=${encodeURIComponent(email)}`" class="banner-action banner-action--primary">
                  Entrar com esta conta
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7h8M8 4l3 3-3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </NuxtLink>
                <NuxtLink to="/auth/forgot-password" class="banner-action banner-action--secondary">
                  Recuperar senha
                </NuxtLink>
              </div>
            </div>
          </Transition>

          <!-- Erro genérico -->
          <Transition name="fade">
            <div v-if="error" class="form__error-banner" role="alert">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <circle cx="8" cy="8" r="7.5" stroke="currentColor"/>
                <path d="M8 4.5v4M8 10.5v1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              {{ error }}
            </div>
          </Transition>

          <!-- Name -->
          <div class="field" :class="{ 'field--error': errors.name }">
            <label class="field__label" for="name">Nome completo</label>
            <div class="field__wrapper">
              <svg class="field__icon" width="18" height="18" viewBox="0 0 18 18" fill="none">
                <circle cx="9" cy="6" r="3.5" stroke="currentColor" stroke-width="1.25"/>
                <path d="M2.5 15.5c0-3.314 2.91-6 6.5-6s6.5 2.686 6.5 6" stroke="currentColor" stroke-width="1.25" stroke-linecap="round"/>
              </svg>
              <input
                id="name"
                v-model="name"
                type="text"
                class="field__input"
                placeholder="Maria Silva"
                autocomplete="name"
                autofocus
                :aria-invalid="!!errors.name"
              />
            </div>
            <p v-if="errors.name" class="field__message">{{ errors.name }}</p>
          </div>

          <!-- Email -->
          <div class="field" :class="{ 'field--error': errors.email }">
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
                :aria-invalid="!!errors.email"
              />
            </div>
            <p v-if="errors.email" class="field__message">{{ errors.email }}</p>
          </div>

          <!-- Phone (optional) -->
          <div class="field">
            <label class="field__label">
              Telefone <span class="field__optional">(opcional)</span>
            </label>
            <AppPhoneInput v-model="phoneFull" />
          </div>

          <!-- Password -->
          <div class="field" :class="{ 'field--error': errors.password }">
            <label class="field__label" for="password">Senha</label>
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
                placeholder="Mínimo 8 caracteres"
                autocomplete="new-password"
                :aria-invalid="!!errors.password"
              />
              <button
                type="button"
                class="field__toggle"
                tabindex="-1"
                @click="showPassword = !showPassword"
                :aria-label="showPassword ? 'Ocultar senha' : 'Mostrar senha'"
              >
                <svg v-if="!showPassword" width="16" height="16" viewBox="0 0 18 18" fill="none">
                  <path d="M1 9s3-6 8-6 8 6 8 6-3 6-8 6-8-6-8-6z" stroke="currentColor" stroke-width="1.25"/>
                  <circle cx="9" cy="9" r="2.5" stroke="currentColor" stroke-width="1.25"/>
                </svg>
                <svg v-else width="16" height="16" viewBox="0 0 18 18" fill="none">
                  <path d="M2 2l14 14M7.5 7.7A2.5 2.5 0 0 0 11.3 11.5M5.2 5.3C3.4 6.4 2 8 2 9s3 6 7 6c1.5 0 2.9-.5 4-1.3M9 3c4 0 7 3 7 6" stroke="currentColor" stroke-width="1.25" stroke-linecap="round"/>
                </svg>
              </button>
            </div>

            <!-- Strength bar -->
            <div v-if="password" class="strength">
              <div class="strength__bars">
                <span
                  v-for="i in 3"
                  :key="i"
                  class="strength__bar"
                  :class="{ active: passwordStrength >= i, [strengthClass]: passwordStrength >= i }"
                />
              </div>
              <span class="strength__label" :class="strengthClass">{{ strengthLabel }}</span>
            </div>

            <p v-if="errors.password" class="field__message">{{ errors.password }}</p>
          </div>

          <!-- Confirm password -->
          <div class="field" :class="{ 'field--error': errors.confirmPassword }">
            <label class="field__label" for="confirm">Confirmar senha</label>
            <div class="field__wrapper">
              <svg class="field__icon" width="18" height="18" viewBox="0 0 18 18" fill="none">
                <path d="M4 9l4 4 6-7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="9" cy="9" r="7.5" stroke="currentColor" stroke-width="1.25"/>
              </svg>
              <input
                id="confirm"
                v-model="confirmPassword"
                :type="showConfirm ? 'text' : 'password'"
                class="field__input"
                placeholder="Repita a senha"
                autocomplete="new-password"
                :aria-invalid="!!errors.confirmPassword"
              />
              <button
                type="button"
                class="field__toggle"
                tabindex="-1"
                @click="showConfirm = !showConfirm"
                aria-label="Alternar visibilidade"
              >
                <svg v-if="!showConfirm" width="16" height="16" viewBox="0 0 18 18" fill="none">
                  <path d="M1 9s3-6 8-6 8 6 8 6-3 6-8 6-8-6-8-6z" stroke="currentColor" stroke-width="1.25"/>
                  <circle cx="9" cy="9" r="2.5" stroke="currentColor" stroke-width="1.25"/>
                </svg>
                <svg v-else width="16" height="16" viewBox="0 0 18 18" fill="none">
                  <path d="M2 2l14 14M7.5 7.7A2.5 2.5 0 0 0 11.3 11.5M5.2 5.3C3.4 6.4 2 8 2 9s3 6 7 6c1.5 0 2.9-.5 4-1.3M9 3c4 0 7 3 7 6" stroke="currentColor" stroke-width="1.25" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
            <p v-if="errors.confirmPassword" class="field__message">{{ errors.confirmPassword }}</p>
          </div>

          <p class="form__terms">
            Ao criar sua conta você concorda com os
            <NuxtLink to="/terms" target="_blank" tabindex="-1">Termos de Uso</NuxtLink> e a
            <NuxtLink to="/privacy" target="_blank" tabindex="-1">Política de Privacidade</NuxtLink> do Wolliz.
          </p>

          <button type="submit" class="btn-submit" :disabled="loading">
            <span v-if="!loading">Criar conta grátis</span>
            <span v-else class="btn-submit__loading">
              <span class="spinner" />
              Criando conta…
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

/* ── Hero ────────────────────────────────────────────────────── */
.hero {
  position: relative;
  flex: 0 0 60%;
  overflow: hidden;
  display: flex;
  align-items: stretch;
}

.hero__bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 70% 50% at 20% 30%, #0a3d7a 0%, transparent 60%),
    radial-gradient(ellipse 80% 60% at 80% 80%, #092d5e 0%, transparent 55%),
    linear-gradient(155deg, #071525 0%, #0c2448 45%, #081b3a 100%);
}

.hero__noise {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0,106,255,.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,106,255,.04) 1px, transparent 1px);
  background-size: 56px 56px;
}

.hero__content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  padding: 48px 56px 48px;
  width: 100%;
}


/* Hero text */
.hero__text {
  margin-top: 52px;
}

.hero__eyebrow {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: rgba(255,255,255,.45);
  margin-bottom: 14px;
}

.hero__headline {
  font-family: 'Fraunces', serif;
  font-size: clamp(32px, 3.5vw, 48px);
  font-weight: 600;
  font-style: italic;
  color: #fff;
  line-height: 1.12;
  letter-spacing: -.02em;
}

.hero__headline em {
  font-style: italic;
  background: linear-gradient(90deg, #60a5fa, #a5f3fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Stacked cards */
.cards-stack {
  position: relative;
  margin-top: 40px;
  height: 220px;
}

.listing-card {
  position: absolute;
  background: rgba(255,255,255,.06);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,.1);
  border-radius: 14px;
  overflow: hidden;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 0 16px 0 0;
  width: 88%;
  height: 80px;
  transition: transform .3s ease;
}

.listing-card--front {
  bottom: 0;
  left: 0;
  z-index: 3;
  height: 108px;
  background: rgba(255,255,255,.1);
  border-color: rgba(255,255,255,.18);
}

.listing-card--back1 {
  bottom: 96px;
  left: 24px;
  z-index: 2;
  opacity: .7;
  transform: scale(.97);
}

.listing-card--back2 {
  bottom: 166px;
  left: 42px;
  z-index: 1;
  opacity: .45;
  transform: scale(.94);
}

.listing-card__thumb {
  flex-shrink: 0;
  width: 72px;
  height: 100%;
  border-radius: 10px 0 0 10px;
}

.listing-card--front .listing-card__thumb {
  width: 80px;
}

.listing-card__thumb--a {
  background: linear-gradient(135deg, #1a4080 0%, #0d2d65 50%, #1565c0 100%);
  position: relative;
}

.listing-card__thumb--a::after {
  content: '';
  position: absolute;
  inset: 0;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='92'%3E%3Crect x='15' y='40' width='50' height='40' fill='%23ffffff0c' rx='2'/%3E%3Crect x='25' y='28' width='30' height='12' fill='%23ffffff08'/%3E%3Crect x='18' y='52' width='14' height='28' fill='%23ffffff12' rx='1'/%3E%3Crect x='48' y='56' width='14' height='24' fill='%23ffffff12' rx='1'/%3E%3Crect x='33' y='58' width='14' height='22' fill='%231a5fc840' rx='1'/%3E%3C/svg%3E") center/cover;
}

.listing-card__thumb--b {
  background: linear-gradient(135deg, #0e3558 0%, #1a4a7a 100%);
}

.listing-card__thumb--c {
  background: linear-gradient(135deg, #0a2540 0%, #163456 100%);
}

.listing-card__info {
  flex: 1;
  min-width: 0;
}

.listing-card__badge {
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: #34d399;
  background: rgba(52,211,153,.15);
  border-radius: 3px;
  padding: 2px 6px;
  display: inline-block;
  margin-bottom: 4px;
}

.listing-card__price {
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  letter-spacing: -.4px;
}

.listing-card--back1 .listing-card__price,
.listing-card--back2 .listing-card__price {
  font-size: 14px;
}

.listing-card__loc {
  font-size: 11px;
  color: rgba(255,255,255,.45);
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.listing-card__tags {
  display: flex;
  gap: 5px;
  margin-top: 7px;
  flex-wrap: nowrap;
  overflow: hidden;
}

.listing-card__tags span {
  font-size: 10px;
  color: rgba(255,255,255,.5);
  background: rgba(255,255,255,.07);
  border-radius: 4px;
  padding: 2px 7px;
}

.hero__note {
  margin-top: auto;
  padding-top: 32px;
  font-size: 13px;
  color: rgba(255,255,255,.35);
}

.hero__note strong {
  color: rgba(255,255,255,.65);
  font-weight: 600;
}

/* ── Form panel ──────────────────────────────────────────────── */
.form-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-surface);
  padding: 40px 24px;
  overflow-y: auto;
}

.form-panel__inner {
  width: 100%;
  max-width: 380px;
}

.mobile-logo {
  display: none;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 36px;
}


/* Form header */
.form-header {
  margin-bottom: 28px;
}

.form-header__title {
  font-family: 'Fraunces', serif;
  font-size: 28px;
  font-weight: 600;
  font-style: italic;
  color: var(--color-text);
  letter-spacing: -.03em;
  margin-bottom: 8px;
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
  gap: 16px;
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

/* Banner email já existe */
.form__email-exists-banner {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: var(--radius-md);
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.form__email-exists-banner__top {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  color: #1d4ed8;
  font-size: 13px;
  line-height: 1.5;
}

.form__email-exists-banner__top svg {
  flex-shrink: 0;
  margin-top: 1px;
}

.form__email-exists-banner__actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.banner-action {
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: opacity .15s;
}

.banner-action:hover { opacity: .8; text-decoration: none; }

.banner-action--primary {
  color: #fff;
  background: var(--color-brand);
  padding: 7px 14px;
  border-radius: var(--radius-sm);
}

.banner-action--secondary {
  color: var(--color-brand);
  padding: 7px 0;
}

/* Fields */
.field {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.field__label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text);
}

.field__optional {
  font-weight: 400;
  color: var(--color-text-muted);
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
}

.field__input {
  width: 100%;
  height: 46px;
  padding: 0 44px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 14px;
  color: var(--color-text);
  background: var(--color-surface);
  transition: border-color .2s, box-shadow .2s;
  outline: none;
  font-family: 'DM Sans', sans-serif;
}

.field__input::placeholder {
  color: #d1d5db;
}

.field__input:focus {
  border-color: var(--color-brand);
  box-shadow: 0 0 0 3px rgba(0,106,255,.1);
}

.field--error .field__input {
  border-color: var(--color-error);
}

.field--error .field__input:focus {
  box-shadow: 0 0 0 3px rgba(220,38,38,.1);
}

.field__toggle {
  position: absolute;
  right: 12px;
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

/* Strength meter */
.strength {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 2px;
}

.strength__bars {
  display: flex;
  gap: 4px;
}

.strength__bar {
  width: 40px;
  height: 3px;
  border-radius: 99px;
  background: var(--color-border);
  transition: background .3s;
}

.strength__bar.active.weak   { background: #ef4444; }
.strength__bar.active.medium { background: #f59e0b; }
.strength__bar.active.strong { background: #22c55e; }

.strength__label {
  font-size: 11px;
  font-weight: 500;
}

.strength__label.weak   { color: #ef4444; }
.strength__label.medium { color: #f59e0b; }
.strength__label.strong { color: #22c55e; }

/* Terms */
.form__terms {
  font-size: 12px;
  color: var(--color-text-muted);
  line-height: 1.6;
}

.form__terms a {
  color: var(--color-brand);
}

/* Submit */
.btn-submit {
  height: 50px;
  background: var(--color-brand);
  color: #fff;
  border: none;
  border-radius: var(--radius-md);
  font-size: 15px;
  font-weight: 600;
  font-family: 'DM Sans', sans-serif;
  cursor: pointer;
  transition: background .2s, transform .1s, box-shadow .2s;
  box-shadow: 0 4px 14px rgba(0,106,255,.3);
}

.btn-submit:hover:not(:disabled) {
  background: var(--color-brand-dark);
  box-shadow: 0 6px 20px rgba(0,106,255,.4);
  transform: translateY(-1px);
}

.btn-submit:active:not(:disabled) { transform: translateY(0); }

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

@keyframes spin { to { transform: rotate(360deg); } }

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
  .page { flex-direction: column; }

  .hero { display: none; }

  .form-panel {
    align-items: flex-start;
    padding: 40px 24px;
  }

  .form-panel__inner { max-width: 100%; }

  .mobile-logo { display: flex; }

}
</style>
