export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const body = await readBody(event);

  const user = await $fetch(`${config.apiBaseUrl}/api/auth/register`, {
    method: "POST",
    body: {
      email: body.email,
      name: body.name,
      password: body.password,
      phone: body.phone ?? "",
    },
  }).catch((err) => {
    const status = err?.response?.status ?? 400;
    const detail = err?.data?.detail ?? "Erro ao criar conta.";
    throw createError({ statusCode: status, message: detail });
  });

  return { user };
});
