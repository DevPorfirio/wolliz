/**
 * Django retorna URLs internas do Docker (minio:9000).
 * Substitui pelo endereço público para o browser conseguir acessar.
 */
export function fixAvatarUrl(user: any): any {
  if (!user) return user
  if (user.avatar_url && typeof user.avatar_url === 'string') {
    user.avatar_url = user.avatar_url
      .replace('http://minio:9000', process.env.NUXT_PUBLIC_CDN_URL?.replace(/\/wolliz-static.*$/, '') ?? 'http://localhost:9000')
  }
  return user
}
