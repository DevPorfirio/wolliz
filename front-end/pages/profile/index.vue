<script setup lang="ts">
import { useAuth } from '~/composables/useAuth'
import { useAuthStore } from '~/stores/auth'
import { isLocalPhoneValid, fullToLocal } from '~/composables/usePhoneInput'

definePageMeta({ middleware: 'auth' })
useHead({ title: 'Meu Perfil — Wolliz' })

const { user, logout } = useAuth()
const store = useAuthStore()

// ── Form ─────────────────────────────────────────────────────────
const name      = ref(user.value?.name  ?? '')
const phoneFull = ref(user.value?.phone ?? '')
// Telefone é opcional; só bloqueia se preenchido e inválido
const phoneValid = computed(() => {
  const local = fullToLocal(phoneFull.value)
  return !local || isLocalPhoneValid(local)
})
const saving   = ref(false)
const saveSuccess = ref(false)
const saveError   = ref('')

// ── Avatar ───────────────────────────────────────────────────────
const uploading     = ref(false)
const uploadError   = ref('')
const fileInput     = ref<HTMLInputElement | null>(null)
const avatarPreview = computed(() =>
  store.user?.avatar_url ?? null
)

function getInitials(n: string) {
  return n.split(' ').slice(0, 2).map(s => s[0]).join('').toUpperCase()
}

// ── Crop state ───────────────────────────────────────────────────
const showCrop    = ref(false)
const cropImgSrc  = ref('')
const cropImg     = ref<HTMLImageElement | null>(null)
const cropZoom    = ref(1)
const cropMinZoom = ref(1)   // atualizado quando a imagem carrega
const cropMaxZoom = ref(10)  // atualizado quando a imagem carrega
const cropX       = ref(0)   // offset em px no espaço da imagem
const cropY       = ref(0)
const dragging    = ref(false)
const dragLast    = ref({ x: 0, y: 0 })
const CROP_SIZE   = 280       // diâmetro do círculo de recorte

let rawFile: File | null = null

function openFileDialog() { fileInput.value?.click() }

function onFileChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  rawFile = file
  cropImgSrc.value = URL.createObjectURL(file)
  cropZoom.value = 1
  cropX.value = 0
  cropY.value = 0
  showCrop.value = true
  ;(e.target as HTMLInputElement).value = ''

  // Pré-carrega a imagem para saber as dimensões
  const img = new Image()
  img.onload = () => {
    cropImg.value = img
    // Zoom mínimo: imagem cobre exatamente o círculo de recorte
    const minZoom = Math.max(CROP_SIZE / img.naturalWidth, CROP_SIZE / img.naturalHeight)
    // Zoom máximo: resolução nativa (1px imagem = 1px tela)
    const maxZoom = Math.max(img.naturalWidth, img.naturalHeight) / CROP_SIZE
    cropMinZoom.value = minZoom
    cropMaxZoom.value = Math.max(maxZoom, minZoom + 0.01) // garante range válido
    cropZoom.value = minZoom
  }
  img.src = cropImgSrc.value
}

// ── Drag ─────────────────────────────────────────────────────────
function onPointerDown(e: PointerEvent) {
  dragging.value = true
  dragLast.value = { x: e.clientX, y: e.clientY }
  ;(e.currentTarget as HTMLElement).setPointerCapture(e.pointerId)
}
function onPointerMove(e: PointerEvent) {
  if (!dragging.value) return
  const dx = e.clientX - dragLast.value.x
  const dy = e.clientY - dragLast.value.y
  dragLast.value = { x: e.clientX, y: e.clientY }
  clampedMove(dx, dy)
}
function onPointerUp() { dragging.value = false }

function onWheel(e: WheelEvent) {
  e.preventDefault()
  const delta = e.deltaY > 0 ? -0.08 : 0.08
  cropZoom.value = clampZoom(cropZoom.value + delta)
  clampedMove(0, 0)
}

function clampZoom(z: number) {
  return Math.min(cropMaxZoom.value, Math.max(cropMinZoom.value, z))
}

function clampedMove(dx: number, dy: number) {
  if (!cropImg.value) return
  const scaledW = cropImg.value.naturalWidth  * cropZoom.value
  const scaledH = cropImg.value.naturalHeight * cropZoom.value
  const maxX = Math.max(0, (scaledW - CROP_SIZE) / 2)
  const maxY = Math.max(0, (scaledH - CROP_SIZE) / 2)
  cropX.value = Math.min(maxX, Math.max(-maxX, cropX.value + dx))
  cropY.value = Math.min(maxY, Math.max(-maxY, cropY.value + dy))
}

// ── Confirm crop: gera PNG via canvas e faz upload ───────────────
async function confirmCrop() {
  if (!cropImg.value || !rawFile) return
  uploading.value = true
  showCrop.value  = false
  uploadError.value = ''

  const OUTPUT = 400
  const canvas = document.createElement('canvas')
  canvas.width  = OUTPUT
  canvas.height = OUTPUT
  const ctx = canvas.getContext('2d')!

  ctx.beginPath()
  ctx.arc(OUTPUT / 2, OUTPUT / 2, OUTPUT / 2, 0, Math.PI * 2)
  ctx.clip()

  // Calcula qual região da imagem original está visível dentro do círculo.
  // srcSize: quantos pixels naturais cabem no diâmetro do círculo de recorte.
  // cropX/cropY estão em CSS px (deslocamento da imagem no stage).
  const srcSize = CROP_SIZE / cropZoom.value
  const srcX    = cropImg.value.naturalWidth  / 2 - srcSize / 2 - cropX.value / cropZoom.value
  const srcY    = cropImg.value.naturalHeight / 2 - srcSize / 2 - cropY.value / cropZoom.value

  ctx.drawImage(cropImg.value, srcX, srcY, srcSize, srcSize, 0, 0, OUTPUT, OUTPUT)

  canvas.toBlob(async (blob) => {
    if (!blob) { uploading.value = false; return }
    const form = new FormData()
    form.append('avatar', blob, 'avatar.jpg')
    try {
      const data = await $fetch<any>('/api/auth/avatar', {
        method: 'POST',
        headers: { Authorization: `Bearer ${store.accessToken}` },
        body: form,
      })
      store.user = data
    } catch (e: any) {
      uploadError.value = e?.data?.message ?? 'Erro ao fazer upload.'
    } finally {
      uploading.value = false
    }
  }, 'image/jpeg', 0.92)
}

function cancelCrop() {
  showCrop.value = false
  rawFile = null
  cropImgSrc.value = ''
  cropMinZoom.value = 1
  cropMaxZoom.value = 10
}

// ── Save profile ─────────────────────────────────────────────────
async function saveProfile() {
  saving.value = true
  saveError.value = ''
  saveSuccess.value = false
  try {
    const data = await $fetch<any>('/api/auth/profile', {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${store.accessToken}` },
      body: { name: name.value, phone: phoneFull.value },
    })
    store.user = data
    saveSuccess.value = true
    setTimeout(() => saveSuccess.value = false, 3000)
  } catch (e: any) {
    saveError.value = e?.data?.message ?? 'Erro ao salvar.'
  } finally {
    saving.value = false
  }
}

// Sync form quando store atualiza
watch(() => store.user, (u) => {
  if (u) { name.value = u.name; phoneFull.value = u.phone ?? '' }
})
</script>

<template>
  <div class="page">
    <header class="topbar">
      <NuxtLink to="/" class="logo-link"><AppLogo size="sm" /></NuxtLink>
      <button class="topbar__logout" @click="logout">Sair</button>
    </header>

    <main class="content">
      <div class="card">
        <NuxtLink to="/" class="card__close" aria-label="Voltar para o início">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M1 1l12 12M13 1L1 13" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>
          </svg>
        </NuxtLink>

        <!-- Avatar -->
        <div class="avatar-section">
          <div class="avatar-wrap" @click="openFileDialog">
            <img v-if="avatarPreview" :src="avatarPreview" class="avatar-img" alt="Foto de perfil" />
            <div v-else class="avatar-initials">{{ getInitials(user?.name ?? '') }}</div>
            <div v-if="uploading" class="avatar-overlay"><span class="spinner" /></div>
            <div class="avatar-edit" aria-hidden="true">
              <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                <path d="M8.5 2l2.5 2.5L3.5 12H1v-2.5L8.5 2z" stroke="white" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
          <input ref="fileInput" type="file" accept="image/jpeg,image/png,image/webp" class="file-input" @change="onFileChange" />
          <div class="avatar-info">
            <p class="avatar-name">{{ user?.name }}</p>
            <p class="avatar-email">{{ user?.email }}</p>
          </div>
          <p v-if="uploadError" class="upload-error">{{ uploadError }}</p>
          <p class="avatar-hint">Clique para trocar · JPG, PNG ou WebP · máx. 5 MB</p>
        </div>

        <div class="divider" />

        <!-- Form -->
        <form class="form" @submit.prevent="saveProfile" novalidate>
          <h2 class="form__title">Informações pessoais</h2>

          <div class="field">
            <label class="field__label" for="pf-name">Nome completo</label>
            <input id="pf-name" v-model="name" type="text" class="field__input" placeholder="Seu nome" autocomplete="name" />
          </div>

          <div class="field">
            <label class="field__label" for="pf-email">E-mail</label>
            <input id="pf-email" :value="user?.email" type="email" class="field__input field__input--disabled" disabled />
            <p class="field__hint">O e-mail não pode ser alterado.</p>
          </div>

          <div class="field">
            <label class="field__label">
              Telefone <span class="field__optional">(opcional)</span>
            </label>
            <AppPhoneInput v-model="phoneFull" />
          </div>

          <p v-if="saveError" class="form__error">{{ saveError }}</p>

          <button type="submit" class="btn-save" :disabled="saving || !phoneValid">
            <template v-if="saving"><span class="spinner spinner--white" /> Salvando…</template>
            <template v-else-if="saveSuccess">
              <svg width="15" height="15" viewBox="0 0 15 15" fill="none">
                <path d="M3 8l3.5 3.5 5.5-7" stroke="white" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Salvo!
            </template>
            <template v-else>Salvar alterações</template>
          </button>
        </form>

        <div class="divider" />

        <!-- Segurança -->
        <div class="security-section">
          <h3 class="security-section__title">Segurança</h3>
          <NuxtLink to="/profile/change-password" class="security-item">
            <div class="security-item__icon">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <rect x="2.5" y="7" width="11" height="8" rx="1.5" stroke="currentColor" stroke-width="1.3"/>
                <path d="M5 7V5a3 3 0 0 1 6 0v2" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
                <circle cx="8" cy="11" r="1.2" fill="currentColor"/>
              </svg>
            </div>
            <div class="security-item__body">
              <p class="security-item__label">Alterar senha</p>
              <p class="security-item__sub">Atualize sua senha de acesso</p>
            </div>
            <svg class="security-item__chevron" width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M5 3l4 4-4 4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </NuxtLink>
        </div>
      </div>
    </main>

    <!-- ── Crop modal ────────────────────────────────────────────── -->
    <Teleport to="body">
      <div v-if="showCrop" class="crop-backdrop" @click.self="cancelCrop">
        <div class="crop-modal">
          <div class="crop-modal__header">
            <h3 class="crop-modal__title">Ajustar foto de perfil</h3>
            <p class="crop-modal__sub">Arraste para reposicionar · scroll para zoom</p>
          </div>

          <div
            class="crop-stage"
            @pointerdown="onPointerDown"
            @pointermove="onPointerMove"
            @pointerup="onPointerUp"
            @pointercancel="onPointerUp"
            @wheel.prevent="onWheel"
          >
            <!-- Imagem posicionada -->
            <img
              v-if="cropImgSrc"
              :src="cropImgSrc"
              class="crop-image"
              :style="{
                transform: `translate(calc(-50% + ${cropX}px), calc(-50% + ${cropY}px)) scale(${cropZoom})`,
                transformOrigin: 'center center',
              }"
              draggable="false"
            />
            <!-- Overlay escuro com buraco circular -->
            <div class="crop-overlay" />
            <!-- Aro branco do círculo -->
            <div class="crop-ring" />
          </div>

          <!-- Slider de zoom -->
          <div class="crop-zoom">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <circle cx="6" cy="6" r="4.5" stroke="currentColor" stroke-width="1.3"/>
              <path d="M10 10l2.5 2.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
              <path d="M4 6h4M6 4v4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
            </svg>
            <input
              type="range" :min="cropMinZoom" :max="cropMaxZoom" step="0.02"
              :value="cropZoom"
              class="crop-zoom__slider"
              @input="(e) => { cropZoom = clampZoom(parseFloat((e.target as HTMLInputElement).value)); clampedMove(0,0) }"
            />
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <circle cx="6" cy="6" r="4.5" stroke="currentColor" stroke-width="1.3"/>
              <path d="M10 10l2.5 2.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
              <path d="M4 6h4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
            </svg>
          </div>

          <div class="crop-actions">
            <button class="crop-btn crop-btn--cancel" @click="cancelCrop">Cancelar</button>
            <button class="crop-btn crop-btn--confirm" @click="confirmCrop">Usar esta foto</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.page {
  min-height: 100dvh;
  background: var(--color-bg);
  font-family: 'DM Sans', var(--font-sans);
}

/* Topbar */
.topbar {
  height: 60px;
  padding: 0 24px;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.logo-link { text-decoration: none; display: flex; align-items: center; }
.topbar__logout {
  font-size: 13px; font-weight: 500; color: var(--color-text-muted);
  background: none; border: none; cursor: pointer;
  padding: 6px 10px; border-radius: var(--radius-sm);
  transition: background .2s, color .2s;
}
.topbar__logout:hover { background: var(--color-bg); color: var(--color-text); }

/* Content */
.content { max-width: 520px; margin: 0 auto; padding: 40px 24px 80px; }

.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  position: relative;
}

.card__close {
  position: absolute;
  top: 14px;
  right: 14px;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
  text-decoration: none;
  transition: background .15s, color .15s, border-color .15s;
  z-index: 10;
}
.card__close:hover {
  background: var(--color-border);
  color: var(--color-text);
  border-color: transparent;
}

/* Avatar */
.avatar-section {
  display: flex; flex-direction: column; align-items: center;
  padding: 36px 24px 28px; gap: 8px;
}
.avatar-wrap {
  position: relative; width: 88px; height: 88px;
  cursor: pointer;
}
.avatar-wrap:hover .avatar-edit { opacity: 1; }
.avatar-img {
  width: 88px; height: 88px; border-radius: 50%;
  object-fit: cover; display: block;
}
.avatar-initials {
  width: 88px; height: 88px; border-radius: 50%;
  background: var(--color-brand); color: #fff;
  font-size: 28px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.avatar-overlay {
  position: absolute; inset: 0; border-radius: 50%;
  background: rgba(0,0,0,.45);
  display: flex; align-items: center; justify-content: center;
}
.avatar-edit {
  position: absolute; bottom: 2px; right: 2px;
  width: 26px; height: 26px; border-radius: 50%;
  background: var(--color-brand); border: 2px solid #fff;
  display: flex; align-items: center; justify-content: center;
  opacity: 0; transition: opacity .2s;
  pointer-events: none;
}
.file-input { display: none; }
.avatar-info { text-align: center; }
.avatar-name { font-size: 17px; font-weight: 600; color: var(--color-text); }
.avatar-email { font-size: 13px; color: var(--color-text-muted); margin-top: 2px; }
.avatar-hint { font-size: 12px; color: var(--color-text-muted); }
.upload-error { font-size: 13px; color: var(--color-error); }

.divider { height: 1px; background: var(--color-border); }

/* Form */
.form { padding: 28px 28px 32px; display: flex; flex-direction: column; gap: 20px; }
.form__title { font-size: 15px; font-weight: 600; color: var(--color-text); letter-spacing: -.01em; }
.form__error {
  font-size: 13px; color: var(--color-error);
  background: #fef2f2; border: 1px solid #fecaca;
  border-radius: var(--radius-sm); padding: 10px 14px;
}
.field { display: flex; flex-direction: column; gap: 6px; }
.field__label { font-size: 13px; font-weight: 500; color: var(--color-text); }
.field__optional { font-weight: 400; color: var(--color-text-muted); }
.field__input {
  height: 42px; border: 1px solid var(--color-border);
  border-radius: var(--radius-md); padding: 0 14px;
  font-size: 14px; color: var(--color-text);
  background: var(--color-surface); outline: none;
  transition: border-color .2s, box-shadow .2s;
}
.field__input:focus { border-color: var(--color-brand); box-shadow: 0 0 0 3px rgba(0,106,255,.12); }
.field__input--disabled { background: var(--color-bg); color: var(--color-text-muted); cursor: not-allowed; }
.field__hint { font-size: 12px; color: var(--color-text-muted); }
.btn-save {
  height: 44px; background: var(--color-brand); color: #fff;
  border: none; border-radius: var(--radius-md);
  font-size: 14px; font-weight: 600; cursor: pointer;
  display: flex; align-items: center; justify-content: center; gap: 7px;
  transition: background .2s; margin-top: 4px;
}
.btn-save:hover:not(:disabled) { background: var(--color-brand-dark); }
.btn-save:disabled { opacity: .7; cursor: not-allowed; }

/* Security section */
.security-section {
  padding: 24px 28px 8px;
}
.security-section__title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 12px;
}
.security-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  text-decoration: none;
  color: var(--color-text);
  transition: background .15s, border-color .15s;
  margin-bottom: 16px;
}
.security-item:hover {
  background: var(--color-bg);
  border-color: #c0c9d6;
}
.security-item__icon {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: rgba(0,106,255,.08);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-brand);
  flex-shrink: 0;
}
.security-item__body { flex: 1; }
.security-item__label { font-size: 14px; font-weight: 500; line-height: 1.3; }
.security-item__sub { font-size: 12px; color: var(--color-text-muted); margin-top: 2px; }
.security-item__chevron { color: var(--color-text-muted); flex-shrink: 0; }

/* Spinner */
.spinner {
  width: 16px; height: 16px;
  border: 2px solid rgba(0,106,255,.2); border-top-color: var(--color-brand);
  border-radius: 50%; animation: spin .7s linear infinite; display: inline-block;
}
.spinner--white { border-color: rgba(255,255,255,.3); border-top-color: #fff; }
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Crop modal ──────────────────────────────────────────────────── */
.crop-backdrop {
  position: fixed; inset: 0; z-index: 1000;
  background: rgba(0,0,0,.7);
  display: flex; align-items: center; justify-content: center;
  padding: 24px;
  animation: fade-in .15s ease;
}
@keyframes fade-in { from { opacity: 0 } to { opacity: 1 } }

.crop-modal {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  width: 100%; max-width: 360px;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  animation: slide-up .2s ease;
}
@keyframes slide-up { from { transform: translateY(12px); opacity: 0 } to { transform: translateY(0); opacity: 1 } }

.crop-modal__header { padding: 20px 20px 16px; text-align: center; }
.crop-modal__title { font-size: 15px; font-weight: 600; color: var(--color-text); }
.crop-modal__sub { font-size: 12px; color: var(--color-text-muted); margin-top: 4px; }

.crop-stage {
  position: relative;
  width: 100%;
  height: 280px;
  background: #111;
  overflow: hidden;
  cursor: grab;
  touch-action: none;
}
.crop-stage:active { cursor: grabbing; }

.crop-image {
  position: absolute;
  top: 50%; left: 50%;
  max-width: none;
  user-select: none;
  pointer-events: none;
}

/* Overlay escuro com buraco circular */
.crop-overlay {
  position: absolute; inset: 0;
  background: rgba(0,0,0,.55);
  border-radius: 0;
  /* Buraco circular no centro usando mask */
  mask-image: radial-gradient(circle 140px at center, transparent 100%, black 100%);
  -webkit-mask-image: radial-gradient(circle 140px at center, transparent 100%, black 100%);
  pointer-events: none;
}

/* Aro branco */
.crop-ring {
  position: absolute;
  top: 50%; left: 50%;
  width: 280px; height: 280px;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  border: 2px solid rgba(255,255,255,.8);
  pointer-events: none;
}

/* Zoom slider */
.crop-zoom {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 20px;
  color: var(--color-text-muted);
  border-top: 1px solid var(--color-border);
}
.crop-zoom__slider {
  flex: 1; height: 3px; cursor: pointer;
  accent-color: var(--color-brand);
}

.crop-actions {
  display: grid; grid-template-columns: 1fr 1fr; gap: 10px;
  padding: 14px 20px 20px;
}
.crop-btn {
  height: 40px; border-radius: var(--radius-md);
  font-size: 14px; font-weight: 600; cursor: pointer;
  transition: background .15s;
  border: none;
}
.crop-btn--cancel {
  background: var(--color-bg); color: var(--color-text);
  border: 1px solid var(--color-border);
}
.crop-btn--cancel:hover { background: var(--color-border); }
.crop-btn--confirm { background: var(--color-brand); color: #fff; }
.crop-btn--confirm:hover { background: var(--color-brand-dark); }
</style>
