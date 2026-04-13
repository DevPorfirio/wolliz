/**
 * Formata telefone brasileiro sem o DDI no input.
 * Exibe: 48 98416-1284
 * Armazena completo: +55 48 98416-1284
 */

export function formatLocalPhone(raw: string): string {
  // Aceita só dígitos (espaços e hífens são tratados como separadores e ignorados na extração)
  const digits = raw.replace(/\D/g, '').slice(0, 11)
  if (!digits) return ''

  const ddd  = digits.slice(0, 2)
  const rest = digits.slice(2)

  if (!rest) return ddd

  // Celular começa com 9 → formato XXXXX-XXXX
  // Fixo → formato XXXX-XXXX
  const isMobile = rest[0] === '9'

  if (isMobile) {
    if (rest.length <= 5) return `${ddd} ${rest}`
    return `${ddd} ${rest.slice(0, 5)}-${rest.slice(5, 9)}`
  } else {
    if (rest.length <= 4) return `${ddd} ${rest}`
    return `${ddd} ${rest.slice(0, 4)}-${rest.slice(4, 8)}`
  }
}

export function localToFull(local: string, dialCode = '+55'): string {
  return local ? `${dialCode} ${local}` : ''
}

export function fullToLocal(full: string): string {
  // Remove DDI (+55 ou similar) do início
  return full.replace(/^\+\d{1,3}\s*/, '')
}

export function isLocalPhoneValid(local: string): boolean {
  const digits = local.replace(/\D/g, '')
  return digits.length === 10 || digits.length === 11
}

export function usePhoneInput(initialFull = '') {
  const localPhone = ref(initialFull ? formatLocalPhone(fullToLocal(initialFull)) : '')
  const rawDigits  = ref(localPhone.value.replace(/\D/g, ''))

  function onPhoneInput(e: Event) {
    const input     = (e.target as HTMLInputElement)
    const formatted = formatLocalPhone(input.value)
    rawDigits.value = formatted.replace(/\D/g, '')
    localPhone.value = formatted
    // Força o DOM a refletir o valor formatado (impede dígitos extras no input)
    input.value = formatted
    // Reposiciona cursor no fim após reformatação
    const pos = formatted.length
    requestAnimationFrame(() => input.setSelectionRange(pos, pos))
  }

  const phoneError = computed<string>(() => {
    if (!localPhone.value) return ''
    const d = rawDigits.value
    if (d.length > 0 && d.length < 10) return 'Número incompleto'
    return ''
  })

  const phoneValid = computed(() => !localPhone.value || isLocalPhoneValid(localPhone.value))

  // Valor completo para enviar ao backend
  const phoneFull = computed(() => localToFull(localPhone.value))

  return { localPhone, onPhoneInput, phoneError, phoneValid, phoneFull }
}
