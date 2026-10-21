
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from streamlit_autorefresh import st_autorefresh

# ==========================================================
# VERDANT | Invernadero inteligente
# ==========================================================

st.set_page_config(
    page_title="VERDANT | Invernadero inteligente",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Firebase Realtime Database
FIREBASE_URL = "https://invernadero-d72ec-default-rtdb.firebaseio.com"

# Actualización automática cada 15 segundos
st_autorefresh(interval=15_000, key="verdant_actualizacion")


# ==========================================================
# CONEXIÓN CON FIREBASE
# ==========================================================

def leer_coleccion(nombre):
    """Lee datos de Firebase mediante su API REST."""
    url = f"{FIREBASE_URL}/{nombre}.json"

    respuesta = requests.get(url, timeout=10)
    respuesta.raise_for_status()

    datos = respuesta.json()

    if isinstance(datos, dict):
        return list(datos.values())

    if isinstance(datos, list):
        return [dato for dato in datos if dato is not None]

    return []


firebase_error = None
lecturas = []
riegos = []

try:
    lecturas = [
        dato
        for dato in leer_coleccion("lecturas")
        if isinstance(dato, dict) and dato.get("ts") is not None
    ]

    riegos = [
        dato
        for dato in leer_coleccion("riegos")
        if isinstance(dato, dict) and dato.get("ts") is not None
    ]

    lecturas.sort(key=lambda dato: int(dato["ts"]))
    riegos.sort(key=lambda dato: int(dato["ts"]))

except (
    requests.RequestException,
    ValueError,
    TypeError,
    KeyError,
) as error:
    firebase_error = str(error)


# ==========================================================
# ORGANIZAR LAS MEDICIONES
# ==========================================================

if lecturas:
    registros = []

    for dato in lecturas:
        try:
            registros.append({
                "Fecha y hora": pd.to_datetime(
                    int(dato["ts"]),
                    unit="ms",
                ),
                "Temperatura (°C)": float(dato["t"]),
                "Humedad (%)": float(dato["h"]),
            })
        except (
            KeyError,
            TypeError,
            ValueError,
            OverflowError,
        ):
            continue

    historico = pd.DataFrame(registros)

    if not historico.empty:
        historico = (
            historico
            .dropna()
            .sort_values("Fecha y hora")
            .reset_index(drop=True)
        )
else:
    historico = pd.DataFrame(
        columns=[
            "Fecha y hora",
            "Temperatura (°C)",
            "Humedad (%)",
        ]
    )

ultima_lectura = (
    historico.iloc[-1]
    if not historico.empty
    else None
)

ultimo_riego = riegos[-1] if riegos else None


# Imagen de referencia de la planta
PLANT_IMAGE = (
    "https://latiendadelcactus.com/wp-content/uploads/2017/06/"
    "kalanchoe-tomentosa.jpg"
)


# ==========================================================
# ESTILOS VISUALES
# ==========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

:root {
    --cream: #f7f5e9;
    --cream2: #fffdf4;
    --sage: #dce8d0;
    --sage2: #c4d9ae;
    --leaf: #729653;
    --deep: #244d3d;
    --deep2: #315e4b;
    --mint: #cde9df;
    --aqua: #78bcb3;
    --ink: #24483c;
    --muted: #6f8779;
    --line: #d7e1cb;
}

.stApp {
    color: var(--ink);
    background:
      radial-gradient(ellipse at 10% 0%, #dce8d0 0%, transparent 32%),
      radial-gradient(ellipse at 100% 18%, #d2e8df 0%, transparent 28%),
      linear-gradient(145deg, #f7f5e9 0%, #f4f3e5 58%, #eef3e5 100%);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(247,245,233,.82);
}

.block-container {
    max-width: 1500px;
    padding-top: 1.35rem;
    padding-bottom: 2.5rem;
}

h1, h2, h3, h4 {
    color: var(--deep) !important;
    font-family: 'Playfair Display', Georgia, serif !important;
}

p, label, .stMarkdown, [data-testid="stCaptionContainer"] {
    color: var(--ink);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f0f1df 0%, #e5eddc 60%, #dce9d8 100%);
    border-right: 1px solid #cad9c3;
}

section[data-testid="stSidebar"] * {
    color: var(--deep);
}

section[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: .25rem 0;
    font-weight: 600;
}

.brand {
    font-family: 'Playfair Display', Georgia, serif;
    color: var(--deep);
    font-size: 31px;
    font-weight: 700;
    letter-spacing: 4px;
    line-height: 1.15;
}

.brand-sub {
    color: var(--leaf);
    font-size: 10px;
    letter-spacing: 3px;
    margin-top: 4px;
}

.sidebar-note {
    background: #ffffff8c;
    border: 1px solid #d3dfc9;
    border-radius: 16px;
    padding: 13px;
    line-height: 1.65;
    font-size: 12px;
}

.hero {
    position: relative;
    overflow: hidden;
    border-radius: 28px;
    border: 1px solid #cbd9bd;
    background:
      linear-gradient(90deg, rgba(250,249,235,.97) 0%,
        rgba(250,249,235,.92) 44%, rgba(250,249,235,.13) 100%),
      url("https://latiendadelcactus.com/wp-content/uploads/2017/06/kalanchoe-tomentosa.jpg")
      center 44% / cover no-repeat,
      linear-gradient(120deg, #e9efd9, #d3e6d8);
    min-height: 285px;
    padding: 34px 38px;
    box-shadow: 0 12px 32px #385d3d12;
    margin-bottom: 26px;
}

.hero-content {
    max-width: 590px;
    position: relative;
    z-index: 1;
}

.hero-kicker {
    color: var(--leaf);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.hero h1 {
    font-size: clamp(35px, 4vw, 54px) !important;
    line-height: 1.08;
    margin: 13px 0 12px;
}

.hero p {
    max-width: 520px;
    color: #355a4b;
    line-height: 1.75;
    font-size: 14px;
}

.pill {
    display: inline-block;
    border-radius: 30px;
    padding: 8px 13px;
    margin: 4px 5px 0 0;
    background: var(--deep2);
    color: white;
    font-size: 11px;
    font-weight: 600;
}

.pill-light {
    display: inline-block;
    border-radius: 30px;
    padding: 7px 12px;
    margin: 4px 5px 0 0;
    background: #ffffffb8;
    color: var(--deep);
    border: 1px solid #bdcfb0;
    font-size: 11px;
    font-weight: 600;
}

.section-heading {
    display: flex;
    gap: 10px;
    align-items: center;
    color: var(--deep);
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 25px;
    font-weight: 700;
    margin: 5px 0 2px;
}

.section-sub {
    color: var(--muted);
    font-size: 12px;
    margin: 0 0 15px 36px;
    line-height: 1.6;
}

.panel {
    background: rgba(255,253,244,.84);
    border: 1px solid var(--line);
    border-radius: 22px;
    padding: 21px;
    box-shadow: 0 8px 25px #35553d0a;
    margin-bottom: 15px;
}

.panel-title {
    color: var(--deep);
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 19px;
    font-weight: 700;
}

.panel-sub {
    color: var(--muted);
    font-size: 11px;
    line-height: 1.75;
    margin-top: 5px;
}

.sensor-card {
    min-height: 150px;
    border: 1px solid #cbdcb8;
    border-radius: 22px;
    padding: 20px;
    background: linear-gradient(135deg, #faffed 0%, #e7f0d8 100%);
    box-shadow: 0 7px 20px #476b3510;
    position: relative;
    overflow: hidden;
}

.sensor-card:after {
    content: "❧";
    position: absolute;
    right: 6px;
    bottom: -24px;
    font-size: 90px;
    color: #719a5024;
    transform: rotate(-22deg);
}

.sensor-card.aqua {
    background: linear-gradient(135deg, #f1fbf5 0%, #d9eee7 100%);
    border-color: #bfddd3;
}

.sensor-label {
    font-size: 12px;
    color: #547466;
    font-weight: 700;
    letter-spacing: .5px;
    text-transform: uppercase;
}

.sensor-value {
    font-family: 'Playfair Display', Georgia, serif;
    color: var(--deep);
    font-size: 39px;
    font-weight: 700;
    margin: 8px 0 3px;
}

.sensor-note {
    font-size: 10px;
    color: var(--muted);
}

.sensor-icon {
    float: right;
    font-size: 28px;
    background: #ffffffa8;
    border: 1px solid #d4e0c8;
    border-radius: 50%;
    width: 53px;
    height: 53px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.plant-image-caption {
    color: var(--muted);
    font-size: 10px;
    text-align: center;
    padding-top: 7px;
}

.care-item {
    border-bottom: 1px solid #e0e7d6;
    padding: 8px 0;
    font-size: 12px;
    color: var(--deep);
}

.care-item:last-child {
    border-bottom: none;
}

.status-pill {
    display: inline-block;
    border-radius: 25px;
    padding: 7px 11px;
    background: #f6edcf;
    color: #7d6730;
    font-size: 11px;
    font-weight: 700;
}

.status-dot {
    display: inline-block;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #d9ad4a;
    margin-right: 7px;
}

.empty-state {
    text-align: center;
    border: 1px dashed #c7d7bc;
    background: #ffffff6b;
    border-radius: 18px;
    padding: 30px 15px;
    color: var(--muted);
}

.empty-icon {
    font-size: 34px;
    margin-bottom: 7px;
}

.step {
    border-left: 2px solid #c8d9b8;
    padding: 1px 0 15px 16px;
    margin-left: 8px;
    position: relative;
}

.step:before {
    content: "";
    position: absolute;
    left: -7px;
    top: 4px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #86a96a;
    border: 2px solid #fffdf4;
}

.step-title {
    color: var(--deep);
    font-size: 12px;
    font-weight: 700;
}

.step-desc {
    color: var(--muted);
    font-size: 11px;
    line-height: 1.6;
    margin-top: 3px;
}

div.stButton > button,
div.stDownloadButton > button {
    border: 1px solid #6f9457;
    border-radius: 13px;
    background: linear-gradient(110deg, #789b59, #a9c77e);
    color: #fffdf4;
    font-weight: 700;
    padding: 10px 15px;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    border-color: #315e4b;
    background: #315e4b;
    color: white;
}

div[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 15px;
    overflow: hidden;
}

hr {
    border-color: #cbd9c3;
}

.footer {
    text-align: center;
    padding: 25px 0 5px;
    color: #78907d;
    font-size: 10px;
    letter-spacing: 2px;
}

@media (max-width: 800px) {
    .hero {
        padding: 25px;
        background-position: 62% center;
    }

    .hero-content {
        max-width: 100%;
    }

    .sensor-card {
        padding: 16px;
    }

    .sensor-value {
        font-size: 32px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==========================================================
# MENÚ LATERAL
# ==========================================================

with st.sidebar:
    st.markdown('<div style="font-size:38px">🌿</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand">VERDANT</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">SMART GREENHOUSE</div>', unsafe_allow_html=True)
    st.write("")
    st.markdown("---")
    st.markdown("### 🍃 Explorar")

    seccion = st.radio(
        "Secciones",
        ["Vista general", "Histórico", "Sistema"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### 🪴 Tu planta")
    st.markdown("**Kalanchoe tomentosa**")
    st.caption("Planta panda · Hojas aterciopeladas")

    st.markdown(
        '<div class="sidebar-note">☀️ Luz indirecta brillante<br>'
        '💧 Riego moderado, cuando el sustrato esté seco<br>'
        '🌱 Suculenta de hojas carnosas</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    if firebase_error:
        st.markdown(
            '<span class="status-dot" style="background:#c65b45"></span>'
            '<b>Error de conexión</b>',
            unsafe_allow_html=True,
        )
        st.caption(f"Detalle del error: {firebase_error}")

    elif not historico.empty:
        st.markdown(
            '<span class="status-dot" style="background:#4b9b62"></span>'
            '<b>Firebase conectado</b>',
            unsafe_allow_html=True,
        )
        st.caption("Lecturas sincronizadas desde la nube.")

    else:
        st.markdown(
            '<span class="status-dot"></span>'
            '<b>Esperando mediciones</b>',
            unsafe_allow_html=True,
        )
        st.caption("Firebase responde; aún no hay lecturas guardadas.")


# ==========================================================
# PORTADA
# ==========================================================

st.markdown("""
<div class="hero">
  <div class="hero-content">
    <div class="hero-kicker">✦ Naturaleza + tecnología</div>
    <h1>Tu invernadero,<br>en equilibrio. 🍃</h1>
    <p>
      Un espacio inteligente para observar, comprender y cuidar tu planta.
      Consulta las condiciones ambientales y el historial de mediciones
      desde una sola pantalla.
    </p>
    <span class="pill">❧ Monitoreo ambiental</span>
    <span class="pill-light">♧ Riego inteligente</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# VISTA GENERAL
# ==========================================================

if seccion == "Vista general":

    st.markdown(
        '<div class="section-heading">🌿 El ambiente de tu planta</div>'
        '<div class="section-sub">Datos sincronizados desde Firebase y actualizados automáticamente cada 15 segundos.</div>',
        unsafe_allow_html=True,
    )

    if ultima_lectura is not None:
        temp_text = f"{ultima_lectura['Temperatura (°C)']:.1f}"
        hum_text = f"{ultima_lectura['Humedad (%)']:.0f}"
        ultima_hora = ultima_lectura["Fecha y hora"].strftime(
            "%d/%m/%Y · %H:%M:%S"
        )
    else:
        temp_text = "—"
        hum_text = "—"
        ultima_hora = "Esperando lectura real del DHT11"

    left, right = st.columns(2, gap="medium")

    with left:
        st.markdown(f"""
        <div class="sensor-card">
          <div class="sensor-icon">🌡️</div>
          <div class="sensor-label">Temperatura ambiente</div>
          <div class="sensor-value">{temp_text} <span style="font-size:18px">°C</span></div>
          <div class="sensor-note">Última lectura: {ultima_hora}</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown(f"""
        <div class="sensor-card aqua">
          <div class="sensor-icon">💧</div>
          <div class="sensor-label">Humedad ambiental</div>
          <div class="sensor-value">{hum_text} <span style="font-size:18px">%</span></div>
          <div class="sensor-note">Última lectura: {ultima_hora}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    plant_col, system_col = st.columns([1.12, 1], gap="large")

    with plant_col:
        st.markdown("""
        <div class="panel">
          <div class="panel-title">🌱 Conoce tu planta</div>
          <div class="panel-sub">KALANCHOE TOMENTOSA · PLANTA PANDA</div>
        </div>
        """, unsafe_allow_html=True)

        st.image(PLANT_IMAGE, width="stretch")

        st.markdown(
            '<div class="plant-image-caption">Kalanchoe tomentosa · hojas suaves con bordes marrones</div>',
            unsafe_allow_html=True,
        )

        st.markdown("""
        <div class="panel">
          <div class="panel-title">🌼 Cuidados de tu suculenta</div>
          <div class="panel-sub">Pequeños cuidados para mantenerla saludable.</div>
          <div class="care-item">☀️ <b>Luz:</b> brillante e indirecta</div>
          <div class="care-item">💧 <b>Riego:</b> moderado; deja secar el sustrato</div>
          <div class="care-item">🪴 <b>Sustrato:</b> suelto y con buen drenaje</div>
          <div class="care-item">🌿 <b>Hojas:</b> carnosas y cubiertas de pelitos</div>
        </div>
        """, unsafe_allow_html=True)

    with system_col:
        if ultimo_riego:
            try:
                riego_fecha = pd.to_datetime(
                    int(ultimo_riego["ts"]), unit="ms"
                ).strftime("%d/%m/%Y · %H:%M:%S")
                estado_riego = f"Último evento de riego registrado: {riego_fecha}"
            except (ValueError, TypeError, KeyError):
                estado_riego = "Hay un evento de riego guardado en Firebase."
        else:
            estado_riego = "Todavía no hay eventos de riego registrados."

        st.markdown(f"""
        <div class="panel">
          <div class="panel-title">💧 Sistema de riego</div>
          <div class="panel-sub">ESTADO DE LA BOMBA Y DEL RELÉ</div>
          <br>
          <span class="status-pill">
            <span class="status-dot"></span>
            {'Evento de riego registrado' if ultimo_riego else 'Sin eventos registrados'}
          </span>
          <p style="font-size:12px;line-height:1.8;margin-top:15px">{estado_riego}</p>
          <p style="font-size:11px;line-height:1.7">
            Esta tarjeta informa los eventos guardados en Firebase;
            no activa la bomba física desde Streamlit.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="panel">
          <div class="panel-title">🌐 Conexión del sistema</div>
          <div class="panel-sub">Así viajan las lecturas hasta tu panel.</div>
          <br>
          <div class="step">
            <div class="step-title">01 · Arduino Uno</div>
            <div class="step-desc">Lee el sensor DHT11.</div>
          </div>
          <div class="step">
            <div class="step-title">02 · Programa Python</div>
            <div class="step-desc">Recibe los datos por el cable USB y los envía a Firebase.</div>
          </div>
          <div class="step">
            <div class="step-title">03 · Firebase</div>
            <div class="step-desc">Guarda las mediciones reales en la nube.</div>
          </div>
          <div class="step" style="padding-bottom:0">
            <div class="step-title">04 · VERDANT</div>
            <div class="step-desc">Actualiza los valores y el histórico automáticamente.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">📈 Histórico ambiental</div>'
        '<div class="section-sub">Las gráficas se generan con las mediciones guardadas en Firebase.</div>',
        unsafe_allow_html=True,
    )

    df = historico.copy()

    if df.empty:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">🌱</div>
          <b style="color:#315e4b">Tu histórico comienza aquí</b>
          <p style="font-size:12px">
            Todavía no hay mediciones registradas.<br>
            Cuando el sistema guarde lecturas en Firebase, aparecerán aquí.
          </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df["Fecha y hora"],
            y=df["Temperatura (°C)"],
            mode="lines+markers",
            name="Temperatura",
            line=dict(color="#789b59", width=3, shape="spline"),
        ))

        fig.add_trace(go.Scatter(
            x=df["Fecha y hora"],
            y=df["Humedad (%)"],
            mode="lines+markers",
            name="Humedad",
            line=dict(color="#4caaa0", width=3, shape="spline"),
            yaxis="y2",
        ))

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,253,244,.6)",
            font=dict(color="#315e4b"),
            height=360,
            margin=dict(l=10, r=10, t=35, b=10),
            legend=dict(orientation="h", y=1.12),
            xaxis=dict(title="Fecha y hora", gridcolor="#dfe7d8"),
            yaxis=dict(title="Temperatura (°C)", gridcolor="#dfe7d8"),
            yaxis2=dict(
                title="Humedad (%)",
                overlaying="y",
                side="right",
                showgrid=False,
            ),
        )

        st.plotly_chart(fig, width="stretch")


# ==========================================================
# HISTÓRICO
# ==========================================================

elif seccion == "Histórico":

    st.markdown(
        '<div class="section-heading">📚 Bitácora de mediciones</div>'
        '<div class="section-sub">Registro cronológico de las lecturas del invernadero.</div>',
        unsafe_allow_html=True,
    )

    df = historico.copy()

    if df.empty:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">🍃</div>
          <b style="color:#315e4b">Todavía no hay registros</b>
          <p style="font-size:12px">
            Las mediciones aparecerán cuando se guarden en Firebase.
          </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        df = df.sort_values("Fecha y hora", ascending=False)

        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Descargar histórico CSV",
            data=csv,
            file_name="historico_invernadero.csv",
            mime="text/csv",
        )


# ==========================================================
# SISTEMA
# ==========================================================

elif seccion == "Sistema":

    st.markdown(
        '<div class="section-heading">⚙️ Centro de conexión</div>'
        '<div class="section-sub">Estado de la conexión y recorrido de los datos.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="panel">
      <div class="panel-title">🔌 Arquitectura del invernadero</div>
      <div class="panel-sub">El recorrido previsto para los datos del sensor.</div>
      <br>
      <div class="step">
        <div class="step-title">01 · Arduino Uno</div>
        <div class="step-desc">Lee la temperatura y la humedad con el DHT11.</div>
      </div>
      <div class="step">
        <div class="step-title">02 · Programa Python en el computador</div>
        <div class="step-desc">Lee el puerto serial USB y envía las mediciones a Firebase.</div>
      </div>
      <div class="step">
        <div class="step-title">03 · Firebase</div>
        <div class="step-desc">Almacena las mediciones para que el panel pueda consultarlas.</div>
      </div>
      <div class="step" style="padding-bottom:0">
        <div class="step-title">04 · Panel VERDANT</div>
        <div class="step-desc">Muestra valores reales, gráficas e histórico.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if firebase_error:
        st.error(f"Detalle del error: {firebase_error}")

    elif historico.empty:
        st.info(
            "Firebase se está consultando, pero todavía no hay mediciones. "
            "Cuando el programa que recibe el Arduino guarde datos en "
            "'lecturas', aparecerán aquí."
        )

    else:
        st.success(
            f"Firebase conectado. Hay {len(historico)} mediciones disponibles. "
            "El panel se actualiza cada 15 segundos."
        )

    st.markdown("### 📡 Datos recibidos")

    st.write(f"**Mediciones ambientales:** {len(historico)}")
    st.write(f"**Eventos de riego:** {len(riegos)}")

    if not historico.empty:
        st.write(
            "**Última lectura:** "
            + historico.iloc[-1]["Fecha y hora"].strftime("%d/%m/%Y %H:%M:%S")
        )


# ==========================================================
# PIE DE PÁGINA
# ==========================================================

st.markdown("""
<div class="footer">
  VERDANT · CULTIVAR CON INTELIGENCIA · CUIDAR CON NATURALEZA 🌿
</div>
""", unsafe_allow_html=True)
