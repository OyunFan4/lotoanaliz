
export const handler = async (event) => {
  const game = event.queryStringParameters?.game;

  if (game !== "sayisal" && game !== "super") {
    return {
      statusCode: 400,
      body: JSON.stringify({
        error: "Gecersiz oyun"
      })
    };
  }

  return {
    statusCode: 200,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store"
    },
    body: JSON.stringify({
      status: "test",
      game,
      results: [],
      message: "Sync fonksiyonu calisiyor. Resmi veri baglantisi henuz kurulmadı."
    })
  };
};
