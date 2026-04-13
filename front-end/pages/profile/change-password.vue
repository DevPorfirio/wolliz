<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

definePageMeta({ middleware: 'auth', layout: false })
useHead({ title: 'Alterar senha — Wolliz' })

const router = useRouter()
const store  = useAuthStore()

const currentPassword  = ref('')
const newPassword      = ref('')
const confirmPassword  = ref('')

const showCurrent = ref(false)
const showNew     = ref(false)
const showConfirm = ref(false)

const loading = ref(false)
const error   = ref('')
const success  = ref(false)

// ── Validação inline ──────────────────────────────────────────
const currentError  = ref('')
const newError      = ref('')
const confirmError  = ref('')

// Força da nova senha
const strength = computed(() => {
  const p = newPassword.value
  if (!p) return 0
  let score = 0
  if (p.length >= 8)  score++
  if (p.length >= 12) score++
  if (/[A-Z]/.test(p)) score++
  if (/[0-9]/.test(p)) score++
  if (/[^A-Za-z0-9]/.test(p)) score++
  return score
})

const strengthLabel = computed(() => {
  if (!newPassword.value) return ''
  if (strength.value <= 1) return 'Fraca'
  if (strength.value <= 3) return 'Média'
  return 'Forte'
})

const strengthClass = computed(() => {
  if (!newPassword.value) return ''
  if (strength.value <= 1) return 'weak'
  if (strength.value <= 3) return 'medium'
  return 'strong'
})

function validate(): boolean {
  currentError.value  = ''
  newError.value      = ''
  confirmError.value  = ''
  let ok = true

  if (!currentPassword.value) {
    currentError.value = 'Informe a senha atual'
    ok = false
  }
  if (!newPassword.value || newPassword.value.length < 8) {
    newError.value = 'A nova senha deve ter pelo menos 8 caracteres'
    ok = false
  }
  if (newPassword.value && newPassword.value === currentPassword.value) {
    newError.value = 'A nova senha deve ser diferente da atual'
    ok = false
  }
  if (!confirmPassword.value) {
    confirmError.value = 'Confirme a nova senha'
    ok = false
  } else if (confirmPassword.value !== newPassword.value) {
    confirmError.value = 'As senhas não coincidem'
    ok = false
  }
  return ok
}

async function handleSubmit() {
  if (!validate()) return
  loading.value = true
  error.value   = ''
  try {
    await $fetch('/api/auth/change-password', {
      method: 'POST',
      headers: { Authorization: `Bearer ${store.accessToken}` },
      body: {
        current_password: currentPassword.value,
        new_password:     newPassword.value,
      },
    })
    success.value = true
    setTimeout(() => router.push('/profile'), 2200)
  } catch (e: any) {
    error.value = e?.data?.message ?? 'Erro ao alterar senha. Tente novamente.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page">
    <header class="topbar">
      <NuxtLink to="/profile" class="back-btn" aria-label="Voltar ao perfil">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M10 3L5 8l5 5" stroke="currentColor" stroke-width="1.6"
                stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Voltar
      </NuxtLink>
      <AppLogo size="sm" />
      <div style="width: 72px" />
    </header>

    <main class="content">
      <div class="card">

        <!-- Cabeçalho do card -->
        <div class="card__head">
          <div class="card__head-icon">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <rect x="3" y="9" width="14" height="10" rx="2" stroke="var(--color-brand)" stroke-width="1.4"/>
              <path d="M6.5 9V6.5a3.5 3.5 0 0 1 7 0V9" stroke="var(--color-brand)" stroke-width="1.4" stroke-linecap="round"/>
              <circle cx="10" cy="14" r="1.5" fill="var(--color-brand)"/>
            </svg>
          </div>
          <div>
            <h2 class="card__title">Alterar senha</h2>
            <p class="card__sub">Escolha uma senha forte e única.</p>
          </div>
        </div>

        <div class="divider" />

        <!-- Formulário -->
        <form class="form" @submit.prevent="handleSubmit" novalidate>

          <!-- Erro geral -->
          <Transition name="fade">
            <div v-if="error" class="form__error-banner" role="alert">
              <svg width="15" height="15" viewBox="0 0 15 15" fill="none">
                <circle cx="7.5" cy="7.5" r="7" stroke="currentColor"/>
                <path d="M7.5 4v4M7.5 10v1" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
              </svg>
              {{ error }}
            </div>
          </Transition>

          <!-- Sucesso -->
          <Transition name="fade">
            <div v-if="success" class="form__success-banner" role="status">
              <svg width="15" height="15" viewBox="0 0 15 15" fill="none">
                <circle cx="7.5" cy="7.5" r="7" stroke="currentColor"/>
                <path d="M4.5 8l2.5 2.5 4-5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Senha alterada! Redirecionando…
            </div>
          </Transition>

          <!-- Senha atual -->
          <div class="field" :class="{ 'field--error': currentError }">
            <label class="field__label" for="cp-current">Senha atual</label>
            <div class="field__wrapper">
              <svg class="field__icon" width="17" height="17" viewBox="0 0 17 17" fill="none">
                <rect x="3" y="7" width="11" height="8" rx="1.5" stroke="currentColor" stroke-width="1.2"/>
                <path d="M5.5 7V5.5a3 3 0 1 1 6 0V7" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
              </svg>
              <input
                id="cp-current"
                v-model="currentPassword"
                :type="showCurrent ? 'text' : 'password'"
                class="field__input"
                placeholder="••••••••"
                autocomplete="current-password"
              />
              <button type="button" class="field__toggle" tabindex="-1"
                      @click="showCurrent = !showCurrent">
                <svg v-if="!showCurrent" width="17" height="17" viewBox="0 0 17 17" fill="none">
                  <path d="M1 8.5s3-5.5 7.5-5.5S16 8.5 16 8.5s-3 5.5-7.5 5.5S1 8.5 1 8.5z" stroke="currentColor" stroke-width="1.2"/>
                  <circle cx="8.5" cy="8.5" r="2.2" stroke="currentColor" stroke-width="1.2"/>
                </svg>
                <svg v-else width="17" height="17" viewBox="0 0 17 17" fill="none">
                  <path d="M2 2l13 13M7 7.2A2.2 2.2 0 0 0 10.8 11M4.8 4.9C3.2 6 2 7.7 2 8.5s3 5.5 6.5 5.5c1.4 0 2.7-.5 3.7-1.3M8.5 3c3.5 0 6.5 2.7 6.5 5.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
            <p v-if="currentError" class="field__message">{{ currentError }}</p>
          </div>

          <!-- Nova senha -->
          <div class="field" :class="{ 'field--error': newError }">
            <label class="field__label" for="cp-new">Nova senha</label>
            <div class="field__wrapper">
              <svg class="field__icon" width="17" height="17" viewBox="0 0 17 17" fill="none">
                <rect x="3" y="7" width="11" height="8" rx="1.5" stroke="currentColor" stroke-width="1.2"/>
                <path d="M5.5 7V5.5a3 3 0 1 1 6 0V7" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
              </svg>
              <input
                id="cp-new"
                v-model="newPassword"
                :type="showNew ? 'text' : 'password'"
                class="field__input"
                placeholder="••••••••"
                autocomplete="new-password"
              />
              <button type="button" class="field__toggle" tabindex="-1"
                      @click="showNew = !showNew">
                <svg v-if="!showNew" width="17" height="17" viewBox="0 0 17 17" fill="none">
                  <path d="M1 8.5s3-5.5 7.5-5.5S16 8.5 16 8.5s-3 5.5-7.5 5.5S1 8.5 1 8.5z" stroke="currentColor" stroke-width="1.2"/>
                  <circle cx="8.5" cy="8.5" r="2.2" stroke="currentColor" stroke-width="1.2"/>
                </svg>
                <svg v-else width="17" height="17" viewBox="0 0 17 17" fill="none">
                  <path d="M2 2l13 13M7 7.2A2.2 2.2 0 0 0 10.8 11M4.8 4.9C3.2 6 2 7.7 2 8.5s3 5.5 6.5 5.5c1.4 0 2.7-.5 3.7-1.3M8.5 3c3.5 0 6.5 2.7 6.5 5.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                </svg>
              </button>
            </div>

            <!-- Barra de força -->
            <div v-if="newPassword" class="strength-bar">
              <div class="strength-bar__track">
                <div
                  class="strength-bar__fill"
                  :class="strengthClass"
                  :style="{ width: `${Math.min(strength / 5 * 100, 100)}%` }"
                />
              </div>
              <span class="strength-bar__label" :class="strengthClass">{{ strengthLabel }}</span>
            </div>

            <p v-if="newError" class="field__message">{{ newError }}</p>
          </div>

          <!-- Confirmar nova senha -->
          <div class="field" :class="{ 'field--error': confirmError }">
            <label class="field__label" for="cp-confirm">Confirmar nova senha</label>
            <div class="field__wrapper">
              <svg class="field__icon" width="17" height="17" viewBox="0 0 17 17" fill="none">
                <rect x="3" y="7" width="11" height="8" rx="1.5" stroke="currentColor" stroke-width="1.2"/>
                <path d="M5.5 7V5.5a3 3 0 1 1 6 0V7" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
              </svg>
              <input
                id="cp-confirm"
                v-model="confirmPassword"
                :type="showConfirm ? 'text' : 'password'"
                class="field__input"
                placeholder="••••••••"
                autocomplete="new-password"
              />
              <button type="button" class="field__toggle" tabindex="-1"
                      @click="showConfirm = !showConfirm">
                <svg v-if="!showConfirm" width="17" height="17" viewBox="0 0 17 17" fill="none">
                  <path d="M1 8.5s3-5.5 7.5-5.5S16 8.5 16 8.5s-3 5.5-7.5 5.5S1 8.5 1 8.5z" stroke="currentColor" stroke-width="1.2"/>
                  <circle cx="8.5" cy="8.5" r="2.2" stroke="currentColor" stroke-width="1.2"/>
                </svg>
                <svg v-else width="17" height="17" viewBox="0 0 17 17" fill="none">
                  <path d="M2 2l13 13M7 7.2A2.2 2.2 0 0 0 10.8 11M4.8 4.9C3.2 6 2 7.7 2 8.5s3 5.5 6.5 5.5c1.4 0 2.7-.5 3.7-1.3M8.5 3c3.5 0 6.5 2.7 6.5 5.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
            <p v-if="confirmError" class="field__message">{{ confirmError }}</p>
          </div>

          <button type="submit" class="btn-submit" :disabled="loading || success">
            <template v-if="loading">
              <span class="spinner" /> Salvando…
            </template>
            <template v-else>Alterar senha</template>
          </button>

        </form>
      </div>
    </main>
  </div>
</template>

<style scoped>
* { box-sizing: border-box; }

.page {
  min-height: 100dvh;
  background: var(--color-bg);
  font-family: 'DM Sans', var(--font-sans);
  display: flex;
  flex-direction: column;
}

/* Topbar */
.topbar {
  height: 60px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-muted);
  text-decoration: none;
  transition: color .15s;
  width: 72px;
}
.back-btn:hover { color: var(--color-brand); }

/* Content */
.content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 24px 60px;
}

/* Card */
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  width: 100%;
  max-width: 440px;
  overflow: hidden;
}

.card__head {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 28px 28px 24px;
}

.card__head-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(0,106,255,.08);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card__title {
  font-family: 'Fraunces', serif;
  font-size: 20px;
  font-weight: 600;
  font-style: italic;
  color: var(--color-text);
  letter-spacing: -.02em;
  line-height: 1.2;
}

.card__sub {
  font-size: 13px;
  color: var(--color-text-muted);
  margin-top: 3px;
}

.divider { height: 1px; background: var(--color-border); }

/* Form */
.form {
  padding: 28px;
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

.form__success-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: var(--radius-md);
  color: #16a34a;
  font-size: 13px;
  padding: 12px 14px;
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
  left: 13px;
  color: #9ca3af;
  pointer-events: none;
  transition: color .2s;
}

.field__input {
  width: 100%;
  height: 46px;
  padding: 0 42px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 14px;
  color: var(--color-text);
  background: var(--color-surface);
  outline: none;
  transition: border-color .2s, box-shadow .2s;
}

.field__input::placeholder { color: #d1d5db; }

.field__input:focus {
  border-color: var(--color-brand);
  box-shadow: 0 0 0 3px rgba(0,106,255,.12);
}

.field__wrapper:focus-within .field__icon { color: var(--color-brand); }
.field--error .field__input { border-color: var(--color-error); }
.field--error .field__input:focus { box-shadow: 0 0 0 3px rgba(220,38,38,.1); }

.field__toggle {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  padding: 4px;
  color: #9ca3af;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: color .15s;
  border-radius: 4px;
}
.field__toggle:hover { color: var(--color-text); }

.field__message {
  font-size: 12px;
  color: var(--color-error);
  padding-left: 2px;
}

/* Strength bar */
.strength-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 2px;
}

.strength-bar__track {
  flex: 1;
  height: 4px;
  background: var(--color-border);
  border-radius: 99px;
  overflow: hidden;
}

.strength-bar__fill {
  height: 100%;
  border-radius: 99px;
  transition: width .3s ease, background-color .3s ease;
}

.strength-bar__fill.weak   { background: var(--color-error); }
.strength-bar__fill.medium { background: #f59e0b; }
.strength-bar__fill.strong { background: #16a34a; }

.strength-bar__label {
  font-size: 11px;
  font-weight: 500;
  white-space: nowrap;
}
.strength-bar__label.weak   { color: var(--color-error); }
.strength-bar__label.medium { color: #d97706; }
.strength-bar__label.strong { color: #16a34a; }

/* Submit */
.btn-submit {
  height: 46px;
  background: var(--color-brand);
  color: #fff;
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 600;
  font-family: 'DM Sans', sans-serif;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: background .2s, box-shadow .2s, transform .1s;
  box-shadow: 0 4px 14px rgba(0,106,255,.3);
  margin-top: 4px;
}
.btn-submit:hover:not(:disabled) {
  background: var(--color-brand-dark);
  box-shadow: 0 6px 20px rgba(0,106,255,.4);
  transform: translateY(-1px);
}
.btn-submit:active:not(:disabled) { transform: translateY(0); }
.btn-submit:disabled { opacity: .7; cursor: not-allowed; }

/* Spinner */
.spinner {
  width: 15px; height: 15px;
  border: 2px solid rgba(255,255,255,.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin .65s linear infinite;
  flex-shrink: 0;
  display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Fade transition */
.fade-enter-active, .fade-leave-active { transition: opacity .2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
