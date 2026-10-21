
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="VERDANT | Invernadero inteligente",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "historico" not in st.session_state:
    st.session_state.historico = pd.DataFrame(
        columns=["Hora", "Temperatura", "Humedad"]
    )

# =====================================================
# ESTILOS
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

.stApp {
    background: #f7f5ed;
    color: #294b37;
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #e8eee1;
    border-right: 1px solid #d7e1d0;
}

[data-testid="stSidebar"] * {
    color: #294b37;
}

.brand {
    font-size: 29px;
    font-weight: 700;
    letter-spacing: 4px;
    color: #294b37;
    margin-bottom: 0;
}

.brand-sub {
    font-size: 10px;
    letter-spacing: 3px;
    color: #7b9276;
    margin-top: 0;
}

.eyebrow {
    color: #789273;
    text-transform: uppercase;
    letter-spacing: 3px;
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 10px;
}

.hero-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(35px, 4vw, 55px);
    line-height: 1.12;
    color: #254b37;
    font-weight: 600;
    margin-bottom: 14px;
}

.hero-description {
    color: #718171;
    font-size: 15px;
    line-height: 1.8;
    max-width: 700px;
}

.hero-pill {
    display: inline-block;
    background: #e4eddf;
    color: #426747;
    border-radius: 30px;
    padding: 9px 15px;
    font-size: 11px;
    letter-spacing: 1px;
    margin-top: 14px;
}

.section-title {
    font-family: 'Playfair Display', Georgia, serif;
    color: #294b37;
    font-size: 27px;
    font-weight: 600;
}

.section-caption {
    font-size: 12px;
    color: #839080;
    margin-bottom: 18px;
}

.metric-card {
    background: #fffefa;
    border: 1px solid #e4e9de;
    border-radius: 20px;
    padding: 22px;
    min-height: 142px;
    box-shadow: 0 5px 20px rgba(42,72,47,.04);
}

.metric-label {
    color: #788775;
    font-size: 11px;
    letter-spacing: 1.3px;
    font-weight: 700;
}

.metric-value {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 36px;
    color: #294b37;
    margin: 10px 0 4px;
}

.metric-note {
    color: #8a9688;
    font-size: 11px;
}

.panel {
    background: #fffefa;
    border: 1px solid #e4e9de;
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 5px 20px rgba(42,72,47,.035);
}

.plant-scene {
    background: linear-gradient(160deg, #edf2e4, #d6e5c9);
    border-radius: 24px;
    padding: 20px;
    text-align: center;
    min-height: 320px;
    overflow: hidden;
}

.plant-sun {
    font-size: 34px;
    text-align: right;
    margin-right: 16px;
}

.plant-art {
    font-family: sans-serif;
    font-size: 88px;
    line-height: 1.4;
    margin: 12px 0;
}

.plant-name {
    color: #355d3e;
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 23px;
    font-weight: 600;
}

.plant-label {
    font-size: 10px;
    letter-spacing: 2px;
    color: #71866c;
    margin-top: 8px;
}

.plant-caption {
    color: #71816e;
    font-size: 12px;
    line-height: 1.8;
    margin-top: 14px;
}

.status-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 0;
    border-bottom: 1px solid #edf0e8;
}

.status-row:last-child {
    border-bottom: none;
}

.status-icon {
    min-width: 42px;
    height: 42px;
    border-radius: 14px;
    background: #e8efe2;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 21px;
}

.status-title {
    color: #355640;
    font-size: 13px;
    font-weight: 700;
}

.status-desc {
    color: #879284;
    font-size: 11px;
    margin-top: 4px;
}

.notice {
    background: #f3efdf;
    border: 1px solid #e9dfc1;
    border-radius: 15px;
    padding: 15px;
    color: #7e7048;
    font-size: 12px;
    line-height: 1.8;
}

.flow-step {
    background: #edf2e8;
    border: 1px solid #dce7d6;
    border-radius: 16px;
    padding: 17px 10px;
    text-align: center;
    color: #34573d;
    font-weight: 700;
    font-size: 13px;
}

.flow-desc {
    font-size: 10px;
    font-weight: 400;
    color: #83917f;
    margin-top: 5px;
}

.stButton > button {
    background: #f9fbf6;
    border: 1px solid #d8e2d2;
    color: #31563b;
    border-radius: 12px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #e8efe2;
    color: #254b37;
    border-color: #769b73;
}

.footer {
    text-align: center;
    color: #91a08e;
    font-size: 11px;
    letter-spacing: 1px;
    padding-top: 20px;
}

hr {
    border-color: #e2e7dc;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# BARRA LATERAL
# =====================================================

with st.sidebar:
    st.markdown(
        '<p class="brand">VERDANT</p>'
        '<p class="brand-sub">SMART GREENHOUSE</p>',
        unsafe_allow_html=True
    )

    st.markdown("### 🌱 Navegación")

    pagina = st.radio(
        "Selecciona una sección",
        ["Vista general", "Histórico", "Sistema"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("#### 🌿 Nuestro propósito")
    st.caption(
        "Unir naturaleza y tecnología para cuidar "
        "las plantas de manera inteligente."
    )

    st.markdown("---")

    st.markdown("""
    <div class="notice">
        <b>Estado del proyecto</b><br>
        La interfaz está preparada. Las lecturas reales aparecerán
        cuando se complete la conexión con Arduino y Firebase.
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# CABECERA
# =====================================================

st.markdown(
    '<div class="eyebrow">TU PEQUEÑO ECOSISTEMA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-title">Un hogar más verde,<br>'
    'una planta más feliz.</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="hero-description">
Bienvenido a tu invernadero inteligente. Un espacio donde
la naturaleza y la tecnología trabajan juntas para cuidar
cada hoja, cada gota de agua y cada nuevo crecimiento.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-pill">
    ✿ &nbsp; CULTIVANDO UN FUTURO MÁS VERDE
</div>
""", unsafe_allow_html=True)

st.write("")


# =====================================================
# VISTA GENERAL
# =====================================================

if pagina == "Vista general":

    st.markdown(
        '<div class="section-title">El bienestar de tu planta</div>'
        '<div class="section-caption">'
        'Información ambiental de tu invernadero</div>',
        unsafe_allow_html=True
    )

    datos = st.session_state.historico

    temp = None
    hum = None

    if not datos.empty:
        temp = datos.iloc[-1]["Temperatura"]
        hum = datos.iloc[-1]["Humedad"]

    col1, col2, col3 = st.columns(3)

    with col1:
        valor = f"{temp:.1f} °C" if temp is not None else "—"

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">☀️ TEMPERATURA</div>
            <div class="metric-value">{valor}</div>
            <div class="metric-note">Ambiente del invernadero</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        valor = f"{hum:.1f} %" if hum is not None else "—"

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💧 HUMEDAD</div>
            <div class="metric-value">{valor}</div>
            <div class="metric-note">Humedad relativa del aire</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        estado = "Sin conexión" if datos.empty else "Con datos"

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🌿 ESTADO</div>
            <div class="metric-value" style="font-size:26px">
                {estado}
            </div>
            <div class="metric-note">Recepción de mediciones</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    izquierda, derecha = st.columns([1, 1], gap="large")

    # PLANTA
    with izquierda:
        st.markdown(
            '<div class="section-title">Un rincón de naturaleza</div>'
            '<div class="section-caption">'
            'Inspiración botánica para tu invernadero</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="plant-scene">
            <div class="plant-sun">☀️</div>
            <div class="plant-art">🌿</div>
            <div style="font-size:38px;line-height:1.3">
                🍃 🪴 🍃
            </div>
            <div class="plant-name">Un espacio para crecer</div>
            <div class="plant-label">
                CRECER · CUIDAR · FLORECER
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="plant-caption">
            <b>La protagonista de nuestro invernadero.</b><br>
            Observamos las condiciones ambientales para acompañar
            el crecimiento de nuestras plantas y crear un espacio
            lleno de vida.
        </div>
        """, unsafe_allow_html=True)

    # CENTRO DE CONTROL CORREGIDO
    with derecha:
        st.markdown(
            '<div class="section-title">Centro de control</div>'
            '<div class="section-caption">'
            'Los elementos de tu invernadero</div>',
            unsafe_allow_html=True
        )

        componentes = [
            ("🌡️", "Sensor DHT11",
             "Mide temperatura y humedad ambiental"),
            ("🧠", "Arduino Uno",
             "Lee y procesa los datos del sensor"),
            ("💦", "Bomba de agua",
             "Accionamiento mediante módulo relé"),
            ("☁️", "Firebase",
             "Almacena las mediciones en la nube")
        ]

        st.markdown('<div class="panel">', unsafe_allow_html=True)

        for emoji, titulo, descripcion in componentes:
            st.markdown(
                f"""
                <div class="status-row">
                    <div class="status-icon">{emoji}</div>
                    <div>
                        <div class="status-title">{titulo}</div>
                        <div class="status-desc">{descripcion}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

        st.write("")

        st.markdown("""
        <div class="notice">
            <b>🌱 Conexión pendiente</b><br>
            La página todavía no está recibiendo datos reales.
            Conectaremos Arduino, Python y Firebase para actualizar
            las mediciones automáticamente.
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # FLUJO DE DATOS
    st.markdown(
        '<div class="section-title">Cómo funciona la magia</div>'
        '<div class="section-caption">El recorrido de los datos</div>',
        unsafe_allow_html=True
    )

    columnas = st.columns(4)

    pasos = [
        ("🌡️", "Arduino", "Lee los sensores"),
        ("💻", "Python", "Envía los datos"),
        ("☁️", "Firebase", "Guarda las lecturas"),
        ("🌿", "VERDANT", "Muestra los resultados")
    ]

    for columna, (emoji, titulo, descripcion) in zip(columnas, pasos):
        with columna:
            st.markdown(f"""
            <div class="flow-step">
                <div style="font-size:26px">{emoji}</div>
                <div style="margin-top:7px">{titulo}</div>
                <div class="flow-desc">{descripcion}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.caption(
        "La interfaz aún no acciona la bomba física. "
        "Su control requiere completar y probar la conexión electrónica."
    )


# =====================================================
# HISTÓRICO
# =====================================================

elif pagina == "Histórico":

    st.markdown(
        '<div class="eyebrow">MEMORIA DEL INVERNADERO</div>'
        '<div class="section-title">Histórico ambiental</div>'
        '<div class="section-caption">'
        'Consulta las mediciones recibidas por el sistema.</div>',
        unsafe_allow_html=True
    )

    datos = st.session_state.historico

    if datos.empty:
        st.markdown("""
        <div class="panel" style="text-align:center;padding:45px 20px;">
            <div style="font-size:55px;">🌱</div>
            <div style="font-family:'Playfair Display',Georgia,serif;
                        font-size:26px;color:#294b37;margin:15px 0;">
                Tu historia comienza aquí
            </div>
            <div style="color:#819080;font-size:13px;line-height:1.8;">
                Aún no hay mediciones registradas.<br>
                Al conectar Firebase, aquí aparecerá el historial real
                de temperatura y humedad.
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=datos["Hora"],
            y=datos["Temperatura"],
            name="Temperatura (°C)",
            mode="lines+markers",
            line=dict(color="#477c53", width=3)
        ))

        fig.add_trace(go.Scatter(
            x=datos["Hora"],
            y=datos["Humedad"],
            name="Humedad (%)",
            mode="lines+markers",
            line=dict(color="#d1ad5b", width=3),
            yaxis="y2"
        ))

        fig.update_layout(
            paper_bgcolor="#fffefa",
            plot_bgcolor="#fffefa",
            font=dict(color="#49604b"),
            margin=dict(l=15, r=15, t=40, b=15),
            legend=dict(orientation="h", y=1.12),
            xaxis=dict(title="Hora", gridcolor="#edf0e8"),
            yaxis=dict(
                title="Temperatura (°C)",
                gridcolor="#edf0e8"
            ),
            yaxis2=dict(
                title="Humedad (%)",
                overlaying="y",
                side="right",
                showgrid=False
            ),
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Registro de mediciones")
        st.dataframe(datos, use_container_width=True, hide_index=True)

        st.download_button(
            "⬇️ Descargar histórico CSV",
            data=datos.to_csv(index=False).encode("utf-8"),
            file_name="historico_invernadero.csv",
            mime="text/csv"
        )


# =====================================================
# SISTEMA
# =====================================================

elif pagina == "Sistema":

    st.markdown(
        '<div class="eyebrow">TECNOLOGÍA Y NATURALEZA</div>'
        '<div class="section-title">Arquitectura del sistema</div>'
        '<div class="section-caption">'
        'Los componentes que hacen posible nuestro invernadero.'
        '</div>',
        unsafe_allow_html=True
    )

    componentes_sistema = [
        ("🌡️", "DHT11 — Sensor ambiental",
         "Mide la temperatura y la humedad del aire."),
        ("🔌", "Arduino Uno — Controlador",
         "Lee las mediciones y se comunica por USB."),
        ("💧", "Relé de 5 V y bomba",
         "Permiten controlar el riego mediante un circuito adecuado."),
        ("💻", "Python — Comunicación",
         "Lee los datos seriales y los envía a Firebase."),
        ("☁️", "Firebase — Base de datos",
         "Almacena las lecturas para consultarlas desde la web.")
    ]

    for emoji, titulo, descripcion in componentes_sistema:
        st.markdown(f"""
        <div class="panel" style="margin-bottom:12px;">
            <div class="status-row">
                <div class="status-icon">{emoji}</div>
                <div style="flex:1">
                    <div class="status-title">{titulo}</div>
                    <div class="status-desc">{descripcion}</div>
                </div>
                <div style="font-size:10px;font-weight:700;color:#a17f3e;">
                    PENDIENTE
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class="notice">
        <b>¿Cómo se conectan?</b><br>
        Arduino Uno → USB → Python → Firebase → Página web.<br><br>
        El computador puede funcionar como puente entre Arduino y Firebase.
        La bomba necesita una conexión eléctrica adecuada y pruebas seguras
        antes de activar el riego.
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown("#### Próximos pasos")

    st.markdown("""
    - [ ] Comprobar el sensor DHT11.
    - [ ] Leer los datos por el puerto serial.
    - [ ] Configurar Firebase.
    - [ ] Conectar el programa Python.
    - [ ] Mostrar las mediciones reales en la página.
    - [ ] Configurar y probar el control de riego.
    """)


# =====================================================
# PIE DE PÁGINA
# =====================================================

st.markdown("---")

st.markdown("""
<div class="footer">
    VERDANT · CULTIVANDO TECNOLOGÍA, CUIDANDO LA NATURALEZA 🌿
</div>
""", unsafe_allow_html=True)
