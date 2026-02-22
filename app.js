/* ============================================
   SIMULADOR DE EXAMEN B-II B — LÓGICA
   ============================================ */

// Estado del examen
let preguntasExamen = [];
let respuestasUsuario = [];
let preguntaActualIdx = 0;
let timerInterval = null;
let tiempoRestante = 40 * 60; // 40 minutos en segundos
const TOTAL_PREGUNTAS = 40;
const PREGUNTAS_APROBACION = 35;

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('total-banco').textContent = PREGUNTAS_BANCO.length;
});

// ===== FUNCIONES PRINCIPALES =====

function iniciarExamen() {
    // Seleccionar 40 preguntas aleatorias
    preguntasExamen = seleccionarAleatorias(PREGUNTAS_BANCO, TOTAL_PREGUNTAS);
    respuestasUsuario = new Array(TOTAL_PREGUNTAS).fill(-1);
    preguntaActualIdx = 0;
    tiempoRestante = 40 * 60;

    // Cambiar pantalla
    mostrarPantalla('pantalla-examen');

    // Generar dots de navegación
    generarNavDots();

    // Mostrar primera pregunta
    mostrarPregunta(0);

    // Iniciar temporizador
    iniciarTimer();
}

function seleccionarAleatorias(array, n) {
    const copia = [...array];
    const resultado = [];
    for (let i = 0; i < n && copia.length > 0; i++) {
        const idx = Math.floor(Math.random() * copia.length);
        resultado.push(copia.splice(idx, 1)[0]);
    }
    return resultado;
}

function mostrarPregunta(idx) {
    preguntaActualIdx = idx;
    const pregunta = preguntasExamen[idx];

    // Actualizar header
    document.getElementById('pregunta-actual-label').textContent = `${idx + 1} / ${TOTAL_PREGUNTAS}`;
    document.getElementById('pregunta-numero').textContent = `Pregunta ${idx + 1}`;
    document.getElementById('pregunta-texto').textContent = pregunta.pregunta;

    // Imagen de la pregunta
    let imgContainer = document.getElementById('pregunta-imagen');
    if (!imgContainer) {
        imgContainer = document.createElement('div');
        imgContainer.id = 'pregunta-imagen';
        imgContainer.className = 'pregunta-imagen-container';
        document.getElementById('pregunta-texto').after(imgContainer);
    }
    if (pregunta.imagen) {
        imgContainer.innerHTML = `<img src="${pregunta.imagen}" alt="Imagen de la pregunta" class="pregunta-img" onerror="this.parentElement.innerHTML='<div class=\'imagen-placeholder\'>🖼️ Imagen no disponible<br><small>${pregunta.imagen}</small></div>'">`;
        imgContainer.style.display = 'block';
    } else {
        imgContainer.innerHTML = '';
        imgContainer.style.display = 'none';
    }

    // Progreso
    const porcentaje = ((idx + 1) / TOTAL_PREGUNTAS) * 100;
    document.getElementById('progreso-fill').style.width = porcentaje + '%';

    // Opciones
    const letras = ['A', 'B', 'C', 'D'];
    const contenedor = document.getElementById('opciones-lista');
    contenedor.innerHTML = '';

    pregunta.opciones.forEach((opcion, i) => {
        const btn = document.createElement('button');
        btn.className = 'opcion-btn';
        if (respuestasUsuario[idx] === i) btn.classList.add('seleccionada');
        btn.onclick = () => seleccionarRespuesta(idx, i);
        btn.innerHTML = `
            <span class="opcion-letra">${letras[i]}</span>
            <span class="opcion-texto">${opcion}</span>
        `;
        contenedor.appendChild(btn);
    });

    // Botones de navegación
    document.getElementById('btn-anterior').disabled = idx === 0;
    document.getElementById('btn-siguiente').textContent = idx === TOTAL_PREGUNTAS - 1 ? '' : '';
    const btnSig = document.getElementById('btn-siguiente');
    if (idx === TOTAL_PREGUNTAS - 1) {
        btnSig.innerHTML = 'Terminar <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
        btnSig.onclick = () => confirmarTerminar();
    } else {
        btnSig.innerHTML = 'Siguiente <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M6 3l5 5-5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
        btnSig.onclick = () => preguntaSiguiente();
    }

    // Actualizar dots
    actualizarNavDots();
}

function seleccionarRespuesta(pregIdx, opcionIdx) {
    respuestasUsuario[pregIdx] = opcionIdx;

    // Actualizar visual
    const btns = document.querySelectorAll('.opcion-btn');
    btns.forEach((btn, i) => {
        btn.classList.toggle('seleccionada', i === opcionIdx);
    });

    // Actualizar dot
    actualizarNavDots();
}

function preguntaAnterior() {
    if (preguntaActualIdx > 0) {
        mostrarPregunta(preguntaActualIdx - 1);
    }
}

function preguntaSiguiente() {
    if (preguntaActualIdx < TOTAL_PREGUNTAS - 1) {
        mostrarPregunta(preguntaActualIdx + 1);
    }
}

// ===== NAVEGACIÓN DOTS =====

function generarNavDots() {
    const contenedor = document.getElementById('nav-dots');
    contenedor.innerHTML = '';
    for (let i = 0; i < TOTAL_PREGUNTAS; i++) {
        const dot = document.createElement('button');
        dot.className = 'nav-dot';
        dot.title = `Pregunta ${i + 1}`;
        dot.onclick = () => mostrarPregunta(i);
        contenedor.appendChild(dot);
    }
}

function actualizarNavDots() {
    const dots = document.querySelectorAll('.nav-dot');
    dots.forEach((dot, i) => {
        dot.className = 'nav-dot';
        if (i === preguntaActualIdx) dot.classList.add('actual');
        else if (respuestasUsuario[i] !== -1) dot.classList.add('respondida');
    });
}

// ===== TEMPORIZADOR =====

function iniciarTimer() {
    clearInterval(timerInterval);
    actualizarTimerDisplay();

    timerInterval = setInterval(() => {
        tiempoRestante--;
        actualizarTimerDisplay();

        if (tiempoRestante <= 0) {
            clearInterval(timerInterval);
            terminarExamen();
        }
    }, 1000);
}

function actualizarTimerDisplay() {
    const min = Math.floor(tiempoRestante / 60);
    const seg = tiempoRestante % 60;
    const texto = `${min.toString().padStart(2, '0')}:${seg.toString().padStart(2, '0')}`;
    document.getElementById('timer-texto').textContent = texto;

    const timer = document.getElementById('timer');
    timer.className = 'timer';
    if (tiempoRestante <= 60) timer.classList.add('danger');
    else if (tiempoRestante <= 300) timer.classList.add('warning');
}

// ===== TERMINAR EXAMEN =====

function confirmarTerminar() {
    const sinResponder = respuestasUsuario.filter(r => r === -1).length;
    const modal = document.getElementById('modal-confirmar');
    const mensaje = document.getElementById('modal-mensaje');

    if (sinResponder > 0) {
        mensaje.textContent = `Tienes ${sinResponder} pregunta${sinResponder > 1 ? 's' : ''} sin responder. ¿Estás seguro de que deseas terminar?`;
    } else {
        mensaje.textContent = '¿Estás seguro de que deseas terminar el examen?';
    }

    modal.classList.add('visible');
}

function cerrarModal() {
    document.getElementById('modal-confirmar').classList.remove('visible');
}

function terminarExamen() {
    clearInterval(timerInterval);
    cerrarModal();

    // Calcular resultados
    let correctas = 0;
    let incorrectas = 0;
    let sinResponder = 0;

    preguntasExamen.forEach((pregunta, i) => {
        if (respuestasUsuario[i] === -1) sinResponder++;
        else if (respuestasUsuario[i] === pregunta.correcta) correctas++;
        else incorrectas++;
    });

    // Mostrar resultados
    mostrarResultados(correctas, incorrectas, sinResponder);
}

function mostrarResultados(correctas, incorrectas, sinResponder) {
    mostrarPantalla('pantalla-resultados');

    const aprobado = correctas >= PREGUNTAS_APROBACION;
    const porcentaje = Math.round((correctas / TOTAL_PREGUNTAS) * 100);

    // Ícono y texto
    document.getElementById('resultado-icono').textContent = aprobado ? '🎉' : '😔';
    document.getElementById('resultado-titulo').textContent = aprobado ? '¡Felicidades!' : 'Examen Finalizado';

    const estado = document.getElementById('resultado-estado');
    estado.textContent = aprobado ? 'APROBADO' : 'DESAPROBADO';
    estado.className = 'resultado-estado ' + (aprobado ? 'aprobado' : 'desaprobado');

    // Stats
    document.getElementById('stat-correctas').textContent = correctas;
    document.getElementById('stat-incorrectas').textContent = incorrectas;
    document.getElementById('stat-sin-responder').textContent = sinResponder;

    // Círculo de progreso
    const circunferencia = 2 * Math.PI * 54; // r=54
    const offset = circunferencia - (porcentaje / 100) * circunferencia;

    // Necesitamos agregar el gradiente SVG para el círculo
    const svg = document.querySelector('.circle-progress svg');
    if (!svg.querySelector('defs')) {
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        const grad = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
        grad.id = 'circleGrad';
        grad.innerHTML = `<stop offset="0%" stop-color="${aprobado ? '#34d399' : '#f87171'}"/>
                          <stop offset="100%" stop-color="${aprobado ? '#60a5fa' : '#fbbf24'}"/>`;
        defs.appendChild(grad);
        svg.insertBefore(defs, svg.firstChild);
    } else {
        const stops = svg.querySelectorAll('stop');
        stops[0].setAttribute('stop-color', aprobado ? '#34d399' : '#f87171');
        stops[1].setAttribute('stop-color', aprobado ? '#60a5fa' : '#fbbf24');
    }

    const circleFg = document.getElementById('circle-fg');
    circleFg.style.strokeDashoffset = circunferencia;

    // Animación del porcentaje
    setTimeout(() => {
        circleFg.style.strokeDashoffset = offset;
        animarNumero('circle-text', 0, porcentaje, 1200, '%');
    }, 200);
}

function animarNumero(elementId, start, end, duration, suffix = '') {
    const el = document.getElementById(elementId);
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const value = Math.round(start + (end - start) * eased);
        el.textContent = value + suffix;
        if (progress < 1) requestAnimationFrame(update);
    }

    requestAnimationFrame(update);
}

// ===== REVISIÓN =====

function verRevisión() {
    mostrarPantalla('pantalla-revision');

    const contenedor = document.getElementById('revision-body');
    contenedor.innerHTML = '';

    preguntasExamen.forEach((pregunta, i) => {
        const respUsuario = respuestasUsuario[i];
        const esCorrecta = respUsuario === pregunta.correcta;
        const sinResp = respUsuario === -1;

        let clase = 'correcto';
        let badgeClase = 'correcto-badge';
        let badgeTexto = '✓ Correcta';

        if (sinResp) {
            clase = 'sin-resp';
            badgeClase = 'sin-resp-badge';
            badgeTexto = '— Sin responder';
        } else if (!esCorrecta) {
            clase = 'incorrecto';
            badgeClase = 'incorrecto-badge';
            badgeTexto = '✗ Incorrecta';
        }

        const letras = ['A', 'B', 'C', 'D'];
        let opcionesHTML = pregunta.opciones.map((op, j) => {
            let claseOp = '';
            if (j === pregunta.correcta) claseOp = 'correcta';
            else if (j === respUsuario && !esCorrecta) claseOp = 'incorrecta';

            return `<div class="opcion-btn ${claseOp}" style="cursor:default">
                <span class="opcion-letra">${letras[j]}</span>
                <span class="opcion-texto">${op}</span>
            </div>`;
        }).join('');

        // Imagen en revisión
        let imgHTML = '';
        if (pregunta.imagen) {
            imgHTML = `<div class="pregunta-imagen-container"><img src="${pregunta.imagen}" alt="Imagen de la pregunta" class="pregunta-img" onerror="this.parentElement.innerHTML='<div class=\'imagen-placeholder\'>🖼️ Imagen no disponible</div>'"></div>`;
        }

        const item = document.createElement('div');
        item.className = `revision-item ${clase}`;
        item.innerHTML = `
            <div class="revision-q-num">Pregunta ${i + 1}</div>
            <span class="revision-badge ${badgeClase}">${badgeTexto}</span>
            <p class="revision-q-text">${pregunta.pregunta}</p>
            ${imgHTML}
            <div class="opciones-lista">${opcionesHTML}</div>
        `;
        contenedor.appendChild(item);
    });
}

function volverResultados() {
    mostrarPantalla('pantalla-resultados');
}

function reiniciarExamen() {
    iniciarExamen();
}

// ===== UTILIDADES =====

function mostrarPantalla(id) {
    document.querySelectorAll('.pantalla').forEach(p => p.classList.remove('activa'));
    document.getElementById(id).classList.add('activa');
    window.scrollTo(0, 0);
}

// ===== MODO ESTUDIO =====

let filtroActual = 'todas';
let todasReveladas = false;

function mostrarEstudio() {
    mostrarPantalla('pantalla-estudio');
    todasReveladas = false;
    document.getElementById('btn-revelar-todas').classList.remove('activo');
    document.getElementById('btn-revelar-todas').textContent = '👁️ Mostrar todas las respuestas';
    document.getElementById('estudio-search').value = '';
    renderizarEstudio(PREGUNTAS_BANCO);
}

function volverInicio() {
    mostrarPantalla('pantalla-inicio');
}

function renderizarEstudio(preguntas) {
    const contenedor = document.getElementById('estudio-body');
    contenedor.innerHTML = '';

    if (preguntas.length === 0) {
        contenedor.innerHTML = `
            <div class="estudio-sin-resultados">
                <span>🔍</span>
                <p>No se encontraron preguntas</p>
                <small>Intenta con otros términos de búsqueda</small>
            </div>
        `;
        document.getElementById('estudio-counter').textContent = '0 preguntas';
        return;
    }

    document.getElementById('estudio-counter').textContent = `${preguntas.length} pregunta${preguntas.length !== 1 ? 's' : ''}`;

    const letras = ['A', 'B', 'C', 'D'];

    preguntas.forEach((pregunta, idx) => {
        const card = document.createElement('div');
        card.className = 'estudio-card';
        card.dataset.id = pregunta.id;
        card.style.animationDelay = `${Math.min(idx * 30, 600)}ms`;

        // Imagen HTML
        let imgHTML = '';
        if (pregunta.imagen) {
            imgHTML = `<div class="estudio-card-img"><img src="${pregunta.imagen}" alt="Imagen de la pregunta" onerror="this.parentElement.innerHTML='<div class=\\'imagen-placeholder\\'>🖼️ No disponible</div>'"></div>`;
        }

        // Badge
        let badgeHTML = '';
        if (pregunta.imagen) {
            badgeHTML = '<span class="badge-imagen">🖼️ Imagen</span>';
        }

        // Opciones
        const opcionesHTML = pregunta.opciones.map((op, j) => {
            const esCorrecta = j === pregunta.correcta;
            return `<div class="estudio-opcion ${todasReveladas && esCorrecta ? 'es-correcta' : ''}" data-correcta="${esCorrecta}">
                <span class="opcion-letra">${letras[j]}</span>
                <span class="opcion-texto">${op}</span>
            </div>`;
        }).join('');

        card.innerHTML = `
            <div class="estudio-card-header" onclick="toggleEstudioCard(this)">
                <div class="estudio-card-num">${pregunta.id}</div>
                <div class="estudio-card-pregunta">${pregunta.pregunta}</div>
                <div class="estudio-card-badges">${badgeHTML}</div>
                <div class="estudio-card-toggle">
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 5l4 4 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
                </div>
            </div>
            <div class="estudio-card-body">
                ${imgHTML}
                <div class="estudio-opciones">
                    ${opcionesHTML}
                </div>
                <button class="estudio-btn-respuesta" onclick="revelarRespuesta(this, ${pregunta.correcta})" ${todasReveladas ? 'style="display:none"' : ''}>
                    ✨ Mostrar respuesta correcta
                </button>
            </div>
        `;

        contenedor.appendChild(card);
    });
}

function toggleEstudioCard(header) {
    const card = header.closest('.estudio-card');
    card.classList.toggle('abierta');
}

function revelarRespuesta(btn, correctaIdx) {
    const body = btn.closest('.estudio-card-body');
    const opciones = body.querySelectorAll('.estudio-opcion');

    opciones.forEach((op, i) => {
        if (i === correctaIdx) {
            op.classList.add('es-correcta');
        }
    });

    btn.style.display = 'none';
}

function toggleRevelarTodas() {
    todasReveladas = !todasReveladas;
    const btn = document.getElementById('btn-revelar-todas');

    if (todasReveladas) {
        btn.classList.add('activo');
        btn.textContent = '🙈 Ocultar todas las respuestas';

        // Revelar en todas las tarjetas
        document.querySelectorAll('.estudio-card').forEach(card => {
            const opciones = card.querySelectorAll('.estudio-opcion');
            opciones.forEach(op => {
                if (op.dataset.correcta === 'true') {
                    op.classList.add('es-correcta');
                }
            });
            const btnResp = card.querySelector('.estudio-btn-respuesta');
            if (btnResp) btnResp.style.display = 'none';
        });
    } else {
        btn.classList.remove('activo');
        btn.textContent = '👁️ Mostrar todas las respuestas';

        // Ocultar en todas las tarjetas
        document.querySelectorAll('.estudio-card').forEach(card => {
            const opciones = card.querySelectorAll('.estudio-opcion');
            opciones.forEach(op => {
                op.classList.remove('es-correcta');
            });
            const btnResp = card.querySelector('.estudio-btn-respuesta');
            if (btnResp) btnResp.style.display = '';
        });
    }
}

function filtrarEstudio() {
    const query = document.getElementById('estudio-search').value.toLowerCase().trim();
    let preguntas = [...PREGUNTAS_BANCO];

    // Filtro de categoría
    if (filtroActual === 'con-imagen') {
        preguntas = preguntas.filter(p => p.imagen);
    } else if (filtroActual === 'sin-imagen') {
        preguntas = preguntas.filter(p => !p.imagen);
    }

    // Filtro de búsqueda
    if (query) {
        preguntas = preguntas.filter(p => {
            const textoPregunta = p.pregunta.toLowerCase();
            const textoOpciones = p.opciones.join(' ').toLowerCase();
            const textoId = p.id.toString();
            return textoPregunta.includes(query) || textoOpciones.includes(query) || textoId === query;
        });
    }

    renderizarEstudio(preguntas);
}

function filtrarCategoria(categoria, btn) {
    filtroActual = categoria;

    // Actualizar estado visual de los botones
    document.querySelectorAll('.filtro-btn').forEach(b => b.classList.remove('activo'));
    btn.classList.add('activo');

    filtrarEstudio();
}

