<script setup lang="ts">
useHead({ title: 'Política de Privacidade — Wolliz' })
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
          A política de privacidade real será elaborada antes do lançamento oficial do Wolliz,
          em conformidade com a LGPD.
        </span>
      </div>

      <div class="doc">
        <div class="doc__header">
          <p class="doc__eyebrow">Documento legal</p>
          <h1 class="doc__title">Política de Privacidade</h1>
          <p class="doc__meta">Última atualização: 12 de abril de 2026 · Versão 0.1 (rascunho)</p>
        </div>

        <div class="doc__body">
          <section>
            <h2>1. Introdução</h2>
            <p>O Wolliz está comprometido com a proteção dos seus dados pessoais. Esta Política de Privacidade descreve como coletamos, usamos e protegemos suas informações em conformidade com a Lei Geral de Proteção de Dados (LGPD — Lei nº 13.709/2018).</p>
          </section>

          <section>
            <h2>2. Dados Coletados</h2>
            <p>Coletamos as seguintes categorias de dados:</p>
            <ul>
              <li><strong>Dados de cadastro:</strong> nome, e-mail e telefone fornecidos no momento do registro;</li>
              <li><strong>Dados de uso:</strong> páginas visitadas, buscas realizadas e imóveis visualizados;</li>
              <li><strong>Dados de dispositivo:</strong> endereço IP, tipo de navegador e sistema operacional;</li>
              <li><strong>Dados de comunicação:</strong> mensagens trocadas com outros usuários pela plataforma.</li>
            </ul>
          </section>

          <section>
            <h2>3. Finalidade do Tratamento</h2>
            <p>Seus dados são utilizados para:</p>
            <ul>
              <li>Prover e melhorar os serviços da plataforma;</li>
              <li>Personalizar sua experiência de busca de imóveis;</li>
              <li>Enviar notificações relevantes sobre imóveis de interesse;</li>
              <li>Garantir a segurança e prevenir fraudes;</li>
              <li>Cumprir obrigações legais e regulatórias.</li>
            </ul>
          </section>

          <section>
            <h2>4. Compartilhamento de Dados</h2>
            <p>Não vendemos seus dados pessoais a terceiros. Podemos compartilhar informações com:</p>
            <ul>
              <li>Prestadores de serviços essenciais à operação da plataforma (hospedagem, pagamentos);</li>
              <li>Autoridades competentes quando exigido por lei.</li>
            </ul>
          </section>

          <section>
            <h2>5. Seus Direitos (LGPD)</h2>
            <p>Você tem direito a:</p>
            <ul>
              <li>Confirmar a existência de tratamento de seus dados;</li>
              <li>Acessar os dados que temos sobre você;</li>
              <li>Corrigir dados incompletos, inexatos ou desatualizados;</li>
              <li>Solicitar a anonimização, bloqueio ou eliminação de dados desnecessários;</li>
              <li>Portabilidade dos seus dados;</li>
              <li>Revogar o consentimento a qualquer momento.</li>
            </ul>
            <p>Para exercer esses direitos, entre em contato pelo e-mail <strong>privacidade@wolliz.com.br</strong>.</p>
          </section>

          <section>
            <h2>6. Cookies</h2>
            <p>Utilizamos cookies para melhorar a experiência de navegação, manter sua sessão ativa e analisar o uso da plataforma. Você pode configurar seu navegador para recusar cookies, mas isso pode limitar algumas funcionalidades.</p>
          </section>

          <section>
            <h2>7. Retenção de Dados</h2>
            <p>Mantemos seus dados pelo tempo necessário para a prestação dos serviços ou conforme exigido por lei. Após a exclusão da conta, os dados são anonimizados ou eliminados em até 90 dias, salvo obrigação legal em contrário.</p>
          </section>

          <section>
            <h2>8. Segurança</h2>
            <p>Adotamos medidas técnicas e organizacionais para proteger seus dados contra acesso não autorizado, perda ou destruição. Isso inclui criptografia em trânsito (HTTPS) e em repouso, controle de acesso e monitoramento contínuo.</p>
          </section>

          <section>
            <h2>9. Contato e DPO</h2>
            <p>Para dúvidas sobre esta Política ou para exercer seus direitos, entre em contato com nosso Encarregado de Proteção de Dados (DPO) pelo e-mail <strong>privacidade@wolliz.com.br</strong>.</p>
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
}

.test-banner svg {
  flex-shrink: 0;
  margin-top: 1px;
  color: #d97706;
}

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
