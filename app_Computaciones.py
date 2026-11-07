# -*- coding: utf-8 -*-
"""
Herramientas numéricas — app Streamlit
  1) Conversor universal de sistemas numéricos
  2) Calculadora multi-base (binario, octal, decimal, hexadecimal)
  3) Calculadora de MCD y mcm

Ejecutar con:  streamlit run app.py
"""
import re
from fractions import Fraction
from functools import reduce
from html import escape
from math import gcd

import streamlit as st

st.set_page_config(page_title="Herramientas numéricas", page_icon="🧮", layout="centered")

# ===========================================================================
# ESTILOS
# ===========================================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; }
#MainMenu, footer { visibility: hidden; }
.block-container { max-width: 880px; padding-top: 5rem !important; padding-bottom: 3rem; }

/* Cabecera */
.hero {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 55%, #DB2777 100%);
    border-radius: 24px; padding: 2.2rem 2rem; margin-bottom: 1.6rem;
    box-shadow: 0 18px 40px -18px rgba(79,70,229,.55);
}
.hero h1 { color: #fff !important; font-size: 2.1rem; font-weight: 800; margin: 0; letter-spacing: -.02em; padding: 0; }
.hero p  { color: rgba(255,255,255,.88); margin: .45rem 0 0 0; font-size: 1.02rem; }

/* Pestañas */
.stTabs [data-baseweb="tab-list"] {
    gap: .35rem; padding: .3rem; border-radius: 16px; border: none !important;
    background: rgba(127,127,127,.13);
}
.stTabs button[role="tab"] {
    flex: 1; justify-content: center; height: 2.7rem; border-radius: 12px; padding: 0 1.1rem;
    background: transparent; border: none; transition: all .18s ease; opacity: .75;
}
.stTabs button[role="tab"] p { font-weight: 600; font-size: .98rem; margin: 0; }
.stTabs button[role="tab"]:hover { opacity: 1; background: rgba(127,127,127,.15); }
.stTabs button[role="tab"][aria-selected="true"] {
    opacity: 1; background: linear-gradient(135deg, #6366F1, #7C3AED);
    box-shadow: 0 6px 16px -6px rgba(99,102,241,.8);
}
.stTabs button[role="tab"][aria-selected="true"],
.stTabs button[role="tab"][aria-selected="true"] * { color: #fff !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {
    display: none !important; height: 0 !important; background: transparent !important;
}

/* Desplegables */
[data-testid="stExpander"] { border: none !important; }
[data-testid="stExpander"] details {
    border: 1px solid rgba(99,102,241,.30) !important; border-radius: 14px !important;
    background: rgba(99,102,241,.06);
}
[data-testid="stExpander"] summary { font-weight: 600; padding: .7rem 1rem; }

/* Títulos de sección */
.sec-title { font-size: 1.35rem; font-weight: 700; margin: 1.2rem 0 .15rem 0; letter-spacing: -.01em; }
.sec-desc  { opacity: .7; margin-bottom: 1.1rem; font-size: .95rem; }

/* Inputs */
.stTextInput input, .stSelectbox [data-baseweb="select"] > div {
    border-radius: 12px !important; font-size: 1rem;
}
.stTextInput input { font-family: 'JetBrains Mono', monospace; }
.stTextInput input:focus { border-color: #6366F1 !important; box-shadow: 0 0 0 3px rgba(99,102,241,.18) !important; }

/* Botones */
.stButton > button, .stFormSubmitButton > button {
    border-radius: 12px; font-weight: 600; padding: .55rem 1.4rem; border: 1px solid rgba(99,102,241,.35);
    transition: all .15s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover { transform: translateY(-1px); border-color: #6366F1; color: #4F46E5; }
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primaryFormSubmit"] {
    background: linear-gradient(135deg, #6366F1, #7C3AED); color: #fff; border: none;
    box-shadow: 0 8px 18px -8px rgba(99,102,241,.7);
}
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover,
button[data-testid="stBaseButton-primary"]:hover, button[data-testid="stBaseButton-primaryFormSubmit"]:hover { color: #fff; filter: brightness(1.08); }

/* Tarjetas de resultado */
.result {
    background: linear-gradient(135deg, rgba(99,102,241,.10), rgba(219,39,119,.08));
    border: 1px solid rgba(99,102,241,.25); border-radius: 18px; padding: 1.2rem 1.4rem; margin: .8rem 0;
}
.result .lbl { font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; color: #6366F1; font-weight: 700; }
.result .val { font-family: 'JetBrains Mono', monospace; font-size: 1.9rem; font-weight: 700; word-break: break-all; margin-top: .2rem; }
.result .sub { opacity: .65; font-size: .9rem; margin-top: .25rem; font-family: 'JetBrains Mono', monospace; }

.chips { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: .7rem; margin: .6rem 0 1rem 0; }
.chip { background: rgba(127,127,127,.10); border: 1px solid rgba(127,127,127,.25); border-radius: 14px; padding: .75rem 1rem; }
.chip span { display: block; font-size: .72rem; text-transform: uppercase; letter-spacing: .07em; opacity: .6; font-weight: 600; }
.chip b { font-family: 'JetBrains Mono', monospace; font-size: 1rem; color: inherit; word-break: break-all; }

.hint { opacity: .7; font-size: .85rem; margin: -.4rem 0 .8rem 0; font-family: 'JetBrains Mono', monospace; }
.hint.ok::before { content: "✓ "; color: #10B981; font-weight: 700; }
.hint.bad { opacity: 1; color: #F43F5E; font-family: 'Inter', sans-serif; }

.hist-item { font-family: 'JetBrains Mono', monospace; font-size: .9rem; padding: .35rem 0; border-bottom: 1px dashed rgba(127,127,127,.3); }
.footer { text-align: center; opacity: .5; font-size: .8rem; margin-top: 2.5rem; }
</style>
""",
    unsafe_allow_html=True,
)


# ===========================================================================
# COMPONENTES DE INTERFAZ
# ===========================================================================
def seccion(titulo, descripcion):
    st.markdown(
        f'<div class="sec-title">{escape(titulo)}</div><div class="sec-desc">{descripcion}</div>',
        unsafe_allow_html=True,
    )


def tarjeta(etiqueta, valor, sub=None):
    sub_html = f'<div class="sub">{escape(sub)}</div>' if sub else ""
    st.markdown(
        f'<div class="result"><div class="lbl">{escape(etiqueta)}</div>'
        f'<div class="val">{escape(valor)}</div>{sub_html}</div>',
        unsafe_allow_html=True,
    )


def chips(pares):
    cuerpo = "".join(
        f'<div class="chip"><span>{escape(k)}</span><b>{escape(v)}</b></div>' for k, v in pares
    )
    st.markdown(f'<div class="chips">{cuerpo}</div>', unsafe_allow_html=True)


def pista(texto, ok=True):
    clase = "ok" if ok else "bad"
    st.markdown(f'<div class="hint {clase}">{escape(texto)}</div>', unsafe_allow_html=True)


# ===========================================================================
# SISTEMAS NUMÉRICOS (compartido por conversor y calculadora)
# ===========================================================================
DIGITOS = "0123456789ABCDEF"
PRECISION_FRACCION = 10  # dígitos después del punto en conversiones
PRECISION_DIVISION = 8  # dígitos después del punto en la división

SISTEMAS = {"Decimal": 10, "Binario": 2, "Octal": 8, "Hexadecimal": 16}
PREFIJOS = {2: "0B", 8: "0O", 16: "0X"}


class ErrorDeValor(ValueError):
    """Valor ingresado inválido."""


class ErrorDeOperacion(Exception):
    """Operación matemática no definida."""


def validar_y_separar(texto, base, nombre):
    """Valida el texto según la base. Devuelve (signo, parte_entera, parte_fraccion)."""
    if texto is None or not texto.strip():
        raise ErrorDeValor("No ingresaste ningún valor.")

    t = texto.strip().upper().replace(" ", "")

    signo = 1
    if t[0] in "+-":
        signo = -1 if t[0] == "-" else 1
        t = t[1:]
        if not t:
            raise ErrorDeValor("Solo ingresaste un signo, falta el número.")

    if base in PREFIJOS and t.startswith(PREFIJOS[base]):
        t = t[2:]
        if not t:
            raise ErrorDeValor("Solo ingresaste el prefijo, falta el número.")

    if t.count(".") > 1:
        raise ErrorDeValor("El número tiene más de un punto decimal.")
    entera, _, fraccion = t.partition(".")
    if not entera and not fraccion:
        raise ErrorDeValor("Solo ingresaste un punto, falta el número.")

    permitidos = DIGITOS[:base]
    invalidos = sorted({c for c in entera + fraccion if c not in permitidos})
    if invalidos:
        raise ErrorDeValor(
            f"Carácter(es) no válido(s) para {nombre} (base {base}): "
            f"{', '.join(repr(c) for c in invalidos)}. "
            f"Solo se permiten: {', '.join(permitidos)}."
        )
    return signo, entera or "0", fraccion


def a_decimal(texto, base, nombre):
    """Texto en base dada -> valor exacto (Fraction)."""
    signo, entera, fraccion = validar_y_separar(texto, base, nombre)
    valor = Fraction(int(entera, base))
    for i, c in enumerate(fraccion, start=1):
        valor += Fraction(DIGITOS.index(c), base ** i)
    return signo * valor


def desde_decimal(valor, base):
    """Valor (Fraction) -> texto en la base destino."""
    signo = "-" if valor < 0 else ""
    valor = abs(valor)
    entera = int(valor)
    fraccion = valor - entera

    if entera == 0:
        texto_entero = "0"
    else:
        digitos = []
        while entera > 0:
            entera, resto = divmod(entera, base)
            digitos.append(DIGITOS[resto])
        texto_entero = "".join(reversed(digitos))

    texto_fraccion = ""
    while fraccion > 0 and len(texto_fraccion) < PRECISION_FRACCION:
        fraccion *= base
        digito = int(fraccion)
        texto_fraccion += DIGITOS[digito]
        fraccion -= digito

    resultado = signo + texto_entero
    if texto_fraccion:
        resultado += "." + texto_fraccion
    if fraccion > 0:
        resultado += "..."  # truncado
    return resultado


def convertir(texto, base_origen, base_destino, nombre_origen="el sistema de origen"):
    return desde_decimal(a_decimal(texto, base_origen, nombre_origen), base_destino)


# ===========================================================================
# 1) CONVERSOR
# ===========================================================================
def _intercambiar_sistemas():
    o, d = st.session_state["conv_origen"], st.session_state["conv_destino"]
    st.session_state["conv_origen"], st.session_state["conv_destino"] = d, o


def pagina_conversor():
    seccion(
        "Conversor de sistemas numéricos",
        "Convierte entre decimal, binario, octal y hexadecimal. "
        "Acepta negativos, fracciones y prefijos <code>0b</code>, <code>0o</code>, <code>0x</code>.",
    )

    c1, c2, c3 = st.columns([5, 1.2, 5])
    with c1:
        nombre_o = st.selectbox("Desde", list(SISTEMAS), index=0, key="conv_origen")
    with c2:
        st.markdown("<div style='height:1.75rem'></div>", unsafe_allow_html=True)
        st.button("⇄", key="conv_swap", on_click=_intercambiar_sistemas, help="Intercambiar", use_container_width=True)
    with c3:
        nombre_d = st.selectbox("Hacia", list(SISTEMAS), index=1, key="conv_destino")

    with st.form("form_conversor", border=False):
        texto = st.text_input(f"Número en {nombre_o.lower()}", placeholder="Ej: 255.75")
        enviar = st.form_submit_button("Convertir", type="primary")

    if enviar:
        try:
            valor = a_decimal(texto, SISTEMAS[nombre_o], nombre_o)
            resultado = desde_decimal(valor, SISTEMAS[nombre_d])
            tarjeta(f"{nombre_o} → {nombre_d}", resultado, f"{texto.strip()} ({nombre_o})")
            otros = [(n, desde_decimal(valor, b)) for n, b in SISTEMAS.items() if n not in (nombre_o, nombre_d)]
            with st.expander("Ver equivalentes en otros sistemas"):
                chips(otros)
        except ErrorDeValor as e:
            st.error(str(e), icon="⚠️")


# ===========================================================================
# 2) CALCULADORA MULTI-BASE (algoritmos "a mano" sobre cadenas de dígitos)
# ===========================================================================
def _v(c):
    return DIGITOS.index(c)


def normalizar(s):
    s = s.lstrip("0")
    return s if s else "0"


def comparar(a, b):
    """-1 si a<b, 0 si a==b, 1 si a>b (el orden ASCII de 0-9A-F coincide con el valor)."""
    a, b = normalizar(a), normalizar(b)
    if len(a) != len(b):
        return -1 if len(a) < len(b) else 1
    return (a > b) - (a < b)


def sumar(a, b, base):
    n = max(len(a), len(b))
    a, b = a.zfill(n), b.zfill(n)
    acarreo, res = 0, []
    for i in range(n - 1, -1, -1):
        total = _v(a[i]) + _v(b[i]) + acarreo
        res.append(DIGITOS[total % base])
        acarreo = total // base
    if acarreo:
        res.append(DIGITOS[acarreo])
    return normalizar("".join(reversed(res)))


def _restar_mayor(a, b, base):
    """Resta con préstamo. Requiere a >= b."""
    n = max(len(a), len(b))
    a, b = a.zfill(n), b.zfill(n)
    prestamo, res = 0, []
    for i in range(n - 1, -1, -1):
        d = _v(a[i]) - _v(b[i]) - prestamo
        if d < 0:
            d += base
            prestamo = 1
        else:
            prestamo = 0
        res.append(DIGITOS[d])
    return normalizar("".join(reversed(res)))


def restar(a, b, base):
    if comparar(a, b) >= 0:
        return _restar_mayor(a, b, base)
    return "-" + _restar_mayor(b, a, base)


def _mult_digito(a, d, base):
    """Multiplica la cadena a por un único dígito d (0 <= d < base)."""
    if d == 0:
        return "0"
    acarreo, res = 0, []
    for c in reversed(a):
        total = _v(c) * d + acarreo
        res.append(DIGITOS[total % base])
        acarreo = total // base
    while acarreo:
        res.append(DIGITOS[acarreo % base])
        acarreo //= base
    return normalizar("".join(reversed(res)))


def multiplicar(a, b, base):
    """Multiplicación larga: productos parciales desplazados y sumados."""
    resultado = "0"
    for i, c in enumerate(reversed(b)):
        d = _v(c)
        if d:
            resultado = sumar(resultado, _mult_digito(a, d, base) + "0" * i, base)
    return resultado


def _cifra_cociente(residuo, b, base):
    for d in range(base - 1, 0, -1):
        if comparar(_mult_digito(b, d, base), residuo) <= 0:
            return d
    return 0


def dividir(a, b, base):
    """División larga. Devuelve (cociente, residuo, fraccion)."""
    if b == "0":
        raise ZeroDivisionError("No se puede dividir entre cero.")

    cociente, residuo = [], "0"
    for c in a:
        residuo = normalizar(residuo + c)
        d = _cifra_cociente(residuo, b, base)
        if d:
            residuo = _restar_mayor(residuo, _mult_digito(b, d, base), base)
        cociente.append(DIGITOS[d])
    q = normalizar("".join(cociente))

    frac, r = [], residuo
    for _ in range(PRECISION_DIVISION):
        if r == "0":
            break
        r = normalizar(r + "0")
        d = _cifra_cociente(r, b, base)
        if d:
            r = _restar_mayor(r, _mult_digito(b, d, base), base)
        frac.append(DIGITOS[d])
    return q, residuo, "".join(frac)


def validar_entero(texto, base, nombre):
    """Devuelve el número normalizado (str) o lanza ErrorDeValor. Solo enteros sin signo."""
    t = texto.strip().upper()
    if not t:
        raise ErrorDeValor("Campo vacío.")
    if re.search(r"\s", t):
        raise ErrorDeValor("El número no puede contener espacios.")
    if "-" in t or "+" in t:
        raise ErrorDeValor("No se permiten signos (+ o -).")
    if "." in t or "," in t:
        raise ErrorDeValor("No se permiten decimales: ingresa solo enteros.")
    if base in PREFIJOS and t.startswith(PREFIJOS[base]):
        t = t[2:]
        if not t:
            raise ErrorDeValor("Solo ingresaste el prefijo, falta el número.")
    permitidos = DIGITOS[:base]
    invalidos = sorted({c for c in t if c not in permitidos})
    if invalidos:
        raise ErrorDeValor(
            f"Carácter(es) no válido(s) para {nombre}: "
            f"{', '.join(repr(c) for c in invalidos)}. Solo se permiten {', '.join(permitidos)}."
        )
    return normalizar(t)


def a_entero(s, base):
    return int(s.lstrip("-"), base) * (-1 if s.startswith("-") else 1)


def de_entero(n, base):
    return desde_decimal(Fraction(n), base)


def entrada_numero(etiqueta, clave, base, nombre):
    """Campo de texto con validación en vivo. Devuelve el número normalizado o None."""
    texto = st.text_input(etiqueta, key=clave, placeholder=f"Número en {nombre.lower()}")
    if not texto.strip():
        return None
    try:
        num = validar_entero(texto, base, nombre)
    except ErrorDeValor as e:
        pista(str(e), ok=False)
        return None
    pista(f"= {a_entero(num, base)} en decimal")
    return num


def pagina_calculadora():
    seccion(
        "Calculadora multi-base",
        "Suma, resta, multiplica y divide en el sistema que elijas. "
        "Las operaciones se hacen dígito a dígito (acarreo, préstamo y división larga).",
    )

    c1, c2 = st.columns([1, 1.4])
    with c1:
        nombre = st.selectbox("Sistema numérico", list(SISTEMAS), index=1, key="calc_sis")
    with c2:
        op = st.radio(
            "Operación",
            ["Sumar", "Restar", "Multiplicar", "Dividir"],
            horizontal=True,
            key="calc_op",
        )
    base = SISTEMAS[nombre]
    simbolo = {"Sumar": "+", "Restar": "-", "Multiplicar": "×", "Dividir": "÷"}[op]

    c1, c2 = st.columns(2)
    with c1:
        a = entrada_numero("Primer número", "calc_a", base, nombre)
    with c2:
        b = entrada_numero("Segundo número", "calc_b", base, nombre)

    if "historial" not in st.session_state:
        st.session_state["historial"] = []

    if st.button("Calcular", type="primary", key="calc_btn"):
        if a is None or b is None:
            st.error("Ingresa dos números válidos para continuar.", icon="⚠️")
        else:
            try:
                expr = f"{a} {simbolo} {b}"
                dec_expr = f"{a_entero(a, base)} {simbolo} {a_entero(b, base)}"
                if op == "Dividir":
                    q, r, frac = dividir(a, b, base)
                    valor_dec = Fraction(a_entero(q, base))
                    tarjeta(f"Cociente ({nombre})", q, expr)
                    col1, col2 = st.columns(2)
                    with col1:
                        chips([("Residuo", f"{r}  (dec: {a_entero(r, base)})")])
                    with col2:
                        if frac:
                            chips([(f"Con fracción ({PRECISION_DIVISION} dígitos)", f"{q}.{frac}")])
                        else:
                            chips([("Con fracción", "División exacta")])
                    resumen = f"[{nombre}] {a} ÷ {b} = {q}" + (f".{frac}" if frac else "") + f", residuo {r}"
                else:
                    if op == "Sumar":
                        res = sumar(a, b, base)
                    elif op == "Restar":
                        res = restar(a, b, base)
                    else:
                        res = multiplicar(a, b, base)
                    valor_dec = Fraction(a_entero(res, base))
                    tarjeta(f"Resultado ({nombre})", res, expr)
                    resumen = f"[{nombre}] {a} {simbolo} {b} = {res}"

                st.caption(f"En decimal: {dec_expr} = {valor_dec}" if op != "Dividir" else f"En decimal: {dec_expr}")
                chips([(n, de_entero(int(valor_dec), bb)) for n, bb in SISTEMAS.items()])
                st.session_state["historial"].append(resumen)
            except ZeroDivisionError as e:
                st.error(str(e), icon="⚠️")

    if st.session_state["historial"]:
        with st.expander(f"Historial ({len(st.session_state['historial'])})"):
            for i, item in enumerate(reversed(st.session_state["historial"]), 1):
                st.markdown(f'<div class="hist-item">{escape(item)}</div>', unsafe_allow_html=True)
            if st.button("Borrar historial", key="calc_clear"):
                st.session_state["historial"] = []
                st.rerun()


# ===========================================================================
# 3) MCD Y mcm
# ===========================================================================
def _mcm_dos_enteros(a, b):
    return abs(a * b) // gcd(a, b)


def calcular_mcd(numeros):
    """MCD de racionales: MCD(numeradores) / mcm(denominadores). Ignora ceros."""
    no_ceros = [abs(x) for x in numeros if x != 0]
    if not no_ceros:
        raise ErrorDeOperacion("El MCD no está definido cuando todos los valores son 0.")
    num = reduce(gcd, (x.numerator for x in no_ceros))
    den = reduce(_mcm_dos_enteros, (x.denominator for x in no_ceros))
    return Fraction(num, den)


def calcular_mcm(numeros):
    """mcm de racionales: mcm(numeradores) / MCD(denominadores). Con un 0 es 0."""
    if any(x == 0 for x in numeros):
        return Fraction(0)
    absolutos = [abs(x) for x in numeros]
    num = reduce(_mcm_dos_enteros, (x.numerator for x in absolutos))
    den = reduce(gcd, (x.denominator for x in absolutos))
    return Fraction(num, den)


def convertir_valor(texto):
    t = texto.strip()
    if not t:
        raise ErrorDeValor("Hay un valor vacío.")
    try:
        return Fraction(t)
    except ZeroDivisionError:
        raise ErrorDeValor(f"'{t}': el denominador no puede ser 0.")
    except ValueError:
        raise ErrorDeValor(
            f"'{t}' no es un número válido (usa enteros, decimales con punto o fracciones a/b)."
        )


def leer_numeros(entrada):
    if entrada is None or not entrada.strip():
        raise ErrorDeValor("No ingresaste ningún valor.")
    partes = [p for p in re.split(r"[\s,;]+", entrada.strip()) if p]
    if len(partes) < 2:
        raise ErrorDeValor("Debes ingresar al menos 2 valores.")
    return [convertir_valor(p) for p in partes]


def formatear(valor):
    """Devuelve (texto_principal, texto_secundario_o_None)."""
    if valor.denominator == 1:
        return str(valor.numerator), None
    return f"{valor.numerator}/{valor.denominator}", f"≈ {float(valor):.10g}"


def pagina_mcd_mcm():
    seccion(
        "MCD y mcm",
        "Máximo común divisor y mínimo común múltiplo de 2 o más valores. "
        "Acepta enteros, decimales y fracciones.",
    )
    op = st.radio(
        "Operación",
        ["MCD", "mcm", "Ambos"],
        horizontal=True,
        key="mcd_op",
    )

    with st.form("form_mcd", border=False):
        entrada = st.text_input(
            "Valores (separados por espacios, comas o punto y coma)",
            placeholder="Ej: 12 18 24   ·   -8, 12   ·   2.5 0.75   ·   1/2 3/4",
        )
        enviar = st.form_submit_button("Calcular", type="primary")

    if enviar:
        try:
            numeros = leer_numeros(entrada)
            st.caption("Valores: " + ", ".join(str(n) for n in numeros))
            if op in ("MCD", "Ambos"):
                p, s = formatear(calcular_mcd(numeros))
                tarjeta("Máximo común divisor", p, s)
            if op in ("mcm", "Ambos"):
                p, s = formatear(calcular_mcm(numeros))
                tarjeta("Mínimo común múltiplo", p, s)
        except ErrorDeValor as e:
            st.error(str(e), icon="⚠️")
        except ErrorDeOperacion as e:
            st.error(str(e), icon="⚠️")


# ===========================================================================
# PÁGINA PRINCIPAL
# ===========================================================================
st.markdown(
    """
<div class="hero">
  <h1>Herramientas numéricas</h1>
  <p>Convierte entre sistemas, calcula en cualquier base y encuentra el MCD y el mcm.</p>
</div>
""",
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["Conversor", "Calculadora", "MCD y mcm"])
with tab1:
    pagina_conversor()
with tab2:
    pagina_calculadora()
with tab3:
    pagina_mcd_mcm()

st.markdown('<div class="footer">Hecho con Streamlit</div>', unsafe_allow_html=True)
