
export default async function handler() {
  return new Response(
    JSON.stringify({
      ok: true,
      application: "LotoAnaliz AI",
      status: "running",
      message: "Netlify Functions calisiyor"
    }),
    {
      status: 200,
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "no-store"
      }
    }
  );
}

export const config = {
  path: "/api/health"
};

