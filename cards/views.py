from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin
from django.utils.safestring import mark_safe
from .models import Comentario

# ── Página de inicio ──────────────────────────────────────────
def index(request):
    return render(request, 'cards/index.html')


# ══════════════════════════════════════════════════════════════
# 1. CSRF
# ══════════════════════════════════════════════════════════════

def csrf_seguro(request):
    """Formulario CON protección CSRF (comportamiento por defecto de Django)."""
    mensaje = None
    if request.method == 'POST':
        autor = request.POST.get('autor', '')
        contenido = request.POST.get('contenido', '')
        Comentario.objects.create(carta='CSRF-Seguro', autor=autor, contenido=contenido)
        mensaje = '✅ Comentario guardado con protección CSRF.'
    comentarios = Comentario.objects.filter(carta='CSRF-Seguro').order_by('-creado_en')
    return render(request, 'cards/csrf_seguro.html', {'comentarios': comentarios, 'mensaje': mensaje})


@csrf_exempt   # ← VULNERABILIDAD intencional para la demo
def csrf_vulnerable(request):
    """Formulario SIN protección CSRF."""
    mensaje = None
    if request.method == 'POST':
        autor = request.POST.get('autor', '')
        contenido = request.POST.get('contenido', '')
        Comentario.objects.create(carta='CSRF-Vulnerable', autor=autor, contenido=contenido)
        mensaje = '⚠️ Comentario guardado SIN protección CSRF.'
    comentarios = Comentario.objects.filter(carta='CSRF-Vulnerable').order_by('-creado_en')
    return render(request, 'cards/csrf_vulnerable.html', {'comentarios': comentarios, 'mensaje': mensaje})


def csrf_ataque(request):
    """Página que simula un sitio externo que hace POST al endpoint vulnerable."""
    return render(request, 'cards/csrf_ataque.html')


# ══════════════════════════════════════════════════════════════
# 2. XSS
# ══════════════════════════════════════════════════════════════

def xss_seguro(request):
    """Muestra comentarios escapando el HTML (Django lo hace por defecto en templates)."""
    mensaje = None
    if request.method == 'POST':
        autor = request.POST.get('autor', '')
        contenido = request.POST.get('contenido', '')
        Comentario.objects.create(carta='XSS-Seguro', autor=autor, contenido=contenido)
        mensaje = '✅ Comentario guardado con escape de HTML.'
    comentarios = Comentario.objects.filter(carta='XSS-Seguro').order_by('-creado_en')
    return render(request, 'cards/xss_seguro.html', {'comentarios': comentarios, 'mensaje': mensaje})


def xss_vulnerable(request):
    """Muestra comentarios con mark_safe → renderiza HTML sin escapar (VULNERABLE)."""
    mensaje = None
    if request.method == 'POST':
        autor = request.POST.get('autor', '')
        contenido = request.POST.get('contenido', '')
        Comentario.objects.create(carta='XSS-Vulnerable', autor=autor, contenido=contenido)
        mensaje = '⚠️ Comentario guardado sin sanitizar.'
    comentarios = Comentario.objects.filter(carta='XSS-Vulnerable').order_by('-creado_en')
    # mark_safe hace que Django NO escape el contenido al renderizar
    comentarios_unsafe = [
        {'autor': c.autor, 'contenido': mark_safe(c.contenido), 'creado_en': c.creado_en}
        for c in comentarios
    ]
    return render(request, 'cards/xss_vulnerable.html', {'comentarios': comentarios_unsafe, 'mensaje': mensaje})


# ══════════════════════════════════════════════════════════════
# 3. Clickjacking
# ══════════════════════════════════════════════════════════════

def clickjacking_seguro(request):
    """Página protegida contra iframes (X-Frame-Options: DENY por defecto)."""
    return render(request, 'cards/clickjacking_seguro.html')


@xframe_options_exempt   # ← VULNERABILIDAD intencional
def clickjacking_vulnerable(request):
    """Página que SÍ puede incrustarse en un iframe."""
    return render(request, 'cards/clickjacking_vulnerable.html')


def clickjacking_ataque(request):
    """Página que intenta incrustar ambas vistas en iframes para comparar."""
    return render(request, 'cards/clickjacking_ataque.html')