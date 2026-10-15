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

# Fixed publish date
PUBLISH_DATE_ISO = "2026-10-14"
PUBLISH_DATE_ES = "14 de octubre de 2026"

def get_theme_script():
    return """
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
          colors: {
            darkbg: '#0B0F19',
            darkcard: '#161F30',
            darkborder: '#233047'
          }
        }
      }
    }
  </script>
    """

def get_theme_toggle_button():
    return """
    <button onclick="toggleDarkMode()" aria-label="Cambiar tema claro/oscuro" class="p-2 sm:px-3 sm:py-2 rounded-xl border border-gray-200 dark:border-slate-700 bg-gray-50 dark:bg-slate-800 text-gray-700 dark:text-amber-400 hover:bg-gray-100 dark:hover:bg-slate-700 transition flex items-center gap-2 text-xs font-semibold shadow-sm">
      <svg class="w-4 h-4 hidden dark:block text-amber-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
      <svg class="w-4 h-4 block dark:hidden text-slate-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
      <span class="hidden sm:inline text-gray-700 dark:text-slate-200">Modo</span>
    </button>
    """

def get_cookie_banner(prefix=""):
    return f"""
  <!-- Banner de Consentimiento de Cookies (Obligatorio para Google AdSense / RGPD) -->
  <div id="cookie-banner" class="fixed bottom-4 left-4 right-4 md:left-auto md:right-4 md:max-w-md bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 p-5 rounded-2xl shadow-2xl z-50 text-sm">
    <div class="flex items-start gap-3 mb-3">
      <span class="text-xl">🍪</span>
      <p class="text-gray-700 dark:text-slate-300 text-xs sm:text-sm">
        Utilizamos cookies propias y de Google AdSense para analizar el tráfico y mostrar publicidad personalizada de acuerdo al RGPD. Consulta nuestra <a href="{prefix}legal/cookies.html" class="text-emerald-600 dark:text-emerald-400 underline font-medium">Política de Cookies</a>.
      </p>
    </div>
    <div class="flex gap-2 justify-end">
      <button onclick="acceptCookies()" class="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold px-4 py-2 rounded-lg text-xs transition shadow-sm">Aceptar todas</button>
      <button onclick="rejectCookies()" class="bg-gray-100 dark:bg-slate-700 hover:bg-gray-200 dark:hover:bg-slate-600 text-gray-700 dark:text-slate-200 font-semibold px-4 py-2 rounded-lg text-xs transition">Rechazar</button>
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

# Catálogo completo de guías de alto RPM (Google AdSense)
TOPICS = [
    {
        "slug": "calcular-sueldo-neto-espana-bruto",
        "title": "Cómo calcular tu sueldo neto a partir del bruto en España: Guía paso a paso",
        "category": "Impuestos y Nómina",
        "category_id": "impuestos",
        "icon": "💶",
        "read_time": "6 min",
        "badge": "Más Leído",
        "description": "Aprende a calcular cuánto dinero recibirás en tu nómina tras retenciones de IRPF y Seguridad Social. Tablas de tramos y ejemplos prácticos.",
        "content_html": """
        <p class="text-lg text-gray-700 dark:text-slate-300 leading-relaxed mb-6 font-medium">Cuando negocias una oferta de trabajo o te anuncian una subida salarial, la cifra que siempre te indican es el <strong>sueldo bruto anual</strong>. Sin embargo, lo que realmente ingresa en tu cuenta bancaria a final de mes es el sueldo neto. En esta guía te explicamos cómo se calcula y qué factores determinan lo que Hacienda y la Seguridad Social retienen.</p>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-slate-700 pb-2">1. ¿Qué deducciones se aplican al salario bruto?</h2>
        <p class="text-gray-700 dark:text-slate-300 mb-4">Para pasar del salario bruto al neto se aplican principalmente dos grandes conceptos de retención obligatoria:</p>
        <ul class="list-disc pl-6 space-y-2 text-gray-700 dark:text-slate-300 mb-6">
          <li><strong>Cotizaciones a la Seguridad Social:</strong> Generalmente suponen un <strong>6,35% a 6,45%</strong> del salario bruto (incluye contingencias comunes, desempleo y formación profesional).</li>
          <li><strong>Retención del IRPF:</strong> Es un pago a cuenta del Impuesto sobre la Renta de las Personas Físicas. No es fijo: varía según el importe del salario, tu situación familiar (hijos a cargo, personas dependientes) y tu comunidad autónoma.</li>
        </ul>

        <div class="bg-emerald-50 dark:bg-emerald-950/40 border-l-4 border-emerald-500 p-5 rounded-r-xl my-6">
          <p class="text-emerald-900 dark:text-emerald-300 font-semibold mb-1">💡 Regla práctica rápida:</p>
          <p class="text-emerald-800 dark:text-emerald-200/90 text-sm">En salarios medios en España (entre 20.000€ y 35.000€ brutos anuales), el sueldo neto mensual suele situarse entre el <strong>75% y el 80%</strong> del salario bruto mensual si cobras en 12 pagas.</p>
        </div>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-slate-700 pb-2">2. Tabla de tramos de IRPF aplicables</h2>
        <p class="text-gray-700 dark:text-slate-300 mb-4">El IRPF es un impuesto progresivo. Esto significa que no se tributa todo el sueldo al porcentaje más alto, sino que se divide en tramos:</p>
        <div class="overflow-x-auto my-6">
          <table class="min-w-full bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm rounded-lg shadow-sm">
            <thead>
              <tr class="bg-gray-100 dark:bg-slate-700/60 text-gray-700 dark:text-slate-200 text-left">
                <th class="py-3 px-4 font-semibold border-b dark:border-slate-700">Tramo de base liquidable</th>
                <th class="py-3 px-4 font-semibold border-b dark:border-slate-700">Tipo estatal + autonómico orientativo</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-slate-700 text-gray-700 dark:text-slate-300">
              <tr><td class="py-2.5 px-4">De 0 € a 12.450 €</td><td class="py-2.5 px-4 font-medium text-emerald-600 dark:text-emerald-400">19%</td></tr>
              <tr><td class="py-2.5 px-4">De 12.450 € a 20.200 €</td><td class="py-2.5 px-4 font-medium text-emerald-600 dark:text-emerald-400">24%</td></tr>
              <tr><td class="py-2.5 px-4">De 20.200 € a 35.200 €</td><td class="py-2.5 px-4 font-medium text-emerald-600 dark:text-emerald-400">30%</td></tr>
              <tr><td class="py-2.5 px-4">De 35.200 € a 60.000 €</td><td class="py-2.5 px-4 font-medium text-emerald-600 dark:text-emerald-400">37%</td></tr>
              <tr><td class="py-2.5 px-4">De 60.000 € a 300.000 €</td><td class="py-2.5 px-4 font-medium text-emerald-600 dark:text-emerald-400">45%</td></tr>
            </tbody>
          </table>
        </div>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-slate-700 pb-2">3. ¿Cómo optimizar tu retención para que no te salga a pagar?</h2>
        <p class="text-gray-700 dark:text-slate-300 mb-4">Si tu empresa te aplica una retención de IRPF inferior a la que te corresponde (algo habitual al inicio de contratos temporales), recibirás más dinero cada mes, pero en la Declaración de la Renta te tocará pagar la diferencia de golpe. Puedes solicitar a Recursos Humanos rellenar el <strong>Modelo 145</strong> para ajustar tu retención al porcentaje real.</p>
        """
    },
    {
        "slug": "metodo-50-30-20-ahorro-personal",
        "title": "La regla 50/30/20: El método definitivo para organizar tu dinero y ahorrar sin sufrir",
        "category": "Ahorro y Presupuesto",
        "category_id": "ahorro",
        "icon": "📊",
        "read_time": "5 min",
        "badge": "Imprescindible",
        "description": "Descubre cómo repartir tus ingresos mensuales según la famosa regla 50/30/20 para ahorrar el 20% de tu sueldo todos los meses de forma automática.",
        "content_html": """
        <p class="text-lg text-gray-700 dark:text-slate-300 leading-relaxed mb-6 font-medium">Ahorrar dinero todos los meses suele parecer difícil cuando no se tiene un sistema claro. La regla 50/30/20, popularizada por la profesora de Harvard Elizabeth Warren, es uno de los métodos presupuestarios más reconocidos a nivel global por su sencillez y eficacia.</p>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-slate-700 pb-2">1. ¿En qué consiste la división 50/30/20?</h2>
        <p class="text-gray-700 dark:text-slate-300 mb-4">El método consiste en dividir tus <strong>ingresos netos mensuales</strong> en tres categorías estrictas:</p>
        
        <div class="grid md:grid-cols-3 gap-6 my-6">
          <div class="bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-900/60 p-5 rounded-2xl">
            <span class="text-blue-600 dark:text-blue-400 font-bold text-xl block mb-2">50% Necesidades</span>
            <p class="text-gray-700 dark:text-slate-300 text-sm">Alquiler o hipoteca, suministros (luz, agua, internet), comida básica, transporte y seguros indispensables.</p>
          </div>
          <div class="bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-900/60 p-5 rounded-2xl">
            <span class="text-amber-600 dark:text-amber-400 font-bold text-xl block mb-2">30% Deseos y Ocio</span>
            <p class="text-gray-700 dark:text-slate-300 text-sm">Cenas fuera, suscripciones a streaming, salidas con amigos, ropa no esencial, aficiones y viajes.</p>
          </div>
          <div class="bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-900/60 p-5 rounded-2xl">
            <span class="text-emerald-600 dark:text-emerald-400 font-bold text-xl block mb-2">20% Ahorro / Inversión</span>
            <p class="text-gray-700 dark:text-slate-300 text-sm">Fondo de emergencias, inversión en fondos indexados o amortización acelerada de préstamos costosos.</p>
          </div>
        </div>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-slate-700 pb-2">2. Ejemplo práctico con un sueldo de 1.500 € netos</h2>
        <ul class="list-disc pl-6 space-y-2 text-gray-700 dark:text-slate-300 mb-6">
          <li><strong>750 € (50%):</strong> Destinados al pago de la vivienda, compra en el supermercado y gastos fijos.</li>
          <li><strong>450 € (30%):</strong> Presupuesto libre para disfrutar del mes sin sentir culpa.</li>
          <li><strong>300 € (20%):</strong> Ahorro automático que se transfiere el día 1 de mes a una cuenta remunerada o fondo.</li>
        </ul>

        <div class="bg-gray-100 dark:bg-slate-800 p-5 rounded-xl text-gray-800 dark:text-slate-200 text-sm my-6 border border-gray-200 dark:border-slate-700">
          <strong>⚡ El truco psicológico: "Págate a ti primero"</strong><br>
          En lugar de esperar a final de mes para ahorrar lo que sobre (que casi nunca sobra nada), programa una transferencia automática de ese 20% el mismo día en que cobras tu nómina.
        </div>
        """
    },
    {
        "slug": "cuentas-remuneradas-mejores-opciones",
        "title": "Cuentas remuneradas vs Depósitos a plazo fijo: Dónde rentabilizar tu dinero seguro",
        "category": "Inversión y Bancos",
        "category_id": "bancos",
        "icon": "🏦",
        "read_time": "7 min",
        "badge": "Tendencia",
        "description": "Comparativa de las mejores opciones para no perder poder adquisitivo con la inflación. Disponibilidad total frente a tipos de interés fijos.",
        "content_html": """
        <p class="text-lg text-gray-700 dark:text-slate-300 leading-relaxed mb-6 font-medium">Tener el dinero ahorrado en una cuenta corriente tradicional que no te da nada es la forma más rápida de perder poder adquisitivo año tras año por culpa de la inflación. Afortunadamente, hoy en día existen herramientas bancarias con total garantía del Fondo de Garantía de Depósitos (hasta 100.000€ por titular).</p>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-slate-700 pb-2">1. Diferencias clave entre Cuenta Remunerada y Depósito</h2>
        <div class="overflow-x-auto my-6">
          <table class="min-w-full bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm rounded-lg shadow-sm">
            <thead>
              <tr class="bg-gray-100 dark:bg-slate-700/60 text-gray-700 dark:text-slate-200 text-left">
                <th class="py-3 px-4 font-semibold border-b dark:border-slate-700">Característica</th>
                <th class="py-3 px-4 font-semibold border-b dark:border-slate-700">Cuenta Remunerada</th>
                <th class="py-3 px-4 font-semibold border-b dark:border-slate-700">Depósito a Plazo Fijo</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-slate-700 text-gray-700 dark:text-slate-300">
              <tr><td class="py-2.5 px-4 font-semibold">Disponibilidad del dinero</td><td class="py-2.5 px-4 text-emerald-600 dark:text-emerald-400 font-medium">Inmediata (en cualquier momento)</td><td class="py-2.5 px-4 text-amber-600 dark:text-amber-400 font-medium">Bloqueado hasta vencimiento</td></tr>
              <tr><td class="py-2.5 px-4 font-semibold">Tipo de interés (TIN / TAE)</td><td class="py-2.5 px-4">Puede variar con aviso previo</td><td class="py-2.5 px-4">Garantizado y fijo durante el plazo</td></tr>
              <tr><td class="py-2.5 px-4 font-semibold">Ideal para...</td><td class="py-2.5 px-4">Fondo de emergencias y ahorro diario</td><td class="py-2.5 px-4">Dinero que no vas a usar a 1-3 años</td></tr>
            </tbody>
          </table>
        </div>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-slate-700 pb-2">2. ¿Cómo tributan los intereses en la Renta?</h2>
        <p class="text-gray-700 dark:text-slate-300 mb-4">Los rendimientos generados por cuentas bancarias y depósitos tributan en la base del ahorro según los siguientes tramos:</p>
        <ul class="list-disc pl-6 space-y-2 text-gray-700 dark:text-slate-300 mb-6">
          <li>Hasta 6.000 € de beneficios: <strong>19%</strong></li>
          <li>Entre 6.000 € y 50.000 €: <strong>21%</strong></li>
          <li>Entre 50.000 € y 200.000 €: <strong>23%</strong></li>
        </ul>
        <p class="text-gray-700 dark:text-slate-300">El propio banco suele aplicar automáticamente la retención fiscal del 19% cada vez que te abona los intereses en cuenta.</p>
        """
    },
    {
        "slug": "que-es-un-fondo-de-emergencia-guia",
        "title": "Fondo de Emergencia: Cuántos meses de gastos necesitas y dónde guardarlo",
        "category": "Ahorro y Seguridad",
        "category_id": "seguridad",
        "icon": "🛡️",
        "read_time": "5 min",
        "badge": "Básico",
        "description": "La piedra angular de cualquier economía familiar sana. Aprende a calcular el importe exacto para tu tranquilidad ante imprevistos laborales o médicos.",
        "content_html": """
        <p class="text-lg text-gray-700 dark:text-slate-300 leading-relaxed mb-6 font-medium">Antes de pensar en invertir en bolsa, criptomonedas o bienes raíces, existe un paso previo fundamental que separa a las personas con tranquilidad financiera de aquellas que viven con estrés constante: el <strong>fondo de emergencia</strong>.</p>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-slate-700 pb-2">1. ¿Qué es exactamente y para qué sirve?</h2>
        <p class="text-gray-700 dark:text-slate-300 mb-4">Un fondo de emergencia es una cantidad de dinero líquido reservada exclusivamente para afrontar imprevistos graves: una avería importante del coche, una urgencia médica, la pérdida de empleo o una reforma inaplazable en la vivienda. Su función no es hacerte rico, sino darte paz mental y evitar que recurras a créditos rápidos o tarjetas revolving con intereses desorbitados del 20%.</p>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-slate-700 pb-2">2. ¿Cuánto dinero debes tener ahorrado?</h2>
        <p class="text-gray-700 dark:text-slate-300 mb-4">La regla general depende de tu estabilidad laboral:</p>
        <div class="space-y-4 my-6">
          <div class="border-l-4 border-blue-500 pl-4 py-1">
            <h3 class="font-bold text-gray-900 dark:text-white">3 a 6 meses de gastos fijos:</h3>
            <p class="text-gray-600 dark:text-slate-400 text-sm">Recomendado para empleados asalariados con contratos indefinidos o funcionarios con ingresos muy previsibles.</p>
          </div>
          <div class="border-l-4 border-amber-500 pl-4 py-1">
            <h3 class="font-bold text-gray-900 dark:text-white">6 a 12 meses de gastos fijos:</h3>
            <p class="text-gray-600 dark:text-slate-400 text-sm">Imprescindible para trabajadores autónomos, freelancers o personas con ingresos variables o comisiones.</p>
          </div>
        </div>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-slate-700 pb-2">3. ¿Dónde guardarlo para que no pierda valor?</h2>
        <p class="text-gray-700 dark:text-slate-300 mb-4">El fondo de emergencia debe cumplir dos condiciones obligatorias: <strong>seguridad máxima (riesgo 0)</strong> y <strong>liquidez inmediata (poder sacarlo en 24h)</strong>. Por tanto, nunca debe invertirse en acciones volátiles. El mejor lugar es una <strong>cuenta remunerada de alta rentabilidad</strong> que genere intereses cada mes mientras el dinero espera.</p>
        """
    },
    {
        "slug": "desgravar-alquiler-declaracion-renta",
        "title": "Cómo deducir el alquiler en la Declaración de la Renta: Deducción estatal y autonómica",
        "category": "Impuestos y Renta",
        "category_id": "impuestos",
        "icon": "🏠",
        "read_time": "6 min",
        "badge": "Ahorro Fiscal",
        "description": "Conoce los requisitos y casillas exactas para ahorrarte hasta 1.000€ en tu IRPF si vives de alquiler. Diferencias por comunidades autónomas.",
        "content_html": """
        <p class="text-lg text-gray-700 dark:text-slate-300 leading-relaxed mb-6 font-medium">El alquiler es uno de los gastos más pesados para millones de familias y jóvenes. Sin embargo, muchos inquilinos desconocen que pueden recuperar cientos de euros en su Declaración de la Renta si aprovechan las deducciones fiscales disponibles tanto a nivel estatal como autonómico.</p>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-slate-700 pb-2">1. Deducción estatal por alquiler</h2>
        <p class="text-gray-700 dark:text-slate-300 mb-4">La deducción estatal solo es aplicable si tu contrato de alquiler es anterior al <strong>1 de enero de 2015</strong> y tu base imponible es inferior a 24.107,20 € anuales. Si tu contrato es más reciente, la ayuda estatal ya no aplica, pero es en las deducciones autonómicas donde está la verdadera oportunidad.</p>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-slate-700 pb-2">2. Deducciones autonómicas (La gran ventaja)</h2>
        <p class="text-gray-700 dark:text-slate-300 mb-4">Casi todas las comunidades autónomas ofrecen deducciones generosas para inquilinos, especialmente para menores de 35 años o familias con rentas medias y bajas:</p>
        <ul class="list-disc pl-6 space-y-2 text-gray-700 dark:text-slate-300 mb-6">
          <li><strong>Comunidad de Madrid:</strong> Deducción del 30% de las cantidades pagadas, hasta un máximo de 1.237,20 € anuales para menores de 35 años.</li>
          <li><strong>Cataluña:</strong> Deducción del 10% hasta 300 € (o 600 € en familias numerosas).</li>
          <li><strong>Comunidad Valenciana:</strong> Deducción entre el 20% y el 25% con límites de hasta 800 € a 1.000 €.</li>
          <li><strong>Andalucía:</strong> Deducción del 15% hasta un tope de 600 € anuales.</li>
        </ul>

        <div class="bg-amber-50 dark:bg-amber-950/40 border-l-4 border-amber-500 p-5 rounded-r-xl my-6">
          <p class="text-amber-900 dark:text-amber-300 font-semibold mb-1">⚠️ Requisito indispensable para que Hacienda no te multe:</p>
          <p class="text-amber-800 dark:text-amber-200/90 text-sm">En la mayoría de comunidades autónomas es obligatorio que el propietario haya depositado la fianza legal del alquiler en el organismo autonómico correspondiente (como el IVIMA en Madrid o el INCASÒL en Cataluña).</p>
        </div>
        """
    },
    {
        "slug": "inversion-fondos-indexados-principiantes-guia",
        "title": "Inversión en Fondos Indexados para principiantes: Cómo empezar con 50€ al mes",
        "category": "Inversión Pasiva",
        "category_id": "bancos",
        "icon": "📈",
        "read_time": "8 min",
        "badge": "Nueva",
        "description": "Guía definitiva sobre MSCI World y S&P 500. Rentabilidad histórica del 7-8%, bajas comisiones y la magia del interés compuesto a largo plazo.",
        "content_html": """
        <p class="text-lg text-gray-700 dark:text-slate-300 leading-relaxed mb-6 font-medium">Invertir en bolsa no significa pasarse el día mirando gráficos ni adivinando qué acción subirá mañana. Para el 95% de las personas, el método más rentable, seguro y comprobado matemáticamente son los <strong>fondos indexados globales</strong>.</p>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-slate-700 pb-2">1. ¿Qué es un fondo indexado y por qué supera a los bancos tradicionales?</h2>
        <p class="text-gray-700 dark:text-slate-300 mb-4">Un fondo indexado es una cesta que replica automáticamente un índice bursátil entero, como el <strong>MSCI World</strong> (más de 1.500 grandes empresas mundiales como Apple, Microsoft, Amazon o Nestlé) o el <strong>S&P 500</strong> (las 500 mayores empresas de EE.UU.).</p>
        <p class="text-gray-700 dark:text-slate-300 mb-4">A diferencia de los fondos de inversión que te vende tu banco habitual (que cobran hasta un 2% o 3% anual en comisiones y pierden contra el mercado), los fondos indexados tienen comisiones ínfimas (alrededor del 0,10% al 0,25%), permitiéndote quedarte con prácticamente todo el beneficio acumulado.</p>

        <div class="bg-emerald-50 dark:bg-emerald-950/40 border-l-4 border-emerald-500 p-5 rounded-r-xl my-6">
          <p class="text-emerald-900 dark:text-emerald-300 font-semibold mb-1">📊 Rentabilidad histórica comprobada:</p>
          <p class="text-emerald-800 dark:text-emerald-200/90 text-sm">En los últimos 50 años, el índice MSCI World ha generado una rentabilidad media anualizada aproximada del <strong>7% al 8%</strong> tras descontar la inflación.</p>
        </div>

        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4 border-b border-gray-200 dark:border-slate-700 pb-2">2. La estrategia Dollar Cost Averaging (DCA)</h2>
        <p class="text-gray-700 dark:text-slate-300 mb-4">No intentes averiguar cuándo el mercado está "barato" o "caro". La técnica ganadora consiste en automatizar una aportación fija (por ejemplo, 50€ o 150€) el día 1 de cada mes. Si el mercado baja, compras más participaciones a precio de ganga; si sube, tu cartera gana valor.</p>
        """
    }
]

def render_article_html(topic: dict) -> str:
    """Generates a complete, standalone, high-PageSpeed SEO article page with dark mode support."""
    slug = topic["slug"]
    title = topic["title"]
    desc = topic["description"]
    cat = topic["category"]
    read_time = topic["read_time"]
    icon = topic.get("icon", "📄")
    date_str = PUBLISH_DATE_ES
    iso_date = PUBLISH_DATE_ISO
    url = f"{SITE_URL}/articulos/{slug}.html"

    ad_box = f"""
    <!-- ESPACIO DE ANUNCIO GOOGLE ADSENSE -->
    <div class="my-8 p-4 bg-gray-50 dark:bg-slate-800/80 border border-dashed border-gray-300 dark:border-slate-700 rounded-2xl text-center text-xs text-gray-400">
      <span class="block uppercase tracking-wider mb-2 font-semibold text-gray-400 dark:text-slate-400">Publicidad</span>
      <div class="min-h-[100px] flex items-center justify-center bg-white dark:bg-slate-900 rounded-xl border border-gray-200 dark:border-slate-800">
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

  {get_theme_script()}
</head>
<body class="bg-gray-50 dark:bg-slate-900 text-gray-800 dark:text-slate-100 antialiased font-sans transition-colors duration-200">
  <!-- Navegación Superior -->
  <header class="bg-white dark:bg-slate-900/90 border-b border-gray-200 dark:border-slate-800 sticky top-0 z-50 backdrop-blur-md shadow-sm">
    <div class="max-w-4xl mx-auto px-4 py-3.5 flex justify-between items-center">
      <a href="../index.html" class="text-lg sm:text-xl font-extrabold text-emerald-600 dark:text-emerald-400 flex items-center gap-2">
        <span>📈 Finanzas Inteligentes</span>
      </a>
      <div class="flex items-center gap-3">
        {get_theme_toggle_button()}
        <a href="../index.html" class="text-xs sm:text-sm font-semibold text-gray-600 dark:text-slate-300 hover:text-emerald-600 dark:hover:text-emerald-400 transition">
          ← Volver al inicio
        </a>
      </div>
    </div>
  </header>

  <!-- Contenido Principal -->
  <main class="max-w-3xl mx-auto px-4 py-10">
    <article class="bg-white dark:bg-slate-800/90 p-6 sm:p-10 rounded-3xl shadow-sm border border-gray-100 dark:border-slate-700/80">
      <!-- Breadcrumbs -->
      <nav class="text-xs text-gray-500 dark:text-slate-400 mb-4 flex items-center gap-2">
        <a href="../index.html" class="hover:underline">Inicio</a> &gt;
        <span class="text-emerald-600 dark:text-emerald-400 font-medium">{cat}</span>
      </nav>

      <!-- Encabezado del Artículo -->
      <div class="flex items-center gap-3 mb-3">
        <span class="text-3xl">{icon}</span>
        <span class="bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800 px-3 py-1 rounded-full text-xs font-bold">{cat}</span>
      </div>

      <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 dark:text-white leading-tight mb-4">
        {title}
      </h1>

      <div class="flex flex-wrap items-center gap-4 text-xs text-gray-500 dark:text-slate-400 mb-8 border-b border-gray-100 dark:border-slate-700 pb-4">
        <span class="flex items-center gap-1">⏱️ Lectura: {read_time}</span>
        <span class="flex items-center gap-1">📅 Actualizado: {date_str}</span>
        <span class="text-emerald-600 dark:text-emerald-400 font-medium">✓ Verificado</span>
      </div>

      <!-- Anuncio Superior -->
      {ad_box}

      <!-- Cuerpo del Artículo -->
      <div class="prose dark:prose-invert max-w-none text-base">
        {topic["content_html"]}
      </div>

      <!-- Anuncio Inferior -->
      {ad_box}

      <!-- Caja de Conclusión / Compartir -->
      <div class="mt-10 p-6 bg-emerald-50 dark:bg-emerald-950/40 rounded-2xl border border-emerald-200 dark:border-emerald-800/60">
        <h3 class="font-bold text-emerald-900 dark:text-emerald-300 text-lg mb-2">💡 ¿Te ha resultado útil esta guía?</h3>
        <p class="text-emerald-800 dark:text-emerald-200/90 text-sm mb-4">Guarda esta página en tus marcadores y compártela con quien quiera mejorar sus finanzas y pagar menos comisiones.</p>
        <a href="../index.html" class="inline-block bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm px-5 py-2.5 rounded-xl transition shadow-sm">Explorar más guías de finanzas</a>
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
    """Generates the main portal index.html with Dark Mode, Financial Simulator, Ticker, Category Filter and Modern Visual Cards."""
    cards_html = ""
    for t in topics:
        slug = t["slug"]
        title = t["title"]
        desc = t["description"]
        cat = t["category"]
        cat_id = t.get("category_id", "all")
        read_time = t["read_time"]
        icon = t.get("icon", "📄")
        badge = t.get("badge", "Destacado")
        
        cards_html += f"""
        <article class="article-card group bg-white dark:bg-slate-800/90 rounded-2xl shadow-sm hover:shadow-xl border border-gray-100 dark:border-slate-700/80 hover:border-emerald-500/50 dark:hover:border-emerald-400/50 transition-all duration-300 p-6 flex flex-col justify-between relative overflow-hidden" data-category="{cat_id}">
          <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-emerald-500 to-teal-400 opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div>
            <div class="flex items-center justify-between text-xs mb-3">
              <span class="bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/60 font-bold px-2.5 py-1 rounded-full flex items-center gap-1.5">
                <span>{icon}</span> {cat}
              </span>
              <span class="bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 px-2 py-0.5 rounded text-[11px] font-semibold">{badge}</span>
            </div>
            <h3 class="text-lg sm:text-xl font-bold text-gray-900 dark:text-white mb-3 group-hover:text-emerald-600 dark:group-hover:text-emerald-400 leading-snug transition-colors">
              <a href="articulos/{slug}.html">{title}</a>
            </h3>
            <p class="text-gray-600 dark:text-slate-300 text-sm leading-relaxed mb-4 line-clamp-3">
              {desc}
            </p>
          </div>
          <div class="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-slate-700/60 mt-2">
            <span class="text-xs text-gray-500 dark:text-slate-400 flex items-center gap-1">⏱️ {read_time}</span>
            <a href="articulos/{slug}.html" class="text-emerald-600 dark:text-emerald-400 font-bold text-sm hover:underline flex items-center gap-1">
              Leer guía <span class="group-hover:translate-x-1 transition-transform">→</span>
            </a>
          </div>
        </article>
        """

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Finanzas Inteligentes | Guías de Ahorro, Impuestos e Inversión</title>
  <meta name="description" content="Portal educativo de finanzas personales, optimización de impuestos, cuentas remuneradas y simulador interactivo para ahorrar e invertir con inteligencia.">
  <link rel="canonical" href="{SITE_URL}/">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="Finanzas Inteligentes | Guías de Ahorro e Inversión">
  <meta property="og:description" content="Aprende a gestionar tu dinero, calcular tu nómina y rentabilizar tus ahorros sin complicaciones.">
  <meta property="og:url" content="{SITE_URL}/">

  <!-- Verificación oficial para Google AdSense -->
  <meta name="google-adsense-account" content="{ADSENSE_PUB_ID}">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB_ID}" crossorigin="anonymous"></script>

  {get_theme_script()}
</head>
<body class="bg-gray-50 dark:bg-slate-900 text-gray-800 dark:text-slate-100 antialiased font-sans transition-colors duration-200">
  
  <!-- Ticker Financiero en Vivo -->
  <div class="bg-slate-900 text-slate-200 text-xs border-b border-slate-800 py-2.5 px-4 overflow-x-auto whitespace-nowrap">
    <div class="max-w-6xl mx-auto flex items-center justify-between gap-6">
      <div class="flex items-center gap-5 text-xs">
        <span class="flex items-center gap-1.5 font-bold text-emerald-400"><span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> Indicadores 2026:</span>
        <span class="flex items-center gap-1">🏦 <span class="text-slate-400">Tipo BCE:</span> <strong class="text-emerald-400">3.25%</strong></span>
        <span class="flex items-center gap-1">📉 <span class="text-slate-400">Euríbor 12M:</span> <strong class="text-emerald-400">2.78%</strong></span>
        <span class="flex items-center gap-1">💰 <span class="text-slate-400">Cuentas Remuneradas:</span> <strong class="text-emerald-400">hasta 3.70% TAE</strong></span>
        <span class="flex items-center gap-1">💶 <span class="text-slate-400">SMI España:</span> <strong class="text-white">1.184 €</strong></span>
      </div>
      <span class="hidden md:inline-block text-[11px] text-slate-400 bg-slate-800 px-2.5 py-0.5 rounded-full border border-slate-700">Actualizado diario</span>
    </div>
  </div>

  <!-- Barra de Navegación Principal -->
  <header class="bg-white/90 dark:bg-slate-900/90 border-b border-gray-200 dark:border-slate-800 sticky top-0 z-40 backdrop-blur-md shadow-sm">
    <div class="max-w-6xl mx-auto px-4 py-3.5 flex justify-between items-center">
      <a href="index.html" class="text-xl sm:text-2xl font-black text-emerald-600 dark:text-emerald-400 flex items-center gap-2">
        <span class="text-2xl">📈</span>
        <span>Finanzas Inteligentes</span>
      </a>
      
      <div class="flex items-center gap-3">
        <a href="#simulador" class="hidden sm:inline-flex items-center gap-1 text-xs font-bold text-emerald-700 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 px-3 py-2 rounded-xl hover:bg-emerald-100 transition">
          ⚡ Calculadora
        </a>
        {get_theme_toggle_button()}
      </div>
    </div>
  </header>

  <!-- Hero Section Mejorada con Gráficos y Métricas -->
  <section class="relative bg-gradient-to-b from-white via-slate-50 to-gray-50 dark:from-slate-900 dark:via-slate-900 dark:to-slate-900/80 py-16 sm:py-20 border-b border-gray-200 dark:border-slate-800 overflow-hidden">
    <!-- Luces y degradados de fondo -->
    <div class="absolute -top-32 -left-32 w-96 h-96 bg-emerald-500/10 dark:bg-emerald-500/15 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute top-10 right-0 w-80 h-80 bg-blue-500/10 dark:bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>

    <div class="max-w-4xl mx-auto text-center px-4 relative z-10">
      <div class="inline-flex items-center gap-2 bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300 text-xs font-extrabold px-3.5 py-1.5 rounded-full uppercase tracking-wider mb-6 shadow-sm">
        <span class="w-2 h-2 rounded-full bg-emerald-500"></span> Educación Financiera 100% Práctica
      </div>
      
      <h1 class="text-3xl sm:text-5xl md:text-6xl font-black text-gray-900 dark:text-white leading-tight mb-6 tracking-tight">
        Haz que tu dinero trabaje para ti, <span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-teal-400">no al revés</span>.
      </h1>
      
      <p class="text-gray-600 dark:text-slate-300 text-base sm:text-lg mb-8 leading-relaxed max-w-2xl mx-auto">
        Guías sin rodeos para optimizar tu nómina, pagar menos IRPF legalmente y hacer crecer tus ahorros con el poder del interés compuesto.
      </p>

      <!-- Badges de estadísticas rápidas -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4 max-w-3xl mx-auto text-left">
        <div class="p-4 rounded-2xl bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 shadow-sm">
          <div class="text-xs text-gray-500 dark:text-slate-400 font-medium">Rentabilidad Media</div>
          <div class="text-xl font-black text-emerald-600 dark:text-emerald-400 mt-1">7% - 8%</div>
          <div class="text-[11px] text-gray-400 dark:text-slate-500">Histórica indexados</div>
        </div>
        <div class="p-4 rounded-2xl bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 shadow-sm">
          <div class="text-xs text-gray-500 dark:text-slate-400 font-medium">Ahorro en IRPF</div>
          <div class="text-xl font-black text-emerald-600 dark:text-emerald-400 mt-1">Hasta 1.000€</div>
          <div class="text-[11px] text-gray-400 dark:text-slate-500">Deducción alquiler</div>
        </div>
        <div class="p-4 rounded-2xl bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 shadow-sm">
          <div class="text-xs text-gray-500 dark:text-slate-400 font-medium">Garantía Bancaria</div>
          <div class="text-xl font-black text-emerald-600 dark:text-emerald-400 mt-1">100.000 €</div>
          <div class="text-[11px] text-gray-400 dark:text-slate-500">FGD por titular</div>
        </div>
        <div class="p-4 rounded-2xl bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 shadow-sm">
          <div class="text-xs text-gray-500 dark:text-slate-400 font-medium">Regla de Oro</div>
          <div class="text-xl font-black text-emerald-600 dark:text-emerald-400 mt-1">50 / 30 / 20</div>
          <div class="text-[11px] text-gray-400 dark:text-slate-500">Ahorro sistemático</div>
        </div>
      </div>
    </div>
  </section>

  <!-- Espacio de Anuncio Principal AdSense -->
  <div class="max-w-5xl mx-auto px-4 my-8">
    <div class="p-4 bg-white dark:bg-slate-800/80 border border-dashed border-gray-300 dark:border-slate-700 rounded-2xl text-center text-xs text-gray-400">
      <span class="block uppercase tracking-wider mb-2 font-semibold text-gray-400 dark:text-slate-400">Publicidad</span>
      <div class="min-h-[90px] flex items-center justify-center bg-gray-50 dark:bg-slate-900 rounded-xl">
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

  <!-- HERRAMIENTA INTERACTIVA: SIMULADOR DE INTERÉS COMPUESTO -->
  <section class="max-w-6xl mx-auto px-4 py-4">
    <div id="simulador" class="p-6 sm:p-10 rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900 to-emerald-950 text-white shadow-2xl border border-emerald-500/30 relative overflow-hidden">
      <!-- Glows -->
      <div class="absolute -right-20 -top-20 w-80 h-80 bg-emerald-500/15 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute -left-20 -bottom-20 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <div class="relative z-10">
        <div class="flex flex-wrap items-center justify-between gap-4 mb-8">
          <div>
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
              ⚡ Simulador Interactivo
            </span>
            <h2 class="text-2xl sm:text-3xl font-black mt-2 text-white">Calculadora de Crecimiento Financiero</h2>
            <p class="text-slate-300 text-sm mt-1">Descubre cuánto dinero puedes acumular mes a mes gracias a la magia del interés compuesto.</p>
          </div>
          <div class="bg-slate-800/90 border border-slate-700 px-4 py-2 rounded-2xl text-right shadow-inner">
            <span class="text-xs text-slate-400 block font-medium">Multiplicador de capital</span>
            <span id="multiplier-badge" class="text-lg font-black text-emerald-400 font-mono">x1.45</span>
          </div>
        </div>

        <div class="grid lg:grid-cols-2 gap-8 items-center">
          <!-- Controles / Sliders -->
          <div class="space-y-6 bg-slate-800/80 p-6 sm:p-7 rounded-2xl border border-slate-700/80 backdrop-blur-md shadow-lg">
            <!-- Slider 1: Aportación Mensual -->
            <div>
              <div class="flex justify-between items-center text-sm font-semibold mb-2">
                <span class="text-slate-200 flex items-center gap-2">💰 Aportación mensual:</span>
                <span id="val-monthly" class="text-emerald-400 font-black text-xl font-mono">200 €</span>
              </div>
              <input type="range" id="input-monthly" min="20" max="1500" step="10" value="200"
                     class="w-full h-2.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-emerald-400">
              <div class="flex justify-between text-[11px] text-slate-400 mt-1.5 font-medium">
                <span>20 €</span>
                <span>500 €</span>
                <span>1.500 €</span>
              </div>
            </div>

            <!-- Slider 2: Años de inversión -->
            <div>
              <div class="flex justify-between items-center text-sm font-semibold mb-2">
                <span class="text-slate-200 flex items-center gap-2">⏳ Plazo de tiempo:</span>
                <span id="val-years" class="text-emerald-400 font-black text-xl font-mono">10 años</span>
              </div>
              <input type="range" id="input-years" min="1" max="30" step="1" value="10"
                     class="w-full h-2.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-emerald-400">
              <div class="flex justify-between text-[11px] text-slate-400 mt-1.5 font-medium">
                <span>1 año</span>
                <span>15 años</span>
                <span>30 años</span>
              </div>
            </div>

            <!-- Slider 3: Rentabilidad esperada -->
            <div>
              <div class="flex justify-between items-center text-sm font-semibold mb-2">
                <span class="text-slate-200 flex items-center gap-2">📈 Rentabilidad anual (TAE):</span>
                <span id="val-rate" class="text-emerald-400 font-black text-xl font-mono">7%</span>
              </div>
              <input type="range" id="input-rate" min="1" max="12" step="0.5" value="7"
                     class="w-full h-2.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-emerald-400">
              <div class="flex justify-between text-[11px] text-slate-400 mt-1.5 font-medium">
                <span>1% (Bancos)</span>
                <span>7% (Indexados)</span>
                <span>12% (Optimista)</span>
              </div>
            </div>
          </div>

          <!-- Resultados Visuales -->
          <div class="space-y-4">
            <div class="p-6 sm:p-7 rounded-2xl bg-gradient-to-br from-emerald-600/30 via-emerald-500/10 to-transparent border border-emerald-500/40 text-center shadow-lg">
              <span class="text-xs uppercase tracking-wider text-slate-300 font-bold block mb-1">Total Estimado en tu Cuenta</span>
              <div id="res-total" class="text-4xl sm:text-5xl font-black text-emerald-400 font-mono tracking-tight my-1">34.819 €</div>
              <span class="text-xs text-slate-300">Capital listo para tu jubilación o metas</span>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div class="p-4 rounded-xl bg-slate-800/90 border border-slate-700">
                <span class="text-xs text-slate-400 block mb-1">Ahorrado de tu sueldo</span>
                <div id="res-invested" class="text-lg sm:text-xl font-bold text-slate-200 font-mono">24.000 €</div>
                <span class="text-[11px] text-slate-400">Total aportado</span>
              </div>
              <div class="p-4 rounded-xl bg-slate-800/90 border border-emerald-500/40">
                <span class="text-xs text-emerald-400 block mb-1">🚀 Intereses generados</span>
                <div id="res-interest" class="text-lg sm:text-xl font-bold text-emerald-400 font-mono">+10.819 €</div>
                <span id="res-gain-percent" class="text-[11px] text-emerald-400 font-semibold">+45.1% extra</span>
              </div>
            </div>

            <!-- Barra gráfica comparativa de capital vs intereses -->
            <div class="bg-slate-800/90 p-4 rounded-xl border border-slate-700">
              <div class="flex justify-between text-xs text-slate-300 mb-2 font-medium">
                <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-blue-500 inline-block"></span> Tu esfuerzo (capital)</span>
                <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-400 inline-block"></span> Ganancia compuesta</span>
              </div>
              <div class="w-full h-3.5 bg-slate-700 rounded-full overflow-hidden flex shadow-inner">
                <div id="bar-invested" class="h-full bg-blue-500 transition-all duration-300" style="width: 69%;"></div>
                <div id="bar-interest" class="h-full bg-emerald-400 transition-all duration-300" style="width: 31%;"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Script del Simulador Financiero -->
  <script>
    function updateCalculator() {{
      const monthly = parseFloat(document.getElementById('input-monthly').value);
      const years = parseFloat(document.getElementById('input-years').value);
      const rate = parseFloat(document.getElementById('input-rate').value) / 100;

      document.getElementById('val-monthly').textContent = monthly.toLocaleString('es-ES') + ' €';
      document.getElementById('val-years').textContent = years + (years === 1 ? ' año' : ' años');
      document.getElementById('val-rate').textContent = (rate * 100).toFixed(1) + '% TAE';

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
      document.getElementById('res-gain-percent').textContent = '+' + gainPercent + '% de beneficio';
      document.getElementById('multiplier-badge').textContent = 'x' + multiplier;

      const investedPercent = Math.min(100, Math.max(0, (invested / total) * 100));
      const interestPercent = 100 - investedPercent;
      document.getElementById('bar-invested').style.width = investedPercent + '%';
      document.getElementById('bar-interest').style.width = interestPercent + '%';
    }}

    document.getElementById('input-monthly').addEventListener('input', updateCalculator);
    document.getElementById('input-years').addEventListener('input', updateCalculator);
    document.getElementById('input-rate').addEventListener('input', updateCalculator);
    updateCalculator();
  </script>

  <!-- Cuadrícula de Artículos con Filtro por Categorías -->
  <main class="max-w-6xl mx-auto px-4 py-12">
    <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
      <div>
        <h2 class="text-2xl sm:text-3xl font-black text-gray-900 dark:text-white">Artículos y Guías Prácticas</h2>
        <p class="text-sm text-gray-500 dark:text-slate-400 mt-1">Explora nuestras guías paso a paso escritas para entender tus finanzas sin rodeos.</p>
      </div>
      <span class="text-xs bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 font-bold px-3 py-1.5 rounded-full border border-emerald-300 dark:border-emerald-800">
        {len(topics)} guías disponibles
      </span>
    </div>

    <!-- Botones de filtro de categorías -->
    <div class="flex flex-wrap gap-2 mb-8 items-center" id="category-filters">
      <button onclick="filterCategory('all', this)" class="cat-pill active px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition bg-emerald-600 text-white shadow-sm flex items-center gap-1.5">
        ⚡ Todas
      </button>
      <button onclick="filterCategory('impuestos', this)" class="cat-pill px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-700 dark:text-slate-300 hover:border-emerald-500 flex items-center gap-1.5">
        💶 Impuestos & Nóminas
      </button>
      <button onclick="filterCategory('ahorro', this)" class="cat-pill px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-700 dark:text-slate-300 hover:border-emerald-500 flex items-center gap-1.5">
        📊 Ahorro & Presupuesto
      </button>
      <button onclick="filterCategory('bancos', this)" class="cat-pill px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-700 dark:text-slate-300 hover:border-emerald-500 flex items-center gap-1.5">
        🏦 Cuentas & Inversión
      </button>
      <button onclick="filterCategory('seguridad', this)" class="cat-pill px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-700 dark:text-slate-300 hover:border-emerald-500 flex items-center gap-1.5">
        🛡️ Seguridad & Fondos
      </button>
    </div>

    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6" id="articles-grid">
      {cards_html}
    </div>
  </main>

  <script>
    function filterCategory(category, btn) {{
      const pills = document.querySelectorAll('.cat-pill');
      pills.forEach(p => {{
        p.classList.remove('bg-emerald-600', 'text-white', 'shadow-sm');
        p.classList.add('bg-white', 'dark:bg-slate-800', 'text-gray-700', 'dark:text-slate-300', 'border', 'border-gray-200', 'dark:border-slate-700');
      }});

      btn.classList.remove('bg-white', 'dark:bg-slate-800', 'text-gray-700', 'dark:text-slate-300', 'border-gray-200', 'dark:border-slate-700');
      btn.classList.add('bg-emerald-600', 'text-white', 'shadow-sm');

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

    print(f"\n✅ Portal compilado con éxito. {len(TOPICS)} artículos listos para Google AdSense con Modo Oscuro y Simulador.")

if __name__ == "__main__":
    build_all()
