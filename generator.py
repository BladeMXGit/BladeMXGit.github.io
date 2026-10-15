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

# Google AdSense Publisher ID
ADSENSE_PUB_ID = os.getenv("ADSENSE_PUB_ID", "ca-pub-7532709201895063")
PUB_NUMERIC_ID = ADSENSE_PUB_ID.replace("ca-pub-", "pub-")

PUBLISH_DATE_ISO = "2026-10-14"
PUBLISH_DATE_ES = "14 de octubre de 2026"

def get_head_assets():
    return """
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script>
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    function toggleDarkMode() {
      if (document.documentElement.classList.contains('dark')) {
        document.documentElement.classList.remove('dark');
        localStorage.theme = 'light';
      } else {
        document.documentElement.classList.add('dark');
        localStorage.theme = 'dark';
      }
    }
  </script>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          },
          colors: {
            hud: {
              line: 'rgba(255, 255, 255, 0.08)',
              linelight: '#E4E6EB',
              bgdark: '#08090C',
              carddark: '#0E1118',
              accent: '#10B981',
              cyan: '#06B6D4'
            }
          }
        }
      }
    }
  </script>
  <style>
    .grid-bg-dark {
      background-image: radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px);
      background-size: 24px 24px;
    }
    .grid-bg-light {
      background-image: radial-gradient(rgba(0, 0, 0, 0.06) 1px, transparent 1px);
      background-size: 24px 24px;
    }
  </style>
    """

def get_hud_navbar(is_subpage=False):
    prefix = "../" if is_subpage else ""
    return f"""
  <!-- Navbar estilo ArtCraft (Bordes técnicos finos, HUD mono y divisores continuos) -->
  <header class="sticky top-0 z-50 w-full border-b border-gray-200 dark:border-hud-line bg-white/90 dark:bg-hud-bgdark/90 backdrop-blur-md">
    <div class="flex h-13 items-stretch justify-between max-w-[1400px] mx-auto">
      
      <!-- Logo + Ticker -->
      <div class="flex items-stretch min-w-0">
        <a href="{prefix}index.html" class="flex items-center gap-2.5 px-4 sm:px-6 border-r border-gray-200 dark:border-hud-line hover:bg-gray-50 dark:hover:bg-hud-carddark transition">
          <div class="w-6 h-6 rounded bg-emerald-500 text-black font-mono font-black text-xs flex items-center justify-center shadow-sm">
            FI
          </div>
          <span class="font-mono font-bold tracking-tight text-sm text-gray-900 dark:text-white uppercase">
            Finanzas<span class="text-emerald-500">.Craft</span>
          </span>
          <span class="hidden lg:inline-block font-mono text-[10px] text-emerald-500 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded ml-1">
            v2.4
          </span>
        </a>

        <!-- Live Ticker HUD -->
        <div class="hidden xl:flex items-center gap-4 px-5 font-mono text-[11px] text-gray-500 dark:text-gray-400 border-r border-gray-200 dark:border-hud-line">
          <span class="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400 font-semibold">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> MERCADOS LIVE
          </span>
          <span class="text-gray-300 dark:text-gray-700">/</span>
          <span>BCE: <strong class="text-gray-900 dark:text-white">3.25%</strong></span>
          <span class="text-gray-300 dark:text-gray-700">/</span>
          <span>EURÍBOR: <strong class="text-gray-900 dark:text-white">2.78%</strong></span>
          <span class="text-gray-300 dark:text-gray-700">/</span>
          <span>DEPÓSITOS: <strong class="text-emerald-500">3.70% TAE</strong></span>
        </div>
      </div>

      <!-- Links & Acciones -->
      <div class="flex items-stretch">
        <a href="{prefix}index.html#simulador" class="hidden md:flex items-center px-4 font-mono text-[11px] uppercase tracking-wider text-gray-600 dark:text-gray-300 hover:text-emerald-500 hover:bg-gray-50 dark:hover:bg-hud-carddark border-l border-gray-200 dark:border-hud-line transition">
          [ 01 // SIMULADOR ]
        </a>
        <a href="{prefix}index.html#guias" class="hidden sm:flex items-center px-4 font-mono text-[11px] uppercase tracking-wider text-gray-600 dark:text-gray-300 hover:text-emerald-500 hover:bg-gray-50 dark:hover:bg-hud-carddark border-l border-gray-200 dark:border-hud-line transition">
          [ 02 // GUÍAS ]
        </a>

        <!-- Botón Modo Oscuro ArtCraft -->
        <button onclick="toggleDarkMode()" aria-label="Cambiar tema" class="w-12 flex items-center justify-center text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-50 dark:hover:bg-hud-carddark border-l border-gray-200 dark:border-hud-line transition">
          <svg class="w-4 h-4 hidden dark:block text-amber-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
          <svg class="w-4 h-4 block dark:hidden text-gray-800" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
        </button>

        <!-- CTA Button ArtCraft style -->
        <a href="{prefix}index.html#simulador" class="flex items-center justify-center px-5 font-mono font-bold uppercase tracking-[0.12em] text-[11px] bg-gray-900 text-white dark:bg-white dark:text-black hover:opacity-90 border-l border-gray-200 dark:border-hud-line transition">
          CALCULAR AHORRO
        </a>
      </div>

    </div>
  </header>
    """

def get_cookie_banner(prefix=""):
    return f"""
  <!-- Banner de Consentimiento de Cookies (Obligatorio para Google AdSense / RGPD) -->
  <div id="cookie-banner" class="fixed bottom-4 left-4 right-4 md:left-auto md:right-4 md:max-w-md bg-white dark:bg-hud-carddark border border-gray-200 dark:border-hud-line p-5 rounded-none shadow-2xl z-50 font-sans">
    <div class="flex items-start gap-3 mb-3">
      <span class="font-mono text-emerald-500 font-bold text-xs">[ RGPD ]</span>
      <p class="text-gray-600 dark:text-gray-300 text-xs leading-relaxed">
        Utilizamos cookies técnicas y publicitarias de Google AdSense de acuerdo al marco europeo de protección de datos. Consulta nuestra <a href="{prefix}legal/cookies.html" class="text-emerald-500 underline font-medium">Política de Cookies</a>.
      </p>
    </div>
    <div class="flex gap-2 justify-end font-mono text-[11px]">
      <button onclick="acceptCookies()" class="bg-emerald-500 hover:bg-emerald-600 text-black font-bold uppercase tracking-wider px-4 py-2 transition">Aceptar</button>
      <button onclick="rejectCookies()" class="bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 font-bold uppercase tracking-wider px-4 py-2 transition">Rechazar</button>
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

TOPICS = [
    {
        "slug": "calcular-sueldo-neto-espana-bruto",
        "index": "01",
        "title": "Cómo calcular tu sueldo neto a partir del bruto en España: Guía paso a paso",
        "category": "Impuestos y Nómina",
        "category_id": "impuestos",
        "read_time": "6 min",
        "status": "Actualizado",
        "description": "Desglose matemático de cotizaciones a la Seguridad Social (6,35%) y tramos del IRPF (19% a 45%). Tablas exactas y optimización con Modelo 145.",
        "content_html": """
        <p class="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-6 font-medium">Cuando negocias una oferta de trabajo o te anuncian una subida salarial, la cifra que siempre te indican es el <strong>sueldo bruto anual</strong>. Sin embargo, lo que realmente ingresa en tu cuenta bancaria a final de mes es el sueldo neto. En esta guía te explicamos cómo se calcula y qué factores determinan lo que Hacienda y la Seguridad Social retienen.</p>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-hud-line pb-2">1. ¿Qué deducciones se aplican al salario bruto?</h2>
        <p class="text-gray-700 dark:text-gray-300 mb-4">Para pasar del salario bruto al neto se aplican principalmente dos grandes conceptos de retención obligatoria:</p>
        <ul class="list-disc pl-6 space-y-2 text-gray-700 dark:text-gray-300 mb-6">
          <li><strong>Cotizaciones a la Seguridad Social:</strong> Generalmente suponen un <strong>6,35% a 6,45%</strong> del salario bruto (incluye contingencias comunes, desempleo y formación profesional).</li>
          <li><strong>Retención del IRPF:</strong> Es un pago a cuenta del Impuesto sobre la Renta de las Personas Físicas. No es fijo: varía según el importe del salario, tu situación familiar (hijos a cargo, personas dependientes) y tu comunidad autónoma.</li>
        </ul>

        <div class="bg-gray-100 dark:bg-hud-carddark border-l-2 border-emerald-500 p-5 rounded-none my-6">
          <p class="text-emerald-600 dark:text-emerald-400 font-mono text-xs uppercase tracking-wider mb-1">[ Regla matemática rápida ]</p>
          <p class="text-gray-800 dark:text-gray-200 text-sm">En salarios medios en España (entre 20.000€ y 35.000€ brutos anuales), el sueldo neto mensual suele situarse entre el <strong>75% y el 80%</strong> del salario bruto mensual si cobras en 12 pagas.</p>
        </div>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-hud-line pb-2">2. Tabla de tramos de IRPF aplicables</h2>
        <p class="text-gray-700 dark:text-gray-300 mb-4">El IRPF es un impuesto progresivo. Esto significa que no se tributa todo el sueldo al porcentaje más alto, sino que se divide en tramos:</p>
        <div class="overflow-x-auto my-6">
          <table class="min-w-full bg-white dark:bg-hud-carddark border border-gray-200 dark:border-hud-line text-sm rounded-none">
            <thead>
              <tr class="bg-gray-50 dark:bg-gray-900 text-gray-700 dark:text-gray-300 text-left font-mono text-xs">
                <th class="py-3 px-4 font-semibold border-b border-gray-200 dark:border-hud-line">Tramo de base liquidable</th>
                <th class="py-3 px-4 font-semibold border-b border-gray-200 dark:border-hud-line">Tipo estatal + autonómico orientativo</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-hud-line text-gray-700 dark:text-gray-300 font-mono text-xs">
              <tr><td class="py-2.5 px-4">De 0 € a 12.450 €</td><td class="py-2.5 px-4 font-bold text-emerald-500">19%</td></tr>
              <tr><td class="py-2.5 px-4">De 12.450 € a 20.200 €</td><td class="py-2.5 px-4 font-bold text-emerald-500">24%</td></tr>
              <tr><td class="py-2.5 px-4">De 20.200 € a 35.200 €</td><td class="py-2.5 px-4 font-bold text-emerald-500">30%</td></tr>
              <tr><td class="py-2.5 px-4">De 35.200 € a 60.000 €</td><td class="py-2.5 px-4 font-bold text-emerald-500">37%</td></tr>
              <tr><td class="py-2.5 px-4">De 60.000 € a 300.000 €</td><td class="py-2.5 px-4 font-bold text-emerald-500">45%</td></tr>
            </tbody>
          </table>
        </div>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-hud-line pb-2">3. ¿Cómo optimizar tu retención para que no te salga a pagar?</h2>
        <p class="text-gray-700 dark:text-gray-300 mb-4">Si tu empresa te aplica una retención de IRPF inferior a la que te corresponde (algo habitual al inicio de contratos temporales), recibirás más dinero cada mes, pero en la Declaración de la Renta te tocará pagar la diferencia de golpe. Puedes solicitar a Recursos Humanos rellenar el <strong>Modelo 145</strong> para ajustar tu retención al porcentaje real.</p>
        """
    },
    {
        "slug": "metodo-50-30-20-ahorro-personal",
        "index": "02",
        "title": "La regla 50/30/20: El método definitivo para organizar tu dinero y ahorrar sin sufrir",
        "category": "Ahorro y Presupuesto",
        "category_id": "ahorro",
        "read_time": "5 min",
        "status": "Clásico",
        "description": "Estructura de distribución de capital: 50% necesidades primarias, 30% estilo de vida y 20% ahorro sistemático de alta rentabilidad.",
        "content_html": """
        <p class="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-6 font-medium">Ahorrar dinero todos los meses suele parecer difícil cuando no se tiene un sistema claro. La regla 50/30/20, popularizada por la profesora de Harvard Elizabeth Warren, es uno de los métodos presupuestarios más reconocidos a nivel global por su sencillez y eficacia.</p>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-hud-line pb-2">1. ¿En qué consiste la división 50/30/20?</h2>
        <p class="text-gray-700 dark:text-gray-300 mb-4">El método consiste en dividir tus <strong>ingresos netos mensuales</strong> en tres categorías estrictas:</p>
        
        <div class="grid md:grid-cols-3 gap-4 my-6">
          <div class="bg-gray-50 dark:bg-hud-carddark border border-gray-200 dark:border-hud-line p-5">
            <span class="font-mono text-emerald-500 font-bold text-lg block mb-2">[ 50% ] Necesidades</span>
            <p class="text-gray-600 dark:text-gray-400 text-xs">Alquiler o hipoteca, suministros (luz, agua, internet), comida básica, transporte y seguros indispensables.</p>
          </div>
          <div class="bg-gray-50 dark:bg-hud-carddark border border-gray-200 dark:border-hud-line p-5">
            <span class="font-mono text-amber-500 font-bold text-lg block mb-2">[ 30% ] Deseos y Ocio</span>
            <p class="text-gray-600 dark:text-gray-400 text-xs">Cenas fuera, suscripciones a streaming, salidas con amigos, ropa no esencial, aficiones y viajes.</p>
          </div>
          <div class="bg-gray-50 dark:bg-hud-carddark border border-gray-200 dark:border-hud-line p-5">
            <span class="font-mono text-cyan-500 font-bold text-lg block mb-2">[ 20% ] Ahorro / Deudas</span>
            <p class="text-gray-600 dark:text-gray-400 text-xs">Fondo de emergencias, inversión en fondos indexados o amortización acelerada de préstamos costosos.</p>
          </div>
        </div>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-hud-line pb-2">2. Ejemplo práctico con un sueldo de 1.500 € netos</h2>
        <ul class="list-disc pl-6 space-y-2 text-gray-700 dark:text-gray-300 mb-6">
          <li><strong>750 € (50%):</strong> Destinados al pago de la vivienda, compra en el supermercado y gastos fijos.</li>
          <li><strong>450 € (30%):</strong> Presupuesto libre para disfrutar del mes sin sentir culpa.</li>
          <li><strong>300 € (20%):</strong> Ahorro automático que se transfiere el día 1 de mes a una cuenta remunerada o fondo.</li>
        </ul>

        <div class="bg-gray-100 dark:bg-hud-carddark border-l-2 border-emerald-500 p-5 my-6">
          <p class="text-emerald-500 font-mono text-xs uppercase tracking-wider mb-1">[ Automatización recomendada ]</p>
          <p class="text-gray-800 dark:text-gray-200 text-sm">Programa una transferencia periódica automática el día 1 de cada mes a tu cuenta remunerada o broker. Ahorrarás sin darte cuenta.</p>
        </div>
        """
    },
    {
        "slug": "cuentas-remuneradas-mejores-opciones",
        "index": "03",
        "title": "Cuentas remuneradas vs Depósitos a plazo fijo: Dónde rentabilizar tu dinero seguro",
        "category": "Inversión y Bancos",
        "category_id": "bancos",
        "read_time": "7 min",
        "status": "Popular",
        "description": "Comparativa de rendimientos TAE frente a la inflación. Disponibilidad de liquidez inmediata vs depósitos bloqueados con Fondo de Garantía de 100.000€.",
        "content_html": """
        <p class="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-6 font-medium">Tener el dinero ahorrado en una cuenta corriente tradicional que no te da nada es la forma más rápida de perder poder adquisitivo año tras año por culpa de la inflación. Afortunadamente, hoy en día existen herramientas bancarias con total garantía del Fondo de Garantía de Depósitos (hasta 100.000€ por titular).</p>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-hud-line pb-2">1. Diferencias clave entre Cuenta Remunerada y Depósito</h2>
        <div class="overflow-x-auto my-6">
          <table class="min-w-full bg-white dark:bg-hud-carddark border border-gray-200 dark:border-hud-line text-sm rounded-none">
            <thead>
              <tr class="bg-gray-50 dark:bg-gray-900 text-gray-700 dark:text-gray-300 text-left font-mono text-xs">
                <th class="py-3 px-4 font-semibold border-b border-gray-200 dark:border-hud-line">Característica</th>
                <th class="py-3 px-4 font-semibold border-b border-gray-200 dark:border-hud-line">Cuenta Remunerada</th>
                <th class="py-3 px-4 font-semibold border-b border-gray-200 dark:border-hud-line">Depósito a Plazo Fijo</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-hud-line text-gray-700 dark:text-gray-300 font-mono text-xs">
              <tr><td class="py-2.5 px-4 font-semibold">Disponibilidad del dinero</td><td class="py-2.5 px-4 text-emerald-500 font-bold">Inmediata (24/7)</td><td class="py-2.5 px-4 text-amber-500 font-bold">Bloqueado hasta vencimiento</td></tr>
              <tr><td class="py-2.5 px-4 font-semibold">Tipo de interés (TIN / TAE)</td><td class="py-2.5 px-4">Variable con aviso previo</td><td class="py-2.5 px-4">Garantizado y fijo durante el plazo</td></tr>
              <tr><td class="py-2.5 px-4 font-semibold">Ideal para...</td><td class="py-2.5 px-4">Fondo de emergencias y ahorro diario</td><td class="py-2.5 px-4">Dinero que no vas a usar a 1-3 años</td></tr>
            </tbody>
          </table>
        </div>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-hud-line pb-2">2. ¿Cómo tributan los intereses en la Renta?</h2>
        <p class="text-gray-700 dark:text-gray-300 mb-4">Los rendimientos generados por cuentas bancarias y depósitos tributan en la base del ahorro según los siguientes tramos:</p>
        <ul class="list-disc pl-6 space-y-2 text-gray-700 dark:text-gray-300 mb-6 font-mono text-xs">
          <li>Hasta 6.000 € de beneficios: <strong class="text-emerald-500">19%</strong></li>
          <li>Entre 6.000 € y 50.000 €: <strong class="text-emerald-500">21%</strong></li>
          <li>Entre 50.000 € y 200.000 €: <strong class="text-emerald-500">23%</strong></li>
        </ul>
        """
    },
    {
        "slug": "que-es-un-fondo-de-emergencia-guia",
        "index": "04",
        "title": "Fondo de Emergencia: Cuántos meses de gastos necesitas y dónde guardarlo",
        "category": "Ahorro y Seguridad",
        "category_id": "seguridad",
        "read_time": "5 min",
        "status": "Seguridad",
        "description": "La reserva líquida que protege tus inversiones de imprevistos. Cálculo de 3 a 6 meses de gastos fijos y ubicación óptima de custodia sin riesgo.",
        "content_html": """
        <p class="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-6 font-medium">Antes de pensar en invertir en bolsa, criptomonedas o bienes raíces, existe un paso previo fundamental que separa a las personas con tranquilidad financiera de aquellas que viven con estrés constante: el <strong>fondo de emergencia</strong>.</p>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-hud-line pb-2">1. ¿Qué es exactamente y para qué sirve?</h2>
        <p class="text-gray-700 dark:text-gray-300 mb-4">Un fondo de emergencia es una cantidad de dinero líquido reservada exclusivamente para afrontar imprevistos graves: una avería importante del coche, una urgencia médica, la pérdida de empleo o una reforma inaplazable en la vivienda. Su función no es hacerte rico, sino darte paz mental y evitar que recurras a créditos rápidos con intereses desorbitados.</p>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-hud-line pb-2">2. ¿Cuánto dinero debes tener ahorrado?</h2>
        <div class="space-y-4 my-6">
          <div class="border-l-2 border-emerald-500 pl-4 py-1">
            <h3 class="font-bold text-gray-900 dark:text-white font-mono text-sm">[ 3 a 6 meses de gastos fijos ]</h3>
            <p class="text-gray-600 dark:text-gray-400 text-xs mt-1">Recomendado para empleados asalariados con contratos indefinidos o funcionarios con ingresos previsibles.</p>
          </div>
          <div class="border-l-2 border-amber-500 pl-4 py-1">
            <h3 class="font-bold text-gray-900 dark:text-white font-mono text-sm">[ 6 a 12 meses de gastos fijos ]</h3>
            <p class="text-gray-600 dark:text-gray-400 text-xs mt-1">Imprescindible para trabajadores autónomos, freelancers o personas con ingresos variables por comisiones.</p>
          </div>
        </div>
        """
    },
    {
        "slug": "desgravar-alquiler-declaracion-renta",
        "index": "05",
        "title": "Cómo deducir el alquiler en la Declaración de la Renta: Deducción estatal y autonómica",
        "category": "Impuestos y Renta",
        "category_id": "impuestos",
        "read_time": "6 min",
        "status": "Fiscal",
        "description": "Recupera hasta 1.200€ en tu IRPF. Requisitos autonómicos (Madrid, Cataluña, Valencia, Andalucía) y cómo comprobar el depósito legal de la fianza.",
        "content_html": """
        <p class="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-6 font-medium">El alquiler es uno de los gastos más pesados para millones de familias y jóvenes. Sin embargo, muchos inquilinos desconocen que pueden recuperar cientos de euros en su Declaración de la Renta si aprovechan las deducciones fiscales disponibles tanto a nivel estatal como autonómico.</p>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-hud-line pb-2">1. Deducciones autonómicas (La gran ventaja)</h2>
        <p class="text-gray-700 dark:text-gray-300 mb-4">Casi todas las comunidades autónomas ofrecen deducciones generosas para inquilinos, especialmente para menores de 35 años o familias con rentas medias y bajas:</p>
        <ul class="list-disc pl-6 space-y-2 text-gray-700 dark:text-gray-300 mb-6 font-mono text-xs">
          <li><strong>Comunidad de Madrid:</strong> Deducción del 30% de las cantidades pagadas, hasta un máximo de 1.237,20 € anuales para menores de 35 años.</li>
          <li><strong>Cataluña:</strong> Deducción del 10% hasta 300 € (o 600 € en familias numerosas).</li>
          <li><strong>Comunidad Valenciana:</strong> Deducción entre el 20% y el 25% con límites de hasta 800 € a 1.000 €.</li>
          <li><strong>Andalucía:</strong> Deducción del 15% hasta un tope de 600 € anuales.</li>
        </ul>
        """
    },
    {
        "slug": "inversion-fondos-indexados-principiantes-guia",
        "index": "06",
        "title": "Inversión en Fondos Indexados para principiantes: Cómo empezar con 50€ al mes",
        "category": "Inversión Pasiva",
        "category_id": "bancos",
        "read_time": "8 min",
        "status": "Nuevo",
        "description": "Guía práctica sobre MSCI World y S&P 500. Rentabilidad histórica del 7-8%, comisiones mínimas del 0,15% y estrategia Dollar Cost Averaging (DCA).",
        "content_html": """
        <p class="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-6 font-medium">Invertir en bolsa no significa pasarse el día mirando gráficos ni adivinando qué acción subirá mañana. Para el 95% de las personas, el método más rentable, seguro y comprobado matemáticamente son los <strong>fondos indexados globales</strong>.</p>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-hud-line pb-2">1. ¿Qué es un fondo indexado y por qué supera a los bancos tradicionales?</h2>
        <p class="text-gray-700 dark:text-gray-300 mb-4">Un fondo indexado es una cesta que replica automáticamente un índice bursátil entero, como el <strong>MSCI World</strong> (más de 1.500 grandes empresas mundiales como Apple, Microsoft, Amazon o Nestlé) o el <strong>S&P 500</strong> (las 500 mayores empresas de EE.UU.).</p>
        <p class="text-gray-700 dark:text-gray-300 mb-4">A diferencia de los fondos de inversión que te vende tu banco habitual (que cobran hasta un 2% o 3% anual en comisiones y pierden contra el mercado), los fondos indexados tienen comisiones ínfimas (alrededor del 0,10% al 0,25%), permitiéndote quedarte con prácticamente todo el beneficio acumulado.</p>

        <div class="bg-gray-100 dark:bg-hud-carddark border-l-2 border-emerald-500 p-5 my-6">
          <p class="text-emerald-500 font-mono text-xs uppercase tracking-wider mb-1">[ Rentabilidad comprobada ]</p>
          <p class="text-gray-800 dark:text-gray-200 text-sm">En los últimos 50 años, el índice MSCI World ha generado una rentabilidad media anualizada aproximada del <strong>7% al 8%</strong> tras descontar la inflación.</p>
        </div>
        """
    }
]

def render_article_html(topic: dict) -> str:
    slug = topic["slug"]
    title = topic["title"]
    desc = topic["description"]
    cat = topic["category"]
    read_time = topic["read_time"]
    index_num = topic.get("index", "01")
    date_str = PUBLISH_DATE_ES
    iso_date = PUBLISH_DATE_ISO
    url = f"{SITE_URL}/articulos/{slug}.html"

    ad_box = f"""
    <!-- ANUNCIO GOOGLE ADSENSE (ARTCRAFT HUD STYLE) -->
    <div class="my-8 p-4 bg-gray-50 dark:bg-hud-carddark border border-gray-200 dark:border-hud-line text-center text-xs">
      <div class="flex justify-between items-center text-[10px] font-mono text-gray-400 mb-2">
        <span>[ AD // PUB-7532709201895063 ]</span>
        <span>PATROCINADO</span>
      </div>
      <div class="min-h-[100px] flex items-center justify-center bg-white dark:bg-hud-bgdark border border-gray-200 dark:border-hud-line">
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
  <title>{title} | Finanzas.Craft</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  
  <meta name="google-adsense-account" content="{ADSENSE_PUB_ID}">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB_ID}" crossorigin="anonymous"></script>

  <meta property="og:type" content="article">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">

  {get_head_assets()}
</head>
<body class="bg-[#F8F9FA] dark:bg-hud-bgdark text-gray-900 dark:text-gray-100 antialiased font-sans transition-colors duration-150">
  
  {get_hud_navbar(is_subpage=True)}

  <!-- Main Article Container -->
  <main class="max-w-4xl mx-auto px-4 sm:px-6 py-10 sm:py-14">
    <article class="bg-white dark:bg-hud-carddark border border-gray-200 dark:border-hud-line p-6 sm:p-12 shadow-sm">
      
      <!-- Meta HUD Top -->
      <div class="flex flex-wrap items-center justify-between gap-2 border-b border-gray-200 dark:border-hud-line pb-4 mb-6 font-mono text-[11px] text-gray-500 dark:text-gray-400">
        <div class="flex items-center gap-2">
          <span class="text-emerald-500 font-bold">[ {index_num} ]</span>
          <span class="uppercase tracking-wider">// {cat}</span>
        </div>
        <div class="flex items-center gap-4">
          <span>⏱️ {read_time}</span>
          <span class="text-emerald-500">● VERIFICADO</span>
        </div>
      </div>

      <!-- Headline -->
      <h1 class="text-2xl sm:text-4xl font-black text-gray-900 dark:text-white leading-tight mb-6 tracking-tight">
        {title}
      </h1>

      <p class="text-sm sm:text-base text-gray-600 dark:text-gray-300 leading-relaxed font-mono border-l-2 border-emerald-500 pl-4 py-1 mb-8 bg-gray-50 dark:bg-hud-bgdark/60">
        {desc}
      </p>

      {ad_box}

      <!-- Body Content -->
      <div class="prose dark:prose-invert max-w-none text-sm sm:text-base leading-relaxed">
        {topic["content_html"]}
      </div>

      {ad_box}

      <!-- Footer CTA Box -->
      <div class="mt-12 p-6 bg-gray-50 dark:bg-hud-bgdark border border-gray-200 dark:border-hud-line flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <div class="font-mono text-xs uppercase tracking-wider text-emerald-500 font-bold mb-1">[ CONTINUAR APRENDIENDO ]</div>
          <div class="text-sm font-semibold text-gray-900 dark:text-white">Explora el simulador de patrimonio e interés compuesto</div>
        </div>
        <a href="../index.html#simulador" class="font-mono text-[11px] font-bold uppercase tracking-wider px-5 py-2.5 bg-emerald-500 text-black hover:bg-emerald-400 transition whitespace-nowrap">
          IR AL SIMULADOR →
        </a>
      </div>
    </article>
  </main>

  <!-- Technical Footer -->
  <footer class="border-t border-gray-200 dark:border-hud-line bg-white dark:bg-hud-bgdark py-12 mt-20 font-mono text-xs text-gray-500 dark:text-gray-400">
    <div class="max-w-[1400px] mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-6">
      <div class="flex items-center gap-3">
        <span class="text-emerald-500 font-bold">[ FI // 2026 ]</span>
        <span>Finanzas.Craft — Arquitectura Financiera Inteligente</span>
      </div>
      <div class="flex gap-6">
        <a href="../legal/aviso-legal.html" class="hover:text-emerald-500 transition">Aviso Legal</a>
        <a href="../legal/privacidad.html" class="hover:text-emerald-500 transition">Privacidad</a>
        <a href="../legal/cookies.html" class="hover:text-emerald-500 transition">Cookies</a>
      </div>
    </div>
  </footer>

  {get_cookie_banner(prefix="../")}
</body>
</html>
"""

def render_home_index_html(topics: list) -> str:
    cards_html = ""
    for t in topics:
        slug = t["slug"]
        title = t["title"]
        desc = t["description"]
        cat = t["category"]
        cat_id = t.get("category_id", "all")
        read_time = t["read_time"]
        index_num = t.get("index", "01")
        status = t.get("status", "Activo")

        cards_html += f"""
        <article class="article-card group bg-white dark:bg-hud-carddark border border-gray-200 dark:border-hud-line hover:border-emerald-500 dark:hover:border-emerald-500 transition-all duration-200 p-6 sm:p-7 flex flex-col justify-between" data-category="{cat_id}">
          <div>
            <!-- Card Header HUD -->
            <div class="flex items-center justify-between font-mono text-[11px] text-gray-500 dark:text-gray-400 mb-4 border-b border-gray-100 dark:border-hud-line pb-3">
              <span class="text-emerald-600 dark:text-emerald-400 font-bold">[ {index_num} // {cat} ]</span>
              <span class="text-[10px] bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 px-2 py-0.5 uppercase tracking-wider font-semibold">
                {status}
              </span>
            </div>

            <!-- Title -->
            <h3 class="text-lg sm:text-xl font-bold text-gray-900 dark:text-white mb-3 group-hover:text-emerald-600 dark:group-hover:text-emerald-400 leading-snug transition-colors">
              <a href="articulos/{slug}.html">{title}</a>
            </h3>

            <!-- Description -->
            <p class="text-gray-600 dark:text-gray-300 text-xs sm:text-sm leading-relaxed mb-6">
              {desc}
            </p>
          </div>

          <!-- Bottom Meta & Link -->
          <div class="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-hud-line font-mono text-xs">
            <span class="text-gray-400 dark:text-gray-500 text-[11px]">⏱️ {read_time}</span>
            <a href="articulos/{slug}.html" class="inline-flex items-center gap-1.5 text-gray-900 dark:text-white font-bold group-hover:text-emerald-500 dark:group-hover:text-emerald-400 transition">
              <span>LEER GUÍA</span>
              <span class="group-hover:translate-x-1 transition-transform">→</span>
            </a>
          </div>
        </article>
        """

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Finanzas.Craft — Inteligencia y Control Financiero para tu Dinero</title>
  <meta name="description" content="Portal de ingeniería financiera personal: optimización de nómina e IRPF, cuentas remuneradas y simulador interactivo de patrimonio e interés compuesto.">
  <link rel="canonical" href="{SITE_URL}/">

  <meta property="og:type" content="website">
  <meta property="og:title" content="Finanzas.Craft — Control Financiero Inteligente">
  <meta property="og:description" content="Haz que tu dinero trabaje para ti con ingeniería de ahorro e inversión pasiva.">
  <meta property="og:url" content="{SITE_URL}/">

  <meta name="google-adsense-account" content="{ADSENSE_PUB_ID}">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB_ID}" crossorigin="anonymous"></script>

  {get_head_assets()}
</head>
<body class="bg-[#F8F9FA] dark:bg-hud-bgdark text-gray-900 dark:text-gray-100 antialiased font-sans transition-colors duration-150">
  
  {get_hud_navbar(is_subpage=False)}

  <!-- HERO SECTION ESTILO ARTCRAFT (Grid técnico, tipografía audaz, badges HUD) -->
  <section class="relative border-b border-gray-200 dark:border-hud-line overflow-hidden dark:grid-bg-dark grid-bg-light py-20 sm:py-28">
    <div class="max-w-[1400px] mx-auto px-6 relative z-10">
      
      <div class="max-w-3xl">
        <!-- HUD Pill -->
        <div class="inline-flex items-center gap-2.5 font-mono text-[11px] uppercase tracking-[0.14em] text-emerald-600 dark:text-emerald-400 bg-white dark:bg-hud-carddark border border-gray-200 dark:border-hud-line px-3.5 py-1.5 mb-6 shadow-sm">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>SISTEMA DE CONTROL PATRIMONIAL // V2026</span>
        </div>

        <h1 class="text-4xl sm:text-6xl md:text-7xl font-black text-gray-900 dark:text-white leading-[1.05] tracking-tight mb-6">
          Ingeniería financiera para <span class="text-emerald-500">multiplicar tu dinero</span>.
        </h1>

        <p class="text-base sm:text-lg text-gray-600 dark:text-gray-300 leading-relaxed mb-8 max-w-2xl font-mono text-xs sm:text-sm">
          Aprende a estructurar tu nómina, minimizar retenciones de IRPF legalmente y aplicar la matemática del interés compuesto con total precisión.
        </p>

        <!-- Botones de Acción ArtCraft -->
        <div class="flex flex-wrap gap-4 font-mono text-xs uppercase tracking-wider">
          <a href="#simulador" class="px-6 py-3.5 bg-gray-900 text-white dark:bg-white dark:text-black font-bold hover:opacity-85 transition flex items-center gap-2">
            <span>[ INICIAR SIMULADOR ]</span>
            <span>→</span>
          </a>
          <a href="#guias" class="px-6 py-3.5 bg-white dark:bg-hud-carddark text-gray-900 dark:text-white border border-gray-200 dark:border-hud-line hover:border-emerald-500 transition flex items-center gap-2">
            <span>VER CATÁLOGO DE GUÍAS</span>
          </a>
        </div>
      </div>

      <!-- Métricas HUD ArtCraft en 4 Columnas -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-0 mt-16 border border-gray-200 dark:border-hud-line bg-white dark:bg-hud-carddark">
        <div class="p-5 border-r border-b md:border-b-0 border-gray-200 dark:border-hud-line">
          <div class="font-mono text-[10px] text-gray-400 uppercase tracking-widest">[ 01 // INDEXADOS ]</div>
          <div class="text-2xl font-black text-emerald-500 font-mono mt-1">+7.8%</div>
          <div class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Media anual histórica</div>
        </div>
        <div class="p-5 border-b md:border-b-0 md:border-r border-gray-200 dark:border-hud-line">
          <div class="font-mono text-[10px] text-gray-400 uppercase tracking-widest">[ 02 // IRPF TOPE ]</div>
          <div class="text-2xl font-black text-gray-900 dark:text-white font-mono mt-1">19% - 45%</div>
          <div class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Tramos progresivos</div>
        </div>
        <div class="p-5 border-r border-gray-200 dark:border-hud-line">
          <div class="font-mono text-[10px] text-gray-400 uppercase tracking-widest">[ 03 // GARANTÍA FGD ]</div>
          <div class="text-2xl font-black text-cyan-500 font-mono mt-1">100.000 €</div>
          <div class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Por titular y entidad</div>
        </div>
        <div class="p-5">
          <div class="font-mono text-[10px] text-gray-400 uppercase tracking-widest">[ 04 // REGLA ORO ]</div>
          <div class="text-2xl font-black text-amber-500 font-mono mt-1">50 / 30 / 20</div>
          <div class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Presupuesto automático</div>
        </div>
      </div>

    </div>
  </section>

  <!-- ANUNCIO SUPERIOR ADSENSE -->
  <div class="max-w-[1400px] mx-auto px-6 my-10">
    <div class="p-4 bg-white dark:bg-hud-carddark border border-gray-200 dark:border-hud-line">
      <div class="flex justify-between items-center text-[10px] font-mono text-gray-400 mb-2">
        <span>[ AD // PUB-7532709201895063 ]</span>
        <span>PATROCINADO</span>
      </div>
      <div class="min-h-[90px] flex items-center justify-center bg-gray-50 dark:bg-hud-bgdark border border-gray-200 dark:border-hud-line">
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

  <!-- SIMULADOR ESTILO COCKPIT TÉCNICO (ARTCRAFT INTERFACE) -->
  <section id="simulador" class="max-w-[1400px] mx-auto px-6 py-10">
    <div class="bg-white dark:bg-hud-carddark border border-gray-200 dark:border-hud-line">
      
      <!-- Cockpit Header -->
      <div class="flex flex-wrap items-center justify-between gap-4 p-6 sm:p-8 border-b border-gray-200 dark:border-hud-line bg-gray-50 dark:bg-hud-bgdark/70">
        <div>
          <div class="font-mono text-xs uppercase tracking-widest text-emerald-500 font-bold mb-1">
            [ MÓDULO // INTERÉS COMPUESTO ]
          </div>
          <h2 class="text-2xl sm:text-3xl font-black text-gray-900 dark:text-white tracking-tight">
            Terminal de Proyección Financiera
          </h2>
          <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mt-1 font-mono">
            Modela el crecimiento de tu capital en base a la aportación recurrente y la tasa anual compuesta.
          </p>
        </div>
        <div class="flex items-center gap-3">
          <div class="font-mono text-right">
            <span class="text-[10px] text-gray-400 uppercase tracking-widest block">Factor Exp.</span>
            <span id="multiplier-badge" class="text-xl font-black text-emerald-500">x1.45</span>
          </div>
        </div>
      </div>

      <!-- Controls & Display Grid -->
      <div class="grid lg:grid-cols-12 gap-0 divide-y lg:divide-y-0 lg:divide-x divide-gray-200 dark:divide-hud-line">
        
        <!-- Controls Column (7 Cols) -->
        <div class="lg:col-span-7 p-6 sm:p-8 space-y-8">
          
          <!-- Slider 1 -->
          <div>
            <div class="flex justify-between items-center mb-2 font-mono text-xs">
              <span class="text-gray-500 dark:text-gray-400 uppercase tracking-wider">[ 01 ] Aportación Mensual:</span>
              <span id="val-monthly" class="text-lg font-black text-gray-900 dark:text-white">200 €</span>
            </div>
            <input type="range" id="input-monthly" min="20" max="1500" step="10" value="200"
                   class="w-full h-1.5 bg-gray-200 dark:bg-gray-800 rounded-none appearance-none cursor-pointer accent-emerald-500">
            <div class="flex justify-between font-mono text-[10px] text-gray-400 mt-2">
              <span>20 €</span>
              <span>500 €</span>
              <span>1.500 €</span>
            </div>
          </div>

          <!-- Slider 2 -->
          <div>
            <div class="flex justify-between items-center mb-2 font-mono text-xs">
              <span class="text-gray-500 dark:text-gray-400 uppercase tracking-wider">[ 02 ] Plazo de Inversión:</span>
              <span id="val-years" class="text-lg font-black text-gray-900 dark:text-white">10 años</span>
            </div>
            <input type="range" id="input-years" min="1" max="35" step="1" value="10"
                   class="w-full h-1.5 bg-gray-200 dark:bg-gray-800 rounded-none appearance-none cursor-pointer accent-emerald-500">
            <div class="flex justify-between font-mono text-[10px] text-gray-400 mt-2">
              <span>1 año</span>
              <span>15 años</span>
              <span>35 años</span>
            </div>
          </div>

          <!-- Slider 3 -->
          <div>
            <div class="flex justify-between items-center mb-2 font-mono text-xs">
              <span class="text-gray-500 dark:text-gray-400 uppercase tracking-wider">[ 03 ] Tasa de Rentabilidad (TAE):</span>
              <span id="val-rate" class="text-lg font-black text-emerald-500">7.0%</span>
            </div>
            <input type="range" id="input-rate" min="1" max="12" step="0.5" value="7"
                   class="w-full h-1.5 bg-gray-200 dark:bg-gray-800 rounded-none appearance-none cursor-pointer accent-emerald-500">
            <div class="flex justify-between font-mono text-[10px] text-gray-400 mt-2">
              <span>1.0% (Bancos)</span>
              <span>7.0% (Indexados)</span>
              <span>12.0% (Renta Variable)</span>
            </div>
          </div>

        </div>

        <!-- Displays Column (5 Cols) -->
        <div class="lg:col-span-5 p-6 sm:p-8 bg-gray-50 dark:bg-hud-bgdark/60 flex flex-col justify-between space-y-6">
          
          <div>
            <div class="font-mono text-[10px] text-gray-400 uppercase tracking-widest mb-1">[ CAPITAL FINAL PROYECTADO ]</div>
            <div id="res-total" class="text-4xl sm:text-5xl font-black text-emerald-500 font-mono tracking-tight">
              34.819 €
            </div>
            <div class="font-mono text-xs text-gray-500 mt-1">Patrimonio acumulado neto</div>
          </div>

          <div class="grid grid-cols-2 gap-4 font-mono">
            <div class="p-4 bg-white dark:bg-hud-carddark border border-gray-200 dark:border-hud-line">
              <div class="text-[10px] text-gray-400 uppercase tracking-wider">Aportado</div>
              <div id="res-invested" class="text-lg font-bold text-gray-900 dark:text-white mt-1">24.000 €</div>
              <div class="text-[10px] text-gray-400">Total puesto por ti</div>
            </div>
            <div class="p-4 bg-white dark:bg-hud-carddark border border-gray-200 dark:border-hud-line">
              <div class="text-[10px] text-emerald-500 uppercase tracking-wider">Intereses</div>
              <div id="res-interest" class="text-lg font-bold text-emerald-500 mt-1">+10.819 €</div>
              <div id="res-gain-percent" class="text-[10px] text-emerald-500 font-semibold">+45.1% extra</div>
            </div>
          </div>

          <!-- Split Bar -->
          <div>
            <div class="flex justify-between font-mono text-[11px] text-gray-400 mb-2">
              <span>Capital [ <span id="split-inv-label">69%</span> ]</span>
              <span>Interés Ganado [ <span id="split-int-label">31%</span> ]</span>
            </div>
            <div class="w-full h-2.5 bg-gray-200 dark:bg-gray-800 flex overflow-hidden">
              <div id="bar-invested" class="h-full bg-gray-900 dark:bg-white transition-all duration-200" style="width: 69%;"></div>
              <div id="bar-interest" class="h-full bg-emerald-500 transition-all duration-200" style="width: 31%;"></div>
            </div>
          </div>

        </div>

      </div>

    </div>
  </section>

  <!-- Script del Simulador ArtCraft -->
  <script>
    function updateCalculator() {{
      const monthly = parseFloat(document.getElementById('input-monthly').value);
      const years = parseFloat(document.getElementById('input-years').value);
      const rate = parseFloat(document.getElementById('input-rate').value) / 100;

      document.getElementById('val-monthly').textContent = monthly.toLocaleString('es-ES') + ' €';
      document.getElementById('val-years').textContent = years + (years === 1 ? ' año' : ' años');
      document.getElementById('val-rate').textContent = (rate * 100).toFixed(1) + '%';

      const months = years * 12;
      const r = rate / 12;
      let total = 0;
      if (r > 0) {{
        total = monthly * ((Math.pow(1 + r, months) - 1) / r);
      }} else {{
        total = monthly * months;
      }}
      const invested = monthly * months;
      const interest = total - invested;
      const multiplier = invested > 0 ? (total / invested).toFixed(2) : 1;
      const gainPercent = invested > 0 ? ((interest / invested) * 100).toFixed(1) : 0;

      document.getElementById('res-total').textContent = Math.round(total).toLocaleString('es-ES') + ' €';
      document.getElementById('res-invested').textContent = Math.round(invested).toLocaleString('es-ES') + ' €';
      document.getElementById('res-interest').textContent = '+' + Math.round(interest).toLocaleString('es-ES') + ' €';
      document.getElementById('res-gain-percent').textContent = '+' + gainPercent + '% extra';
      document.getElementById('multiplier-badge').textContent = 'x' + multiplier;

      const investedPercent = Math.min(100, Math.max(0, Math.round((invested / total) * 100)));
      const interestPercent = 100 - investedPercent;
      document.getElementById('bar-invested').style.width = investedPercent + '%';
      document.getElementById('bar-interest').style.width = interestPercent + '%';
      document.getElementById('split-inv-label').textContent = investedPercent + '%';
      document.getElementById('split-int-label').textContent = interestPercent + '%';
    }}

    document.getElementById('input-monthly').addEventListener('input', updateCalculator);
    document.getElementById('input-years').addEventListener('input', updateCalculator);
    document.getElementById('input-rate').addEventListener('input', updateCalculator);
    updateCalculator();
  </script>

  <!-- SECCIÓN DE ARTÍCULOS / GUÍAS -->
  <main id="guias" class="max-w-[1400px] mx-auto px-6 py-16">
    
    <div class="flex flex-wrap items-end justify-between gap-4 mb-8 pb-4 border-b border-gray-200 dark:border-hud-line">
      <div>
        <div class="font-mono text-xs uppercase tracking-widest text-emerald-500 font-bold mb-1">[ CATÁLOGO // GUÍAS PRÁCTICAS ]</div>
        <h2 class="text-2xl sm:text-4xl font-black text-gray-900 dark:text-white tracking-tight">Artículos y Metodología</h2>
      </div>
      <div class="font-mono text-xs text-gray-500 dark:text-gray-400">
        TOTAL DOCUMENTOS: <strong class="text-emerald-500">{len(topics)}</strong>
      </div>
    </div>

    <!-- Botones de Filtro HUD -->
    <div class="flex flex-wrap gap-2 mb-8 font-mono text-xs" id="category-filters">
      <button onclick="filterCategory('all', this)" class="cat-pill active px-4 py-2 bg-gray-900 text-white dark:bg-white dark:text-black font-bold uppercase transition">
        [ TODAS ]
      </button>
      <button onclick="filterCategory('impuestos', this)" class="cat-pill px-4 py-2 bg-white dark:bg-hud-carddark border border-gray-200 dark:border-hud-line text-gray-700 dark:text-gray-300 font-semibold uppercase hover:border-emerald-500 transition">
        IMPUESTOS & NÓMINAS
      </button>
      <button onclick="filterCategory('ahorro', this)" class="cat-pill px-4 py-2 bg-white dark:bg-hud-carddark border border-gray-200 dark:border-hud-line text-gray-700 dark:text-gray-300 font-semibold uppercase hover:border-emerald-500 transition">
        AHORRO & PRESUPUESTO
      </button>
      <button onclick="filterCategory('bancos', this)" class="cat-pill px-4 py-2 bg-white dark:bg-hud-carddark border border-gray-200 dark:border-hud-line text-gray-700 dark:text-gray-300 font-semibold uppercase hover:border-emerald-500 transition">
        CUENTAS & FONDOS
      </button>
      <button onclick="filterCategory('seguridad', this)" class="cat-pill px-4 py-2 bg-white dark:bg-hud-carddark border border-gray-200 dark:border-hud-line text-gray-700 dark:text-gray-300 font-semibold uppercase hover:border-emerald-500 transition">
        SEGURIDAD PATRIMONIAL
      </button>
    </div>

    <!-- Grid de Artículos -->
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6" id="articles-grid">
      {cards_html}
    </div>

  </main>

  <script>
    function filterCategory(category, btn) {{
      const pills = document.querySelectorAll('.cat-pill');
      pills.forEach(p => {{
        p.className = 'cat-pill px-4 py-2 bg-white dark:bg-hud-carddark border border-gray-200 dark:border-hud-line text-gray-700 dark:text-gray-300 font-semibold uppercase hover:border-emerald-500 transition';
      }});

      btn.className = 'cat-pill active px-4 py-2 bg-gray-900 text-white dark:bg-white dark:text-black font-bold uppercase transition';

      const cards = document.querySelectorAll('.article-card');
      cards.forEach(card => {{
        if (category === 'all' || card.getAttribute('data-category') === category) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}
  </script>

  <!-- Technical Footer -->
  <footer class="border-t border-gray-200 dark:border-hud-line bg-white dark:bg-hud-bgdark py-12 mt-20 font-mono text-xs text-gray-500 dark:text-gray-400">
    <div class="max-w-[1400px] mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-6">
      <div class="flex items-center gap-3">
        <span class="text-emerald-500 font-bold">[ FI // 2026 ]</span>
        <span>Finanzas.Craft — Arquitectura Financiera Inteligente</span>
      </div>
      <div class="flex gap-6">
        <a href="legal/aviso-legal.html" class="hover:text-emerald-500 transition">Aviso Legal</a>
        <a href="legal/privacidad.html" class="hover:text-emerald-500 transition">Privacidad</a>
        <a href="legal/cookies.html" class="hover:text-emerald-500 transition">Cookies</a>
      </div>
    </div>
  </footer>

  {get_cookie_banner(prefix="")}
</body>
</html>
"""

def generate_sitemap(topics: list) -> str:
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
    print("🚀 Compilando portal web estilo ArtCraft...")
    ARTICULOS_DIR.mkdir(parents=True, exist_ok=True)

    for topic in TOPICS:
        html = render_article_html(topic)
        article_file = ARTICULOS_DIR / f"{topic['slug']}.html"
        article_file.write_text(html, encoding="utf-8")
        print(f"  📄 Artículo generado: articulos/{topic['slug']}.html")

    home_html = render_home_index_html(TOPICS)
    (BASE_DIR / "index.html").write_text(home_html, encoding="utf-8")
    print("  🏠 Página de inicio generada: index.html")

    sitemap = generate_sitemap(TOPICS)
    (BASE_DIR / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print("  🗺️ Mapa del sitio generado: sitemap.xml")

    ads_txt_content = f"# Archivo ads.txt para verificación oficial de Google AdSense\ngoogle.com, {PUB_NUMERIC_ID}, DIRECT, f08c47fec0942fa0\n"
    (BASE_DIR / "ads.txt").write_text(ads_txt_content, encoding="utf-8")
    print(f"  💰 ads.txt generado: {PUB_NUMERIC_ID}")

    print(f"\n✅ Portal ArtCraft compilado con éxito. {len(TOPICS)} artículos listos.")

if __name__ == "__main__":
    build_all()
