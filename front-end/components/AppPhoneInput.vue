<script setup lang="ts">
import { formatLocalPhone, fullToLocal, usePhoneInput } from '~/composables/usePhoneInput'

const props = defineProps<{
  modelValue?: string   // valor completo: "+55 48 98416-1284"
}>()
const emit = defineEmits<{
  'update:modelValue': [value: string]
  'error': [msg: string]
}>()

// Países disponíveis (expansível)
const countries = [
  { code: 'BR', flag: '🇧🇷', dial: '+55', name: 'Brasil' },
]
const selectedCountry = ref(countries[0])
const showDropdown    = ref(false)

const { localPhone, onPhoneInput, phoneError, phoneValid, phoneFull } = usePhoneInput(props.modelValue ?? '')

// Sincroniza quando prop muda externamente
watch(() => props.modelValue, (val) => {
  if (val && val !== phoneFull.value) {
    localPhone.value = formatLocalPhone(fullToLocal(val))
  }
})

// Emite valor completo para o pai
watch(phoneFull, (val) => emit('update:modelValue', val))
watch(phoneError, (msg) => emit('error', msg))

function selectCountry(c: typeof countries[0]) {
  selectedCountry.value = c
  showDropdown.value = false
}

function onClickOutside(e: MouseEvent) {
  const el = (e.target as HTMLElement).closest('.phone-country')
  if (!el) showDropdown.value = false
}
onMounted(() => document.addEventListener('click', onClickOutside))
onUnmounted(() => document.removeEventListener('click', onClickOutside))
</script>

<template>
  <div class="phone-wrap" :class="{ 'phone-wrap--error': phoneError }">
    <!-- Seletor de país -->
    <div class="phone-country">
      <button
        type="button"
        class="phone-country__btn"
        @click.stop="showDropdown = !showDropdown"
        :aria-expanded="showDropdown"
        aria-label="Selecionar país"
      >
        <span class="phone-country__flag">{{ selectedCountry.flag }}</span>
        <span class="phone-country__dial">{{ selectedCountry.dial }}</span>
        <svg class="phone-country__chevron" :class="{ open: showDropdown }"
             width="11" height="11" viewBox="0 0 11 11" fill="none">
          <path d="M2 4l3.5 3.5L9 4" stroke="currentColor" stroke-width="1.4"
                stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>

      <div v-if="showDropdown" class="phone-country__dropdown">
        <button
          v-for="c in countries"
          :key="c.code"
          type="button"
          class="phone-country__option"
          :class="{ 'phone-country__option--active': c.code === selectedCountry.code }"
          @click="selectCountry(c)"
        >
          <span>{{ c.flag }}</span>
          <span class="phone-country__option-name">{{ c.name }}</span>
          <span class="phone-country__option-dial">{{ c.dial }}</span>
        </button>
      </div>
    </div>

    <div class="phone-divider" />

    <!-- Input numérico -->
    <input
      :value="localPhone"
      type="tel"
      class="phone-input"
      :placeholder="selectedCountry.code === 'BR' ? '48 98416-1284' : 'número'"
      autocomplete="tel-national"
      @input="onPhoneInput"
    />
  </div>
  <p v-if="phoneError" class="phone-error">{{ phoneError }}</p>
</template>

<style scoped>
.phone-wrap {
  display: flex;
  align-items: center;
  height: 46px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  transition: border-color .2s, box-shadow .2s;
  overflow: visible;
}
.phone-wrap:focus-within {
  border-color: var(--color-brand);
  box-shadow: 0 0 0 3px rgba(0,106,255,.12);
}
.phone-wrap--error {
  border-color: var(--color-error);
}
.phone-wrap--error:focus-within {
  box-shadow: 0 0 0 3px rgba(220,38,38,.1);
}

/* Country selector */
.phone-country {
  position: relative;
  flex-shrink: 0;
}
.phone-country__btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 0 10px 0 12px;
  height: 44px;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-text);
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
}
.phone-country__flag { font-size: 16px; line-height: 1; }
.phone-country__dial { font-size: 13px; color: var(--color-text-muted); }
.phone-country__chevron {
  color: var(--color-text-muted);
  transition: transform .2s;
}
.phone-country__chevron.open { transform: rotate(180deg); }

.phone-country__dropdown {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  min-width: 200px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  z-index: 200;
  overflow: hidden;
  animation: drop-in .12s ease;
}
@keyframes drop-in {
  from { opacity: 0; transform: translateY(-4px); }
  to   { opacity: 1; transform: translateY(0); }
}
.phone-country__option {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 9px 14px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 13px;
  color: var(--color-text);
  transition: background .15s;
  text-align: left;
}
.phone-country__option:hover { background: var(--color-bg); }
.phone-country__option--active { background: var(--color-brand-light); }
.phone-country__option-name { flex: 1; }
.phone-country__option-dial { color: var(--color-text-muted); font-size: 12px; }

/* Divider */
.phone-divider {
  width: 1px;
  height: 22px;
  background: var(--color-border);
  flex-shrink: 0;
}

/* Input */
.phone-input {
  flex: 1;
  height: 100%;
  padding: 0 14px;
  border: none;
  outline: none;
  font-size: 14px;
  color: var(--color-text);
  background: transparent;
  min-width: 0;
}
.phone-input::placeholder { color: var(--color-text-muted); }

/* Error */
.phone-error {
  font-size: 12px;
  color: var(--color-error);
  margin-top: 5px;
}
</style>
