<script setup lang="ts">
useHead({ title: 'Termos de Uso — Wolliz' })
</script>

<template>
  <div class="page">
    <header class="topbar">
      <NuxtLink to="/" class="logo-link">
        <AppLogo size="sm" />
      </NuxtLink>
    </header>

    <main class="content">
      <div class="test-banner" role="alert">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path d="M9 1.5L16.5 15H1.5L9 1.5Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
          <path d="M9 7v3.5M9 12.5v.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span>
          <strong>Página de teste.</strong>
          Este conteúdo é fictício e foi criado apenas para fins de desenvolvimento.
          Os termos reais serão elaborados antes do lançamento oficial do Wolliz.
        </span>
      </div>

      <div class="doc">
        <div class="doc__header">
          <p class="doc__eyebrow">Documento legal</p>
          <h1 class="doc__title">Termos de Uso</h1>
          <p class="doc__meta">Última atualização: 12 de abril de 2026 · Versão 0.1 (rascunho)</p>
        </div>

        <div class="doc__body">
          <section>
            <h2>1. Aceitação dos Termos</h2>
            <p>Ao acessar ou utilizar a plataforma Wolliz, você concorda com estes Termos de Uso. Se você não concordar com qualquer parte destes termos, não poderá utilizar nossos serviços.</p>
          </section>

          <section>
            <h2>2. Descrição do Serviço</h2>
            <p>O Wolliz é um marketplace imobiliário que conecta compradores, vendedores e locatários de imóveis em todo o Brasil. A plataforma oferece ferramentas de busca, listagem e comunicação entre as partes.</p>
          </section>

          <section>
            <h2>3. Cadastro e Conta</h2>
            <p>Para utilizar determinadas funcionalidades, é necessário criar uma conta. Você é responsável por manter a confidencialidade de suas credenciais de acesso e por todas as atividades realizadas com sua conta.</p>
            <p>As informações fornecidas no cadastro devem ser verdadeiras, precisas e atualizadas. O Wolliz reserva o direito de suspender ou encerrar contas que violem esta condição.</p>
          </section>

          <section>
            <h2>4. Uso Permitido</h2>
            <p>Você concorda em utilizar a plataforma apenas para fins lícitos e de acordo com estes termos. É proibido:</p>
            <ul>
              <li>Publicar anúncios falsos ou enganosos;</li>
              <li>Utilizar a plataforma para atividades fraudulentas;</li>
              <li>Realizar scraping ou extração automatizada de dados sem autorização;</li>
              <li>Interferir no funcionamento normal da plataforma.</li>
            </ul>
          </section>

          <section>
            <h2>5. Anúncios e Conteúdo</h2>
            <p>Os usuários são inteiramente responsáveis pelo conteúdo dos anúncios publicados. O Wolliz não se responsabiliza pela veracidade das informações contidas nos anúncios, mas reserva o direito de remover conteúdo que viole estes termos.</p>
          </section>

          <section>
            <h2>6. Propriedade Intelectual</h2>
            <p>Todos os elementos da plataforma Wolliz — incluindo marca, logotipo, design e código-fonte — são de propriedade exclusiva do Wolliz. É proibida a reprodução ou uso sem autorização prévia.</p>
          </section>

          <section>
            <h2>7. Limitação de Responsabilidade</h2>
            <p>O Wolliz não se responsabiliza por danos decorrentes do uso da plataforma, por negociações entre usuários ou por informações imprecisas em anúncios de terceiros.</p>
          </section>

          <section>
            <h2>8. Modificações</h2>
            <p>O Wolliz poderá modificar estes Termos a qualquer momento. As alterações entrarão em vigor após a publicação na plataforma. O uso continuado após as alterações constitui aceitação dos novos termos.</p>
          </section>

          <section>
            <h2>9. Contato</h2>
            <p>Para dúvidas sobre estes Termos de Uso, entre em contato pelo e-mail <strong>legal@wolliz.com.br</strong>.</p>
          </section>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.page {
  min-height: 100dvh;
  background: var(--color-bg);
  font-family: 'DM Sans', var(--font-sans);
}

.topbar {
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
  padding: 0 24px;
  height: 60px;
  display: flex;
  align-items: center;
}

.logo-link {
  text-decoration: none;
  display: flex;
  align-items: center;
}

.content {
  max-width: 720px;
  margin: 0 auto;
  padding: 40px 24px 80px;
}

/* Banner de teste */
.test-banner {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  background: #fffbeb;
  border: 1px solid #fcd34d;
  border-radius: var(--radius-md);
  color: #92400e;
  font-size: 13px;
  line-height: 1.6;
  padding: 14px 16px;
  margin-bottom: 40px;
  flex-shrink: 0;
}

.test-banner svg {
  flex-shrink: 0;
  margin-top: 1px;
  color: #d97706;
}

/* Documento */
.doc__header {
  margin-bottom: 40px;
  padding-bottom: 32px;
  border-bottom: 1px solid var(--color-border);
}

.doc__eyebrow {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--color-brand);
  margin-bottom: 10px;
}

.doc__title {
  font-family: 'Fraunces', serif;
  font-size: 36px;
  font-weight: 600;
  font-style: italic;
  color: var(--color-text);
  letter-spacing: -.03em;
  margin-bottom: 10px;
}

.doc__meta {
  font-size: 13px;
  color: var(--color-text-muted);
}

.doc__body {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

section h2 {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 10px;
  letter-spacing: -.01em;
}

section p {
  font-size: 14px;
  color: #374151;
  line-height: 1.75;
  margin-bottom: 10px;
}

section p:last-child {
  margin-bottom: 0;
}

section ul {
  margin: 8px 0 0 0;
  padding-left: 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

section ul li {
  font-size: 14px;
  color: #374151;
  line-height: 1.6;
}
</style>
