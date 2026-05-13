# 🔐 Django Security Demo

Proyecto educativo desarrollado en **Python + Django** que demuestra de forma práctica tres vulnerabilidades de seguridad web comunes, mostrando tanto el comportamiento vulnerable como la protección que ofrece Django.

---

## 📚 Vulnerabilidades cubiertas

| # | Vulnerabilidad | Descripción |
|---|---------------|-------------|
| 1 | **CSRF** | Cross-Site Request Forgery — falsificación de solicitudes entre sitios |
| 2 | **XSS** | Cross-Site Scripting — inyección de scripts maliciosos |
| 3 | **Clickjacking** | Engaño al usuario mediante iframes superpuestos |

Cada vulnerabilidad tiene su propia sección con:
- ✅ Página **segura** (con protección activa)
- ⚠️ Página **vulnerable** (protección desactivada intencionalmente)
- 🎭 Página de **ataque simulado** (para CSRF y Clickjacking)

---

## 🗂️ Estructura del proyecto

```
security_demo/
├── manage.py
├── security_demo/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── cards/
    ├── models.py
    ├── views.py
    ├── urls.py
    └── templates/
        └── cards/
            ├── base.html
            ├── index.html
            ├── csrf_seguro.html
            ├── csrf_vulnerable.html
            ├── csrf_ataque.html
            ├── xss_seguro.html
            ├── xss_vulnerable.html
            ├── clickjacking_seguro.html
            ├── clickjacking_vulnerable.html
            └── clickjacking_ataque.html
```

---

## ⚙️ Instalación y ejecución

### Prerrequisitos

- Python 3.10 o superior
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/security_demo.git
cd security_demo

# 2. Instalar dependencias
pip install django

# 3. Aplicar migraciones (crea la base de datos SQLite)
python manage.py migrate

# 4. Levantar el servidor de desarrollo
python manage.py runserver
```

Accedé desde el navegador a: **http://127.0.0.1:8000**

---

## 🗺️ Rutas disponibles

| URL | Descripción |
|-----|-------------|
| `/` | Página de inicio |
| `/csrf/seguro/` | Formulario con token CSRF válido |
| `/csrf/vulnerable/` | Formulario sin validación CSRF (`@csrf_exempt`) |
| `/csrf/ataque/` | Simula un sitio externo enviando POST al endpoint vulnerable |
| `/xss/seguro/` | Comentarios con escape automático de HTML |
| `/xss/vulnerable/` | Comentarios renderizados con `mark_safe()` sin sanitizar |
| `/clickjacking/seguro/` | Página con `X-Frame-Options: DENY` |
| `/clickjacking/vulnerable/` | Página con `@xframe_options_exempt` |
| `/clickjacking/ataque/` | Comparación visual de ambas páginas en iframes |

---

## 🔍 Explicación de cada vulnerabilidad

### 1. CSRF (Cross-Site Request Forgery)

**¿Qué es?** Un atacante engaña al usuario para que, sin saberlo, envíe una solicitud maliciosa a un sitio donde ya está autenticado.

**Demo vulnerable:** El endpoint usa `@csrf_exempt`, por lo que acepta POST de cualquier origen sin verificar la identidad del remitente.

**Demo segura:** Django incluye `{% csrf_token %}` en el formulario. Si el token no coincide, la solicitud es rechazada con error 403.

**Protección en Django:**
```python
# settings.py — activo por defecto
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
]

# En el template
<form method="post">
    {% csrf_token %}
    ...
</form>
```

---

### 2. XSS (Cross-Site Scripting)

**¿Qué es?** Un atacante inyecta código JavaScript malicioso en el contenido de la página, que luego se ejecuta en el navegador de otros usuarios.

**Payload de prueba:**
```html
<script>alert('XSS ejecutado!')</script>
```

**Demo vulnerable:** La vista usa `mark_safe()`, lo que le indica a Django que confíe ciegamente en el contenido sin escaparlo.

**Demo segura:** Django escapa automáticamente el HTML en los templates (`{{ variable }}` convierte `<script>` en `&lt;script&gt;`).

**Protección en Django:**
```python
# Django escapa por defecto — nunca usar mark_safe() con input del usuario
{{ comentario.contenido }}        # ✅ seguro
{{ comentario.contenido|safe }}   # ⚠️ vulnerable
```

---

### 3. Clickjacking

**¿Qué es?** Un atacante incrusta la página víctima en un iframe invisible o semitransparente para engañar al usuario y hacer que haga clic en elementos sin saberlo.

**Demo vulnerable:** El decorador `@xframe_options_exempt` elimina el header de protección, permitiendo que la página sea incrustada en cualquier iframe.

**Demo segura:** El middleware agrega automáticamente `X-Frame-Options: DENY`, y el navegador bloquea la carga del iframe.

**Protección en Django:**
```python
# settings.py
X_FRAME_OPTIONS = 'DENY'  # o 'SAMEORIGIN'

MIDDLEWARE = [
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

---

## 🛡️ Resumen de mecanismos de protección de Django

| Vulnerabilidad | Mecanismo | Dónde se configura |
|---------------|-----------|-------------------|
| CSRF | `CsrfViewMiddleware` + `{% csrf_token %}` | `settings.py` + templates |
| XSS | Auto-escape en templates | Comportamiento por defecto |
| Clickjacking | `XFrameOptionsMiddleware` + `X_FRAME_OPTIONS` | `settings.py` |

---

## ⚠️ Advertencia

Este proyecto fue creado con **fines exclusivamente educativos**. Las páginas marcadas como "vulnerables" tienen protecciones desactivadas intencionalmente para demostrar los ataques. **No usar este código en producción.**

---

## 🛠️ Tecnologías

- [Python 3](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- SQLite (base de datos por defecto de Django)

---

## 📄 Licencia

MIT — libre uso con fines educativos.
