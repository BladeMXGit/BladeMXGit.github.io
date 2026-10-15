import sys
import os
import re
import json
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
ARTICULOS_DIR = BASE_DIR / "articulos"
SITE_URL = os.getenv("SITE_URL", "https://blademxgit.github.io")

# Google AdSense Publisher ID (Configurable via env var or placeholder)
ADSENSE_PUB_ID = os.getenv("ADSENSE_PUB_ID", "ca-pub-7532709201895063")
PUB_NUMERIC_ID = ADSENSE_PUB_ID.replace("ca-pub-", "pub-")

# Fixed publish date (only change it when the content really changes)
PUBLISH_DATE_ISO = "2026-10-14"
PUBLISH_DATE_ES = "14 de octubre de 2026"

def get_cookie_banner(prefix=""):
    return f"""
  <!-- Banner de Consentimiento de Cookies (Obligatorio para Google AdSense / RGPD) -->
  <div id="cookie-banner" class="fixed bottom-4 left-4 right-4 md:left-auto md:right-4 md:max-w-md bg-white border border-gray-200 p-5 rounded-2xl shadow-xl z-50 text-sm">
    <p class="text-gray-700 mb-3">
      Utilizamos cookies propias y de terceros (incluido Google AdSense) para analizar el tráfico y mostrar publicidad personalizada. Puedes consultar nuestra <a href="{prefix}legal/cookies.html" class="text-emerald-600 underline font-medium">Política de Cookies</a>.
    </p>
    <div class="flex gap-2 justify-end">
      <button onclick="acceptCookies()" class="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold px-4 py-2 rounded-lg text-xs transition">Aceptar todas</button>
      <button onclick="rejectCookies()" class="bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold px-4 py-2 rounded-lg text-xs transition">Rechazar</button>
    </div>
  </div>
  <script>
    function checkCookies() {{
      if (localStorage.getItem('cookie_consent')) {{
        var el = document.getElementById('cookie-banner');
        if (el) el.style.display = 'none';
      }}
    }}
    function acceptCookies() {{
      localStorage.setItem('cookie_consent', 'accepted');
      var el = document.getElementById('cookie-banner');
      if (el) el.style.display = 'none';
    }}
    function rejectCookies() {{
      localStorage.setItem('cookie_consent', 'rejected');
      var el = document.getElementById('cookie-banner');
      if (el) el.style.display = 'none';
    }}
    checkCookies();
  </script>
    """

# Curated catalog of high-paying Google AdSense search queries (Spain/LatAm)
TOPICS = [
    {
        "slug": "calcular-sueldo-neto-espana-bruto",
        "title": "Cómo calcular tu sueldo neto a partir del bruto en España: Guía paso a paso",
        "category": "Impuestos y Nómina",
        "read_time": "6 min",
        "description": "Aprende a calcular cuánto dinero recibirás en tu nómina tras retenciones de IRPF y Seguridad Social. Tablas de tramos y ejemplos prácticos.",
        "content_html": """
        <p class="text-lg text-gray-700 leading-relaxed mb-6 font-medium">Cuando negocias una oferta de trabajo o te anuncian una subida salarial, la cifra que siempre te indican es el <strong>sueldo bruto anual</strong>. Sin embargo, lo que realmente ingresa en tu cuenta bancaria a final de mes es el sueldo neto. En esta guía te explicamos cómo se calcula y qué factores determinan lo que Hacienda y la Seguridad Social retienen.</p>

        <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4 border-b border-gray-200 pb-2">1. ¿Qué deducciones se aplican al salario bruto?</h2>
        <p class="text-gray-700 mb-4">Para pasar del salario bruto al neto se aplican principalmente dos grandes conceptos de retención obligatoria:</p>
        <ul class="list-disc pl-6 space-y-2 text-gray-700 mb-6">
          <li><strong>Cotizaciones a la Seguridad Social:</strong> Generalmente suponen un <strong>6,35% a 6,45%</strong> del salario bruto (incluye contingencias comunes, desempleo y formación profesional).</li>
          <li><strong>Retención del IRPF:</strong> Es un pago a cuenta del Impuesto sobre la Renta de las Personas Físicas. No es fijo: varía según el importe del salario, tu situación familiar (hijos a cargo, personas dependientes) y tu comunidad autónoma.</li>
        </ul>

        <div class="bg-emerald-50 border-l-4 border-emerald-500 p-5 rounded-r-xl my-6">
          <p class="text-emerald-900 font-semibold mb-1">💡 Regla práctica rápida:</p>
          <p class="text-emerald-800 text-sm">En salarios medios en España (entre 20.000€ y 35.000€ brutos anuales), el sueldo neto mensual suele situarse entre el <strong>75% y el 80%</strong> del salario bruto mensual si cobras en 12 pagas.</p>
        </div>

        <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4 border-b border-gray-200 pb-2">2. Tabla de tramos de IRPF aplicables</h2>
        <p class="text-gray-700 mb-4">El IRPF es un impuesto progresivo. Esto significa que no se tributa todo el sueldo al porcentaje más alto, sino que se divide en tramos:</p>
        <div class="overflow-x-auto my-6">
          <table class="min-w-full bg-white border border-gray-200 text-sm rounded-lg shadow-sm">
            <thead>
              <tr class="bg-gray-100 text-gray-700 text-left">
                <th class="py-3 px-4 font-semibold border-b">Tramo de base liquidable</th>
                <th class="py-3 px-4 font-semibold border-b">Tipo estatal + autonómico orientativo</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 text-gray-700">
              <tr><td class="py-2.5 px-4">De 0 € a 12.450 €</td><td class="py-2.5 px-4 font-medium">19%</td></tr>
              <tr><td class="py-2.5 px-4">De 12.450 € a 20.200 €</td><td class="py-2.5 px-4 font-medium">24%</td></tr>
              <tr><td class="py-2.5 px-4">De 20.200 € a 35.200 €</td><td class="py-2.5 px-4 font-medium">30%</td></tr>
              <tr><td class="py-2.5 px-4">De 35.200 € a 60.000 €</td><td class="py-2.5 px-4 font-medium">37%</td></tr>
              <tr><td class="py-2.5 px-4">De 60.000 € a 300.000 €</td><td class="py-2.5 px-4 font-medium">45%</td></tr>
            </tbody>
          </table>
        </div>

        <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4 border-b border-gray-200 pb-2">3. ¿Cómo optimizar tu retención para que no te salga a pagar?</h2>
        <p class="text-gray-700 mb-4">Si tu empresa te aplica una retención de IRPF inferior a la que te corresponde (algo habitual al inicio de contratos temporales), recibirás más dinero cada mes, pero en la Declaración de la Renta de primavera te tocará pagar la diferencia de golpe. Puedes solicitar a Recursos Humanos rellenar el <strong>Modelo 145</strong> para ajustar tu retención al porcentaje real.</p>
        """
    },
    {
        "slug": "metodo-50-30-20-ahorro-personal",
        "title": "La regla 50/30/20: El método definitivo para organizar tu dinero y ahorrar sin sufrir",
        "category": "Ahorro y Presupuesto",
        "read_time": "5 min",
        "description": "Descubre cómo repartir tus ingresos mensuales según la famosa regla 50/30/20 para ahorrar el 20% de tu sueldo todos los meses de forma automática.",
        "content_html": """
        <p class="text-lg text-gray-700 leading-relaxed mb-6 font-medium">Ahorrar dinero todos los meses suele parecer difícil cuando no se tiene un sistema claro. La regla 50/30/20, popularizada por la profesora de Harvard Elizabeth Warren, es uno de los métodos presupuestarios más reconocidos a nivel global por su sencillez y eficacia.</p>

        <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4 border-b border-gray-200 pb-2">1. ¿En qué consiste la división 50/30/20?</h2>
        <p class="text-gray-700 mb-4">El método consiste en dividir tus <strong>ingresos netos mensuales</strong> en tres categorías estrictas:</p>
        
        <div class="grid md:grid-cols-3 gap-6 my-6">
          <div class="bg-blue-50 border border-blue-200 p-5 rounded-xl">
            <span class="text-blue-600 font-bold text-xl block mb-2">50% Necesidades</span>
            <p class="text-gray-700 text-sm">Alquiler o hipoteca, suministros (luz, agua, internet), comida básica, transporte y seguros indispensables.</p>
          </div>
          <div class="bg-amber-50 border border-amber-200 p-5 rounded-xl">
            <span class="text-amber-600 font-bold text-xl block mb-2">30% Deseos y Ocio</span>
            <p class="text-gray-700 text-sm">Cenas fuera, suscripciones a streaming, salidas con amigos, ropa no esencial, aficiones y viajes.</p>
          </div>
          <div class="bg-emerald-50 border border-emerald-200 p-5 rounded-xl">
            <span class="text-emerald-600 font-bold text-xl block mb-2">20% Ahorro / Deudas</span>
            <p class="text-gray-700 text-sm">Fondo de emergencias, inversión en fondos indexados o amortización acelerada de préstamos costosos.</p>
          </div>
        </div>

        <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4 border-b border-gray-200 pb-2">2. Ejemplo práctico con un sueldo de 1.500 € netos</h2>
        <ul class="list-disc pl-6 space-y-2 text-gray-700 mb-6">
          <li><strong>750 € (50%):</strong> Destinados al pago de la vivienda, compra en el supermercado y gastos fijos.</li>
          <li><strong>450 € (30%):</strong> Presupuesto libre para disfrutar del mes sin sentir culpa.</li>
          <li><strong>300 € (20%):</strong> Ahorro automático que se transfiere el día 1 de mes a una cuenta remunerada o fondo.</li>
        </ul>

        <div class="bg-gray-100 p-5 rounded-xl text-gray-800 text-sm my-6">
          <strong>⚡ El truco psicológico: "Págate a ti primero"</strong><br>
          En lugar de esperar a final de mes para ahorrar lo que sobre (que casi nunca sobra nada), programa una transferencia automática de ese 20% el mismo día en que cobras tu nómina.
        </div>
        """
    },
    {
        "slug": "cuentas-remuneradas-mejores-opciones",
        "title": "Cuentas remuneradas vs Depósitos a plazo fijo: Dónde rentabilizar tu dinero seguro",
        "category": "Inversión y Bancos",
        "read_time": "7 min",
        "description": "Comparativa de las mejores opciones para no perder poder adquisitivo con la inflación. Disponibilidad total frente a tipos de interés fijos.",
        "content_html": """
        <p class="text-lg text-gray-700 leading-relaxed mb-6 font-medium">Tener el dinero ahorrado en una cuenta corriente tradicional que no te da nada es la forma más rápida de perder poder adquisitivo año tras año por culpa de la inflación. Afortunadamente, hoy en día existen herramientas bancarias con total garantía del Fondo de Garantía de Depósitos (hasta 100.000€ por titular).</p>

        <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4 border-b border-gray-200 pb-2">1. Diferencias clave entre Cuenta Remunerada y Depósito</h2>
        <div class="overflow-x-auto my-6">
          <table class="min-w-full bg-white border border-gray-200 text-sm rounded-lg shadow-sm">
            <thead>
              <tr class="bg-gray-100 text-gray-700 text-left">
                <th class="py-3 px-4 font-semibold border-b">Característica</th>
                <th class="py-3 px-4 font-semibold border-b">Cuenta Remunerada</th>
                <th class="py-3 px-4 font-semibold border-b">Depósito a Plazo Fijo</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 text-gray-700">
              <tr><td class="py-2.5 px-4 font-semibold">Disponibilidad del dinero</td><td class="py-2.5 px-4 text-emerald-600 font-medium">Inmediata (en cualquier momento)</td><td class="py-2.5 px-4 text-amber-600 font-medium">Bloqueado hasta vencimiento</td></tr>
              <tr><td class="py-2.5 px-4 font-semibold">Tipo de interés (TIN / TAE)</td><td class="py-2.5 px-4">Puede variar con aviso previo</td><td class="py-2.5 px-4">Garantizado y fijo durante el plazo</td></tr>
              <tr><td class="py-2.5 px-4 font-semibold">Ideal para...</td><td class="py-2.5 px-4">Fondo de emergencias y ahorro diario</td><td class="py-2.5 px-4">Dinero que no vas a usar a 1-3 años</td></tr>
            </tbody>
          </table>
        </div>

        <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4 border-b border-gray-200 pb-2">2. ¿Cómo tributan los intereses en la Renta?</h2>
        <p class="text-gray-700 mb-4">Los rendimientos generados por cuentas bancarias y depósitos tributan en la base del ahorro según los siguientes tramos:</p>
        <ul class="list-disc pl-6 space-y-2 text-gray-700 mb-6">
          <li>Hasta 6.000 € de beneficios: <strong>19%</strong></li>
          <li>Entre 6.000 € y 50.000 €: <strong>21%</strong></li>
          <li>Entre 50.000 € y 200.000 €: <strong>23%</strong></li>
        </ul>
        <p class="text-gray-700">El propio banco español suele aplicar automáticamente la retención fiscal del 19% cada vez que te abona los intereses en cuenta.</p>
        """
    },
    {
        "slug": "que-es-un-fondo-de-emergencia-guia",
        "title": "Fondo de Emergencia: Cuántos meses de gastos necesitas y dónde guardarlo",
        "category": "Ahorro y Seguridad",
        "read_time": "5 min",
        "description": "La piedra angular de cualquier economía familiar sana. Aprende a calcular el importe exacto para tu tranquilidad ante imprevistos laborales o médicos.",
        "content_html": """
        <p class="text-lg text-gray-700 leading-relaxed mb-6 font-medium">Antes de pensar en invertir en bolsa, criptomonedas o bienes raíces, existe un paso previo fundamental que separa a las personas con tranquilidad financiera de aquellas que viven con estrés constante: el <strong>fondo de emergencia</strong>.</p>

        <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4 border-b border-gray-200 pb-2">1. ¿Qué es exactamente y para qué sirve?</h2>
        <p class="text-gray-700 mb-4">Un fondo de emergencia es una cantidad de dinero líquido reservada exclusivamente para afrontar imprevistos graves: una avería importante del coche, una urgencia médica, la pérdida de empleo o una reforma inaplazable en la vivienda. Su función no es hacerte rico, sino darte paz mental y evitar que recurras a créditos rápidos o tarjetas revolving con intereses desorbitados del 20%.</p>

        <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4 border-b border-gray-200 pb-2">2. ¿Cuánto dinero debes tener ahorrado?</h2>
        <p class="text-gray-700 mb-4">La regla general depende de tu estabilidad laboral:</p>
        <div class="space-y-4 my-6">
          <div class="border-l-4 border-blue-500 pl-4 py-1">
            <h3 class="font-bold text-gray-900">3 a 6 meses de gastos fijos:</h3>
            <p class="text-gray-600 text-sm">Recomendado para empleados asalariados con contratos indefinidos o funcionarios con ingresos muy previsibles.</p>
          </div>
          <div class="border-l-4 border-amber-500 pl-4 py-1">
            <h3 class="font-bold text-gray-900">6 a 12 meses de gastos fijos:</h3>
            <p class="text-gray-600 text-sm">Imprescindible para trabajadores autónomos, freelancers o personas con ingresos variables o comisiones.</p>
          </div>
        </div>

        <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4 border-b border-gray-200 pb-2">3. ¿Dónde guardarlo para que no pierda valor?</h2>
        <p class="text-gray-700 mb-4">El fondo de emergencia debe cumplir dos condiciones obligatorias: <strong>seguridad máxima (riesgo 0)</strong> y <strong>liquidez inmediata (poder sacarlo en 24h)</strong>. Por tanto, nunca debe invertirse en acciones o fondos de renta variable. El mejor lugar es una <strong>cuenta remunerada de alta rentabilidad</strong> que genere intereses cada mes mientras el dinero espera.</p>
        """
    },
    {
        "slug": "desgravar-alquiler-declaracion-renta",
        "title": "Cómo deducir el alquiler en la Declaración de la Renta: Deducción estatal y autonómica",
        "category": "Impuestos y Renta",
        "read_time": "6 min",
        "description": "Conoce los requisitos y casillas exactas para ahorrarte hasta 1.000€ en tu IRPF si vives de alquiler. Diferencias por comunidades autónomas.",
        "content_html": """
        <p class="text-lg text-gray-700 leading-relaxed mb-6 font-medium">El alquiler es uno de los gastos más pesados para millones de familias y jóvenes. Sin embargo, muchos inquilinos desconocen que pueden recuperar cientos de euros en su Declaración de la Renta si aprovechan las deducciones fiscales disponibles tanto a nivel estatal como autonómico.</p>

        <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4 border-b border-gray-200 pb-2">1. Deducción estatal por alquiler</h2>
        <p class="text-gray-700 mb-4">La deducción estatal solo es aplicable si tu contrato de alquiler es anterior al <strong>1 de enero de 2015</strong> y tu base imponible es inferior a 24.107,20 € anuales. Si tu contrato es más reciente, la ayuda estatal ya no aplica, pero es en las deducciones autonómicas donde está la verdadera oportunidad.</p>

        <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4 border-b border-gray-200 pb-2">2. Deducciones autonómicas (La gran ventaja)</h2>
        <p class="text-gray-700 mb-4">Casi todas las comunidades autónomas ofrecen deducciones generosas para inquilinos, especialmente para jóvenes de hasta 35 años o familias con rentas medias y bajas:</p>
        <ul class="list-disc pl-6 space-y-2 text-gray-700 mb-6">
          <li><strong>Comunidad de Madrid:</strong> Deducción del 30% de las cantidades pagadas, hasta un máximo de 1.237,20 € anuales para menores de 35 años o personas desempleadas.</li>
          <li><strong>Cataluña:</strong> Deducción del 10% hasta 300 € (o 600 € en familias numerosas o monoparentales).</li>
          <li><strong>Comunidad Valenciana:</strong> Deducción entre el 20% y el 25% con límites de hasta 800 € a 1.000 €.</li>
          <li><strong>Andalucía:</strong> Deducción del 15% hasta un tope de 600 € anuales para menores de 35 años.</li>
        </ul>

        <div class="bg-amber-50 border-l-4 border-amber-500 p-5 rounded-r-xl my-6">
          <p class="text-amber-900 font-semibold mb-1">⚠️ Requisito indispensable para que Hacienda no te multe:</p>
          <p class="text-amber-800 text-sm">En la mayoría de comunidades autónomas es obligatorio que el propietario haya depositado la fianza legal del alquiler en el organismo autonómico correspondiente (como el IVIMA en Madrid o el INCASÒL en Cataluña).</p>
        </div>
        """
    }
]

def render_article_html(topic: dict) -> str:
    """Generates a complete, standalone, high-PageSpeed SEO article page."""
    slug = topic["slug"]
    title = topic["title"]
    desc = topic["description"]
    cat = topic["category"]
    read_time = topic["read_time"]
    date_str = PUBLISH_DATE_ES
    iso_date = PUBLISH_DATE_ISO
    url = f"{SITE_URL}/articulos/{slug}.html"

    # AdSense Placement Templates (Ready for publisher client ID)
    ad_box = f"""
    <!-- ESPACIO DE ANUNCIO GOOGLE ADSENSE -->
    <div class="my-8 p-4 bg-gray-50 border border-dashed border-gray-300 rounded-xl text-center text-xs text-gray-400">
      <span class="block uppercase tracking-wider mb-2 font-semibold text-gray-400">Publicidad</span>
      <div class="min-h-[100px] flex items-center justify-center bg-white rounded border border-gray-200">
        <ins class="adsbygoogle"
             style="display:block; text-align:center;"
             data-ad-layout="in-article"
             data-ad-format="fluid"
             data-ad-client="{ADSENSE_PUB_ID}"
             data-ad-slot="XXXXXXXXXX"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>
    </div>
    """

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Finanzas Inteligentes</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  
  <!-- Verificación oficial para Google AdSense -->
  <meta name="google-adsense-account" content="{ADSENSE_PUB_ID}">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB_ID}" crossorigin="anonymous"></script>

  <!-- Open Graph / Redes Sociales -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  
  <!-- Schema.org JSON-LD para Google Search Rich Snippets -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "{desc}",
    "author": {{
      "@type": "Organization",
      "name": "Finanzas Inteligentes"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "Finanzas Inteligentes"
    }},
    "datePublished": "{iso_date}",
    "dateModified": "{iso_date}"
  }}
  </script>

  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-800 antialiased font-sans">
  <!-- Navegación Superior -->
  <header class="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
    <div class="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
      <a href="../index.html" class="text-xl font-bold text-emerald-600 flex items-center gap-2">
        <span>📈 Finanzas Inteligentes</span>
      </a>
      <a href="../index.html" class="text-sm font-medium text-gray-600 hover:text-emerald-600">← Ver todas las guías</a>
    </div>
  </header>

  <!-- Contenido Principal -->
  <main class="max-w-3xl mx-auto px-4 py-10">
    <article class="bg-white p-6 sm:p-10 rounded-2xl shadow-sm border border-gray-100">
      <!-- Breadcrumbs -->
      <nav class="text-xs text-gray-500 mb-4 flex items-center gap-2">
        <a href="../index.html" class="hover:underline">Inicio</a> &gt;
        <span class="text-emerald-600 font-medium">{cat}</span>
      </nav>

      <!-- Encabezado del Artículo -->
      <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 leading-tight mb-4">
        {title}
      </h1>

      <div class="flex flex-wrap items-center gap-4 text-xs text-gray-500 mb-8 border-b border-gray-100 pb-4">
        <span class="bg-emerald-100 text-emerald-800 px-2.5 py-1 rounded-full font-semibold">{cat}</span>
        <span>⏱️ Lectura: {read_time}</span>
        <span>📅 Actualizado: {date_str}</span>
      </div>

      <!-- Anuncio Superior -->
      {ad_box}

      <!-- Cuerpo del Artículo -->
      <div class="prose max-w-none">
        {topic["content_html"]}
      </div>

      <!-- Anuncio Inferior -->
      {ad_box}

      <!-- Caja de Conclusión / Compartir -->
      <div class="mt-10 p-6 bg-emerald-50 rounded-xl border border-emerald-100">
        <h3 class="font-bold text-emerald-900 text-lg mb-2">¿Te ha resultado útil esta guía?</h3>
        <p class="text-emerald-800 text-sm mb-4">Guarda esta página en tus marcadores y compártela con quien quiera mejorar sus finanzas y pagar menos comisiones.</p>
        <a href="../index.html" class="inline-block bg-emerald-600 text-white font-medium text-sm px-5 py-2.5 rounded-lg hover:bg-emerald-700 transition">Explorar más guías de finanzas</a>
      </div>
    </article>
  </main>

  <!-- Pie de página con enlaces legales obligatorios para Google AdSense -->
  <footer class="bg-gray-900 text-gray-400 py-10 mt-16 text-sm border-t border-gray-800">
    <div class="max-w-4xl mx-auto px-4 text-center">
      <div class="flex justify-center gap-6 mb-4">
        <a href="../legal/aviso-legal.html" class="hover:text-white">Aviso Legal</a>
        <a href="../legal/privacidad.html" class="hover:text-white">Política de Privacidad</a>
        <a href="../legal/cookies.html" class="hover:text-white">Cookies</a>
      </div>
      <p class="text-xs text-gray-500">&copy; 2026 Finanzas Inteligentes. El contenido de este portal tiene fines exclusivamente educativos y no constituye asesoramiento financiero formal.</p>
    </div>
  </footer>

  {get_cookie_banner(prefix="../")}
</body>
</html>
"""

def render_home_index_html(topics: list) -> str:
    """Generates the main portal index.html with all article cards and modern layout."""
    cards_html = ""
    for t in topics:
        slug = t["slug"]
        title = t["title"]
        desc = t["description"]
        cat = t["category"]
        read_time = t["read_time"]
        cards_html += f"""
        <article class="bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition p-6 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between text-xs text-gray-500 mb-3">
              <span class="bg-emerald-50 text-emerald-700 font-semibold px-2.5 py-1 rounded-full">{cat}</span>
              <span>⏱️ {read_time}</span>
            </div>
            <h2 class="text-xl font-bold text-gray-900 mb-3 hover:text-emerald-600 leading-snug">
              <a href="articulos/{slug}.html">{title}</a>
            </h2>
            <p class="text-gray-600 text-sm leading-relaxed mb-4">
              {desc}
            </p>
          </div>
          <a href="articulos/{slug}.html" class="text-emerald-600 font-semibold text-sm hover:underline flex items-center gap-1 mt-2">
            Leer guía completa →
          </a>
        </article>
        """

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Finanzas Inteligentes | Guías de Ahorro, Impuestos e Inversión</title>
  <meta name="description" content="Portal educativo de finanzas personales, optimización de impuestos, cuentas remuneradas y métodos prácticos para ahorrar e invertir con inteligencia.">
  <link rel="canonical" href="{SITE_URL}/">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="Finanzas Inteligentes | Guías de Ahorro e Inversión">
  <meta property="og:description" content="Aprende a gestionar tu dinero, calcular tu sueldo neto y rentabilizar tus ahorros sin complicaciones.">
  <meta property="og:url" content="{SITE_URL}/">

  <!-- Verificación oficial para Google AdSense -->
  <meta name="google-adsense-account" content="{ADSENSE_PUB_ID}">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB_ID}" crossorigin="anonymous"></script>

  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-800 antialiased font-sans">
  <!-- Barra de Navegación -->
  <header class="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
    <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
      <a href="index.html" class="text-xl font-extrabold text-emerald-600 flex items-center gap-2">
        <span>📈 Finanzas Inteligentes</span>
      </a>
      <span class="text-xs bg-emerald-100 text-emerald-800 font-bold px-3 py-1 rounded-full">Edición 2026</span>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="bg-gradient-to-b from-white to-gray-50 py-16 border-b border-gray-100 text-center px-4">
    <div class="max-w-3xl mx-auto">
      <span class="text-emerald-600 font-bold text-sm uppercase tracking-wider mb-2 block">Educación Financiera Práctica</span>
      <h1 class="text-4xl sm:text-5xl font-black text-gray-900 leading-tight mb-4">
        Haz que tu dinero trabaje para ti, <span class="text-emerald-600">no al revés</span>.
      </h1>
      <p class="text-gray-600 text-base sm:text-lg mb-8 leading-relaxed">
        Guías claras y paso a paso para calcular tu nómina, pagar menos impuestos legalmente y poner a rentar tus ahorros con riesgo cero.
      </p>
    </div>
  </section>

  <!-- Espacio de Anuncio Principal AdSense -->
  <div class="max-w-5xl mx-auto px-4 my-8">
    <div class="p-4 bg-white border border-dashed border-gray-300 rounded-xl text-center text-xs text-gray-400">
      <span class="block uppercase tracking-wider mb-2 font-semibold text-gray-400">Publicidad</span>
      <div class="min-h-[90px] flex items-center justify-center bg-gray-50 rounded">
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="{ADSENSE_PUB_ID}"
             data-ad-slot="XXXXXXXXXX"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>
    </div>
  </div>

  <!-- Cuadrícula de Artículos -->
  <main class="max-w-6xl mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-8">
      <h2 class="text-2xl font-black text-gray-900">Guías Destacadas</h2>
      <span class="text-sm text-gray-500">{len(topics)} guías publicadas</span>
    </div>

    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      {cards_html}
    </div>
  </main>

  <!-- Footer Legal Obligatorio para AdSense -->
  <footer class="bg-gray-900 text-gray-400 py-12 mt-20 text-sm border-t border-gray-800">
    <div class="max-w-6xl mx-auto px-4 text-center">
      <div class="flex justify-center gap-6 mb-4 font-medium">
        <a href="legal/aviso-legal.html" class="hover:text-white">Aviso Legal</a>
        <a href="legal/privacidad.html" class="hover:text-white">Política de Privacidad</a>
        <a href="legal/cookies.html" class="hover:text-white">Cookies</a>
      </div>
      <p class="text-xs text-gray-500 max-w-2xl mx-auto mb-2">
        El contenido de Finanzas Inteligentes es estrictamente informativo. No prestamos servicios de intermediación crediticia ni asesoramiento financiero formal según la CNMV.
      </p>
      <p class="text-xs text-gray-600">&copy; 2026 Finanzas Inteligentes. Todos los derechos reservados.</p>
    </div>
  </footer>

  {get_cookie_banner(prefix="")}
</body>
</html>
"""

def generate_sitemap(topics: list) -> str:
    """Generates sitemap.xml for instant indexing by Googlebot."""
    today = PUBLISH_DATE_ISO
    urls = [
        f"""  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <priority>1.0</priority>
  </url>"""
    ]
    for t in topics:
        urls.append(f"""  <url>
    <loc>{SITE_URL}/articulos/{t['slug']}.html</loc>
    <lastmod>{today}</lastmod>
    <priority>0.8</priority>
  </url>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""

def build_all():
    print("🚀 Compilando portal web 'Finanzas Inteligentes'...")
    ARTICULOS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Build individual articles
    for topic in TOPICS:
        html = render_article_html(topic)
        article_file = ARTICULOS_DIR / f"{topic['slug']}.html"
        article_file.write_text(html, encoding="utf-8")
        print(f"  📄 Artículo generado: articulos/{topic['slug']}.html")

    # 2. Build index.html
    home_html = render_home_index_html(TOPICS)
    (BASE_DIR / "index.html").write_text(home_html, encoding="utf-8")
    print("  🏠 Página de inicio generada: index.html")

    # 3. Build sitemap.xml
    sitemap = generate_sitemap(TOPICS)
    (BASE_DIR / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print("  🗺️ Mapa del sitio generado: sitemap.xml")

    # 4. Build ads.txt
    ads_txt_content = f"# Archivo ads.txt para verificación oficial de Google AdSense\ngoogle.com, {PUB_NUMERIC_ID}, DIRECT, f08c47fec0942fa0\n"
    (BASE_DIR / "ads.txt").write_text(ads_txt_content, encoding="utf-8")
    print(f"  💰 ads.txt generado: {PUB_NUMERIC_ID}")

    print(f"\n✅ Portal compilado con éxito. {len(TOPICS)} artículos listos para Google AdSense.")

if __name__ == "__main__":
    build_all()
