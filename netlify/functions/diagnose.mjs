// LotoAnaliz AI - resmi alan adi baglanti teshisi.
// Veri kaydetmez, erisim engeli asmaz, baska kaynaga basvurmaz.
const ORIGIN = 'https://www.millipiyangoonline.com';
const TARGET = ORIGIN + '/super-loto/cekilis-sonuclari.114.2026';

function respond(payload) {
  return {
    statusCode: 200,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      'Access-Control-Allow-Origin': 'https://lotoanaliz.netlify.app'
    },
    body: JSON.stringify(payload)
  };
}

async function probe(label, url, method) {
  const started = Date.now();
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 7000);
  try {
    const response = await fetch(url, {
      method,
      headers: { Accept: 'text/html' },
      redirect: 'manual',
      signal: ctrl.signal
    });
    let templateDetected = null;
    let bodyBytes = null;
    if (method === 'GET' && response.ok) {
      const raw = await response.text();
      bodyBytes = Buffer.byteLength(raw, 'utf8');
      templateDetected = raw.includes('{{#each winningNumber}}');
    }
    return {
      label, method, outcome: 'http_response',
      httpStatus: response.status, elapsedMs: Date.now() - started,
      bodyBytes, templateDetected
    };
  } catch (err) {
    const timeout = ctrl.signal.aborted;
    return {
      label, method, outcome: timeout ? 'timeout' : 'network_error',
      elapsedMs: Date.now() - started,
      errorCode: timeout ? 'ABORT_TIMEOUT' : (err?.cause?.code || err?.code || err?.name || 'UNKNOWN'),
      message: timeout ? '7000 ms icinde yanit yok' : 'Baglanti kurulurken hata olustu'
    };
  } finally {
    clearTimeout(timer);
  }
}

export const handler = async () => {
  const checks = [];
  // Sirali: tek seferde gereksiz paralel yuk olusturmaz.
  const root = await probe('domain', ORIGIN + '/', 'HEAD');
  checks.push(root);
  if (root.outcome === 'http_response') {
    checks.push(await probe('draw_html', TARGET, 'GET'));
  }
  return respond({
    status: 'diagnostic_only',
    checkedAt: new Date().toISOString(),
    sourceDomain: ORIGIN,
    checks,
    note: 'Bu islem sayi cekmez, veri kaydetmez ve resmi API erisimini kanitlamaz.'
  });
};
