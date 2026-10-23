
const BASE = "https://www.millipiyangoonline.com";

const SOURCES = {
  super: {
    path: "/super-loto/cekilis-sonuclari.114.2026",
    max: 60,
    drawNumber: "114",
    date: "2026-09-22"
  },
  sayisal: {
    path: "/sayisal-loto/cekilis-sonuclari.101.2026",
    max: 90,
    drawNumber: "101",
    date: "2026-08-24"
  }
};

function json(statusCode, data) {
  return {
    statusCode,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store"
    },
    body: JSON.stringify(data)
  };
}

function validNumbers(numbers, max) {
  return Array.isArray(numbers) &&
    numbers.length === 6 &&
    numbers.every(n =>
      Number.isInteger(n) && n >= 1 && n <= max
    ) &&
    new Set(numbers).size === 6;
}

function extractNumbers(html, max) {
  // Only accept an explicit JSON winningNumber array.
  // Never guess numbers from arbitrary page text.
  const match = html.match(
    /["']winningNumber["']\s*:\s*\[([\d,\s]+)\]/
  );

  if (!match) return null;

  const numbers = match[1]
    .split(",")
    .map(x => Number(x.trim()));

  if (!validNumbers(numbers, max)) return null;

  return numbers.sort((a, b) => a - b);
}

export const handler = async (event) => {
  const game = event.queryStringParameters?.game;

  if (!SOURCES[game]) {
    return json(400, {
      status: "error",
      results: [],
      message: "Geçersiz oyun seçimi."
    });
  }

  const source = SOURCES[game];
  const url = BASE + source.path;
  const checkedAt = new Date().toISOString();

  try {
    const response = await fetch(url, {
      headers: {
        "Accept": "text/html",
        "User-Agent": "LotoAnalizAI/1.0"
      },
      signal: AbortSignal.timeout(12000)
    });

    if (!response.ok) {
      return json(200, {
        status: "unavailable",
        game,
        checkedAt,
        results: [],
        sourceUrl: url,
        message: "Resmi site HTTP " + response.status
      });
    }

    const html = await response.text();
    const numbers = extractNumbers(html, source.max);

    if (!numbers) {
      return json(200, {
        status: "unavailable",
        game,
        checkedAt,
        results: [],
        sourceUrl: url,
        message:
          "Sayfa acildi ancak alti sayi guvenle ayrilamadi."
      });
    }

    // The page must also explicitly identify
    // the expected draw date and draw number.
    const dateFound =
      html.includes(source.date) ||
      html.includes(source.date.split("-").reverse().join("."));

    const drawFound = new RegExp(
      "(?:drawNumber|draw_number|drawNo)" +
      "[\"'\\s:]*" + source.drawNumber + "\\b"
    ).test(html);

    if (!dateFound || !drawFound) {
      return json(200, {
        status: "unavailable",
        game,
        checkedAt,
        results: [],
        sourceUrl: url,
        message:
          "Sayilar bulundu ancak tarih veya cekilis no dogrulanamadi."
      });
    }

    return json(200, {
      status: "ok",
      game,
      checkedAt,
      message: "Bir cekilis dogrulandi.",
      results: [{
        game,
        date: source.date,
        drawNumber: source.drawNumber,
        numbers,
        sourceUrl: url
      }]
    });

  } catch (error) {
    return json(200, {
      status: "unavailable",
      game,
      checkedAt,
      results: [],
      sourceUrl: url,
      message: "Baglanti hatasi: " + error.message
    });
  }
};
