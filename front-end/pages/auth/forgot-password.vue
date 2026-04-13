<script setup lang="ts">
definePageMeta({ layout: false, middleware: 'guest' })
useHead({ title: 'Recuperar senha — Wolliz' })

const router = useRouter()

const email   = ref('')
const loading = ref(false)
const emailError = ref('')
const showModal  = ref(false)

function validateEmail(): boolean {
  emailError.value = ''
  if (!email.value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    emailError.value = 'Insira um e-mail válido'
    return false
  }
  return true
}

async function handleSubmit() {
  if (!validateEmail()) return
  loading.value = true
  try {
    await $fetch('/api/auth/forgot-password', {
      method: 'POST',
      body: { email: email.value },
    })
  } catch {
    // Sempre mostra o modal — não vaza informação
  } finally {
    loading.value = false
    showModal.value = true
  }
}

function onModalOk() {
  showModal.value = false
  router.push('/auth/login')
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
          <p class="hero__eyebrow">Recuperação de acesso</p>
          <h1 class="hero__headline">Sua chave<br>de volta<br><em>está aqui.</em></h1>
        </div>

        <!-- Lock card -->
        <div class="lock-card">
          <div class="lock-card__icon-wrap">
            <svg class="lock-card__lock" width="36" height="36" viewBox="0 0 36 36" fill="none">
              <rect x="6" y="16" width="24" height="17" rx="3" fill="rgba(255,255,255,.12)" stroke="rgba(255,255,255,.3)" stroke-width="1.5"/>
              <path d="M11 16v-5a7 7 0 1 1 14 0v5" stroke="rgba(255,255,255,.5)" stroke-width="1.5" stroke-linecap="round"/>
              <circle cx="18" cy="24.5" r="2.5" fill="rgba(96,165,250,.8)"/>
              <rect x="16.5" y="24.5" width="3" height="4" rx="1" fill="rgba(96,165,250,.8)"/>
            </svg>
            <div class="lock-card__pulse" />
          </div>
          <p class="lock-card__title">Esqueceu sua senha?</p>
          <p class="lock-card__desc">Não tem problema. Informe seu e-mail e enviaremos as instruções para você criar uma nova senha com segurança.</p>

          <div class="lock-card__steps">
            <div class="lock-card__step">
              <span class="lock-card__step-num">1</span>
              <span>Informe seu e-mail</span>
            </div>
            <div class="lock-card__step-line" />
            <div class="lock-card__step">
              <span class="lock-card__step-num">2</span>
              <span>Receba o link</span>
            </div>
            <div class="lock-card__step-line" />
            <div class="lock-card__step">
              <span class="lock-card__step-num">3</span>
              <span>Crie nova senha</span>
            </div>
          </div>
        </div>

        <p class="hero__footer">
          Seus dados estão protegidos com criptografia de ponta a ponta.
        </p>
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
          <div class="form-header__icon">
            <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
              <rect x="3" y="10" width="16" height="11" rx="2" stroke="var(--color-brand)" stroke-width="1.5"/>
              <path d="M7 10V7a4 4 0 0 1 8 0v3" stroke="var(--color-brand)" stroke-width="1.5" stroke-linecap="round"/>
              <circle cx="11" cy="15.5" r="1.5" fill="var(--color-brand)"/>
            </svg>
          </div>
          <h2 class="form-header__title">Recuperar senha</h2>
          <p class="form-header__sub">
            Digite o e-mail da sua conta e enviaremos um link para você criar uma nova senha.
          </p>
        </header>

        <form class="form" @submit.prevent="handleSubmit" novalidate>

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
              />
            </div>
            <p v-if="emailError" class="field__message">{{ emailError }}</p>
          </div>

          <!-- Submit -->
          <button type="submit" class="btn-submit" :disabled="loading">
            <span v-if="!loading">Enviar instruções</span>
            <span v-else class="btn-submit__loading">
              <span class="spinner" />
              Enviando…
            </span>
          </button>

        </form>

        <div class="form-footer">
          <NuxtLink to="/auth/login" class="back-link">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M9 2L4 7l5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Voltar para o login
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- ── Success modal ───────────────────────────────────────── -->
    <Transition name="modal">
      <div v-if="showModal" class="modal-overlay" @click.self="onModalOk">
        <div class="modal">
          <div class="modal__icon">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <circle cx="16" cy="16" r="15" fill="rgba(0,106,255,.1)" stroke="var(--color-brand)" stroke-width="1.5"/>
              <path d="M10 16l4.5 4.5 7.5-9" stroke="var(--color-brand)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h3 class="modal__title">Verifique seu e-mail</h3>
          <p class="modal__body">
            Se <strong>{{ email }}</strong> estiver cadastrado, você receberá em instantes um link para redefinir sua senha.
          </p>
          <p class="modal__hint">Não recebeu? Verifique a pasta de spam.</p>
          <button class="modal__btn" @click="onModalOk">OK, entendi</button>
        </div>
      </div>
    </Transition>
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
    radial-gradient(ellipse 70% 60% at 20% 80%, #0a2a5c 0%, transparent 55%),
    radial-gradient(ellipse 55% 70% at 85% 15%, #153d8a 0%, transparent 50%),
    linear-gradient(155deg, #060f1e 0%, #0b1f42 45%, #071530 100%);
}

.hero__grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0,106,255,.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,106,255,.05) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(ellipse 100% 100% at 50% 50%, black 40%, transparent 100%);
}

.hero__content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  padding: 48px 56px;
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
  color: rgba(255,255,255,.45);
  margin-bottom: 16px;
}

.hero__headline {
  font-family: 'Fraunces', serif;
  font-size: clamp(34px, 3.8vw, 50px);
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

/* Lock card */
.lock-card {
  margin-top: 40px;
  background: rgba(255,255,255,.06);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255,255,255,.1);
  border-radius: 18px;
  padding: 28px 28px 24px;
  width: min(360px, 90%);
}

.lock-card__icon-wrap {
  position: relative;
  width: 60px;
  height: 60px;
  margin-bottom: 18px;
}

.lock-card__lock {
  position: relative;
  z-index: 1;
}

.lock-card__pulse {
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  background: rgba(0,106,255,.15);
  animation: pulse 2.4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: .6; }
  50% { transform: scale(1.25); opacity: 0; }
}

.lock-card__title {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 8px;
}

.lock-card__desc {
  font-size: 13px;
  color: rgba(255,255,255,.5);
  line-height: 1.6;
  margin-bottom: 22px;
}

.lock-card__steps {
  display: flex;
  align-items: center;
  gap: 0;
}

.lock-card__step {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  color: rgba(255,255,255,.45);
  white-space: nowrap;
}

.lock-card__step-num {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(0,106,255,.3);
  border: 1px solid rgba(96,165,250,.4);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 600;
  color: #93c5fd;
  flex-shrink: 0;
}

.lock-card__step-line {
  flex: 1;
  height: 1px;
  background: rgba(255,255,255,.1);
  margin: 0 8px;
}

.hero__footer {
  margin-top: auto;
  padding-top: 32px;
  font-size: 11px;
  color: rgba(255,255,255,.25);
  display: flex;
  align-items: center;
  gap: 6px;
}

.hero__footer::before {
  content: '';
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(96,165,250,.4);
  flex-shrink: 0;
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
  justify-content: center;
  margin-bottom: 40px;
}

/* Form header */
.form-header {
  margin-bottom: 36px;
}

.form-header__icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(0,106,255,.08);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
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
  line-height: 1.6;
}

/* Form */
.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Fields */
.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field__label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text);
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

.field__input::placeholder { color: #d1d5db; }

.field__input:focus {
  border-color: var(--color-brand);
  box-shadow: 0 0 0 3px rgba(0,106,255,.12);
}

.field__wrapper:focus-within .field__icon { color: var(--color-brand); }

.field--error .field__input { border-color: var(--color-error); }
.field--error .field__input:focus { box-shadow: 0 0 0 3px rgba(220,38,38,.1); }

.field__message {
  font-size: 12px;
  color: var(--color-error);
  padding-left: 2px;
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

.btn-submit:active:not(:disabled) { transform: translateY(0); }
.btn-submit:disabled { opacity: .7; cursor: not-allowed; }

.btn-submit__loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

/* Back link */
.form-footer {
  margin-top: 28px;
  display: flex;
  justify-content: center;
}

.back-link {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--color-text-muted);
  transition: color .2s;
  text-decoration: none;
}

.back-link:hover { color: var(--color-brand); }

/* Spinner */
.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,.35);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin .65s linear infinite;
  flex-shrink: 0;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ── Modal ───────────────────────────────────────────────────── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.45);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 500;
  padding: 24px;
}

.modal {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  box-shadow: 0 24px 60px rgba(0,0,0,.18);
  padding: 40px 36px 32px;
  max-width: 380px;
  width: 100%;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
}

.modal__icon {
  margin-bottom: 20px;
}

.modal__title {
  font-family: 'Fraunces', serif;
  font-size: 22px;
  font-weight: 600;
  font-style: italic;
  color: var(--color-text);
  letter-spacing: -.02em;
  margin-bottom: 12px;
}

.modal__body {
  font-size: 14px;
  color: var(--color-text-muted);
  line-height: 1.65;
  margin-bottom: 6px;
}

.modal__body strong {
  color: var(--color-text);
  font-weight: 500;
  word-break: break-all;
}

.modal__hint {
  font-size: 12px;
  color: var(--color-text-muted);
  opacity: .6;
  margin-bottom: 28px;
}

.modal__btn {
  width: 100%;
  height: 48px;
  background: var(--color-brand);
  color: #fff;
  border: none;
  border-radius: var(--radius-md);
  font-size: 15px;
  font-weight: 600;
  font-family: 'DM Sans', sans-serif;
  cursor: pointer;
  transition: background .2s, box-shadow .2s;
  box-shadow: 0 4px 14px rgba(0,106,255,.3);
}

.modal__btn:hover {
  background: var(--color-brand-dark);
  box-shadow: 0 6px 20px rgba(0,106,255,.4);
}

/* Modal transition */
.modal-enter-active, .modal-leave-active { transition: opacity .2s ease; }
.modal-enter-active .modal, .modal-leave-active .modal { transition: transform .2s ease, opacity .2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-from .modal { transform: scale(.95) translateY(8px); }
.modal-leave-to .modal { transform: scale(.95) translateY(8px); }

/* ── Responsive ──────────────────────────────────────────────── */
@media (max-width: 768px) {
  .hero { display: none; }
  .mobile-logo { display: flex; }
}
</style>
