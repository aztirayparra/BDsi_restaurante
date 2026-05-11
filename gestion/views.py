from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura


# ── AUTH ──────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('inicio')
        messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'gestion/login.html', {'form': form})


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada. Inicia sesión.')
            return redirect('login')
        messages.error(request, 'Corrige los errores.')
    else:
        form = UserCreationForm()
    return render(request, 'gestion/registro.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ── DASHBOARD ─────────────────────────────────
@login_required
def inicio(request):
    context = {
        'total_cliente': Cliente.objects.count(),
        'total_empleados': Empleado.objects.count(),
        'total_mesas': Mesa.objects.count(),
        'total_platos': Plato.objects.count(),
        'total_ordenes': Orden.objects.count(),
        'total_facturas': Factura.objects.count(),
    }
    return render(request, 'gestion/inicio.html', context)


# ── LISTAS ────────────────────────────────────
@login_required
def lista_clientes(request):
    query = request.GET.get('q', '')
    clientes = Cliente.objects.all()
    if query:
        clientes = clientes.filter(
            nombre__icontains=query
        ) | clientes.filter(
            telefono__icontains=query
        ) | clientes.filter(
            correo__icontains=query
        )
    return render(request, 'gestion/clientes.html', {'clientes': clientes, 'query': query})

@login_required
def lista_empleados(request):
    return render(request, 'gestion/empleados.html', {'empleados': Empleado.objects.all()})

@login_required
def lista_mesas(request):
    return render(request, 'gestion/mesas.html', {'mesas': Mesa.objects.all()})

@login_required
def lista_platos(request):
    query = request.GET.get('q', '')
    platos = Plato.objects.all()
    if query:
        platos = platos.filter(
            nombre_plato__icontains=query
        ) | platos.filter(
            categoria__icontains=query
        )
    return render(request, 'gestion/platos.html', {'platos': platos, 'query': query})

@login_required
def lista_ordenes(request):
    return render(request, 'gestion/ordenes.html', {'ordenes': Orden.objects.all()})

@login_required
def lista_facturas(request):
    return render(request, 'gestion/facturas.html', {'facturas': Factura.objects.all()})


# ── CRUD CLIENTES ─────────────────────────────
@login_required
def crear_cliente(request):
    if request.method == 'POST':
        Cliente.objects.create(
            nombre=request.POST['nombre'],
            telefono=request.POST.get('telefono', ''),
            correo=request.POST.get('correo', '') or None,
        )
        messages.success(request, 'Cliente creado.')
        return redirect('lista_clientes')
    return render(request, 'gestion/cliente_form.html', {'titulo': 'Nuevo Cliente'})

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.telefono = request.POST.get('telefono', '')
        cliente.correo = request.POST.get('correo', '') or None
        cliente.save()
        messages.success(request, 'Cliente actualizado.')
        return redirect('lista_clientes')
    return render(request, 'gestion/cliente_form.html', {'titulo': 'Editar Cliente', 'obj': cliente})

@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado.')
        return redirect('lista_clientes')
    return render(request, 'gestion/confirmar_eliminar.html', {'obj': cliente, 'nombre': cliente.nombre, 'volver': 'lista_clientes'})

@login_required
def detalle_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'gestion/cliente_detalle.html', {'cliente': cliente})

# ── CRUD PLATOS ───────────────────────────────
@login_required
def crear_plato(request):
    if request.method == 'POST':
        Plato.objects.create(
            nombre_plato=request.POST['nombre_plato'],
            descripcion=request.POST.get('descripcion', ''),
            precio=request.POST['precio'],
            categoria=request.POST.get('categoria', ''),
            disponible='disponible' in request.POST,
        )
        messages.success(request, 'Plato creado.')
        return redirect('lista_platos')
    return render(request, 'gestion/plato_form.html', {'titulo': 'Nuevo Plato'})

@login_required
def editar_plato(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == 'POST':
        plato.nombre_plato = request.POST['nombre_plato']
        plato.descripcion = request.POST.get('descripcion', '')
        plato.precio = request.POST['precio']
        plato.categoria = request.POST.get('categoria', '')
        plato.disponible = 'disponible' in request.POST
        plato.save()
        messages.success(request, 'Plato actualizado.')
        return redirect('lista_platos')
    return render(request, 'gestion/plato_form.html', {'titulo': 'Editar Plato', 'obj': plato})

@login_required
def eliminar_plato(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == 'POST':
        plato.delete()
        messages.success(request, 'Plato eliminado.')
        return redirect('lista_platos')
    return render(request, 'gestion/confirmar_eliminar.html', {'obj': plato, 'nombre': plato.nombre_plato, 'volver': 'lista_platos'})
@login_required
def detalle_plato(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    return render(request, 'gestion/plato_detalle.html', {'plato': plato})