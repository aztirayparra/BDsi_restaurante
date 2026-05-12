from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura,DetalleOrden


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
@login_required #proteger el login 
def detalle_plato(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    return render(request, 'gestion/plato_detalle.html', {'plato': plato})



# ── CRUD EMPLEADOS ────────────────────────────
@login_required
def lista_empleados(request):
    query = request.GET.get('q', '')
    empleados = Empleado.objects.all()
    if query:
        empleados = empleados.filter(nombre__icontains=query) | empleados.filter(cargo__icontains=query)
    return render(request, 'gestion/empleados.html', {'empleados': empleados, 'query': query})

@login_required
def detalle_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    return render(request, 'gestion/empleado_detalle.html', {'empleado': empleado})

@login_required
def crear_empleado(request):
    CARGOS = ['Mesero','Mesera','Cajero','Cajera','Administrador']
    if request.method == 'POST':
        Empleado.objects.create(
            nombre=request.POST['nombre'],
            cargo=request.POST['cargo'],
            telefono=request.POST.get('telefono', ''),
            correo=request.POST.get('correo', '') or None,
        )
        messages.success(request, 'Empleado creado.')
        return redirect('lista_empleados')
    return render(request, 'gestion/empleado_form.html', {'titulo': 'Nuevo Empleado', 'cargos': CARGOS})

@login_required
def editar_empleado(request, pk):
    CARGOS = ['Mesero','Mesera','Cajero','Cajera','Administrador']
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.nombre = request.POST['nombre']
        empleado.cargo = request.POST['cargo']
        empleado.telefono = request.POST.get('telefono', '')
        empleado.correo = request.POST.get('correo', '') or None
        empleado.save()
        messages.success(request, 'Empleado actualizado.')
        return redirect('lista_empleados')
    return render(request, 'gestion/empleado_form.html', {'titulo': 'Editar Empleado', 'obj': empleado, 'cargos': CARGOS})

@login_required
def eliminar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado.')
        return redirect('lista_empleados')
    return render(request, 'gestion/confirmar_eliminar.html', {'nombre': empleado.nombre, 'volver': 'lista_empleados'})
# ── CRUD MESAS ────────────────────────────────
@login_required
def lista_mesas(request):
    query = request.GET.get('q', '')
    mesas = Mesa.objects.all()
    if query:
        mesas = mesas.filter(numero_mesa__icontains=query) | mesas.filter(estado_mesa__icontains=query)
    return render(request, 'gestion/mesas.html', {'mesas': mesas, 'query': query})

@login_required
def detalle_mesa(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    return render(request, 'gestion/mesa_detalle.html', {'mesa': mesa})

@login_required
def crear_mesa(request):
    ESTADOS = ['Disponible', 'Ocupada', 'Reservada']
    if request.method == 'POST':
        Mesa.objects.create(
            numero_mesa=request.POST['numero_mesa'],
            capacidad=request.POST['capacidad'],
            estado_mesa=request.POST['estado_mesa'],
        )
        messages.success(request, 'Mesa creada.')
        return redirect('lista_mesas')
    return render(request, 'gestion/mesa_form.html', {'titulo': 'Nueva Mesa', 'estados': ESTADOS})

@login_required
def editar_mesa(request, pk):
    ESTADOS = ['Disponible', 'Ocupada', 'Reservada']
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        mesa.numero_mesa = request.POST['numero_mesa']
        mesa.capacidad = request.POST['capacidad']
        mesa.estado_mesa = request.POST['estado_mesa']
        mesa.save()
        messages.success(request, 'Mesa actualizada.')
        return redirect('lista_mesas')
    return render(request, 'gestion/mesa_form.html', {'titulo': 'Editar Mesa', 'obj': mesa, 'estados': ESTADOS})

@login_required
def eliminar_mesa(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        mesa.delete()
        messages.success(request, 'Mesa eliminada.')
        return redirect('lista_mesas')
    return render(request, 'gestion/confirmar_eliminar.html', {'nombre': f'Mesa {mesa.numero_mesa}', 'volver': 'lista_mesas'})

# ── CRUD ÓRDENES ──────────────────────────────
@login_required
def lista_ordenes(request):
    query = request.GET.get('q', '')
    ordenes = Orden.objects.select_related('cliente', 'empleado', 'mesa').all()
    if query:
        ordenes = ordenes.filter(cliente__nombre__icontains=query) | ordenes.filter(estado_orden__icontains=query)
    return render(request, 'gestion/ordenes.html', {'ordenes': ordenes, 'query': query})

@login_required
def detalle_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    detalles = orden.detalles.select_related('plato').all()
    platos = Plato.objects.filter(disponible=True)
    return render(request, 'gestion/orden_detalle.html', {
        'orden': orden,
        'detalles': detalles,
        'platos': platos,
    })
@login_required
def crear_orden(request):
    ESTADOS = ['Activa', 'En preparación', 'Entregada', 'Facturada', 'Cancelada']
    if request.method == 'POST':
        orden = Orden.objects.create(
            cliente=get_object_or_404(Cliente, pk=request.POST['cliente']),
            empleado=get_object_or_404(Empleado, pk=request.POST['empleado']),
            mesa=get_object_or_404(Mesa, pk=request.POST['mesa']),
            estado_orden='Activa',
        )
        messages.success(request, 'Orden creada. Ahora agrega los platos.')
        return redirect('agregar_platos_orden', pk=orden.pk)
    return render(request, 'gestion/orden_form.html', {
        'titulo': 'Nueva Orden',
        'clientes': Cliente.objects.all(),
        'empleados': Empleado.objects.all(),
        'mesas': Mesa.objects.all(),
        'estados': ESTADOS,
    })

@login_required
def editar_orden(request, pk):
    ESTADOS = ['Activa', 'En preparación', 'Entregada', 'Facturada', 'Cancelada']
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        orden.cliente = get_object_or_404(Cliente, pk=request.POST['cliente'])
        orden.empleado = get_object_or_404(Empleado, pk=request.POST['empleado'])
        orden.mesa = get_object_or_404(Mesa, pk=request.POST['mesa'])
        orden.estado_orden = request.POST['estado_orden']
        orden.save()
        messages.success(request, 'Orden actualizada.')
        return redirect('lista_ordenes')
    return render(request, 'gestion/orden_form.html', {
        'titulo': 'Editar Orden',
        'obj': orden,
        'clientes': Cliente.objects.all(),
        'empleados': Empleado.objects.all(),
        'mesas': Mesa.objects.all(),
        'estados': ESTADOS,
    })

@login_required
def eliminar_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        orden.delete()
        messages.success(request, 'Orden eliminada.')
        return redirect('lista_ordenes')
    return render(request, 'gestion/confirmar_eliminar.html', {'nombre': f'Orden #{orden.id}', 'volver': 'lista_ordenes'})

# ── CRUD FACTURAS ─────────────────────────────
@login_required
def lista_facturas(request):
    query = request.GET.get('q', '')
    facturas = Factura.objects.select_related('orden', 'orden__cliente').all()
    if query:
        facturas = facturas.filter(orden__cliente__nombre__icontains=query) | facturas.filter(metodo_pago__icontains=query)
    return render(request, 'gestion/facturas.html', {'facturas': facturas, 'query': query})

@login_required
def detalle_factura(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    return render(request, 'gestion/factura_detalle.html', {'factura': factura})

@login_required
def crear_factura(request):
    METODOS = ['Efectivo', 'Tarjeta', 'Transferencia', 'Nequi', 'Daviplata']
    ordenes_disponibles = Orden.objects.filter(estado_orden='Entregada').exclude(factura__isnull=False)
    if request.method == 'POST':
        orden = get_object_or_404(Orden, pk=request.POST['orden'])
        subtotal = orden.total
        impuesto = round(subtotal * Decimal('0.08'), 2)
        total_factura = subtotal + impuesto
        Factura.objects.create(
            orden=orden,
            subtotal=subtotal,
            impuesto=impuesto,
            total_factura=total_factura,
            metodo_pago=request.POST['metodo_pago'],
        )
        orden.estado_orden = 'Facturada'
        orden.save()
        messages.success(request, 'Factura creada.')
        return redirect('lista_facturas')
    return render(request, 'gestion/factura_form.html', {
        'titulo': 'Nueva Factura',
        'ordenes': ordenes_disponibles,
        'metodos': METODOS,
    })

@login_required
def editar_factura(request, pk):
    METODOS = ['Efectivo', 'Tarjeta', 'Transferencia', 'Nequi', 'Daviplata']
    factura = get_object_or_404(Factura, pk=pk)
    if request.method == 'POST':
        factura.metodo_pago = request.POST['metodo_pago']
        factura.save()
        messages.success(request, 'Factura actualizada.')
        return redirect('lista_facturas')
    return render(request, 'gestion/factura_form.html', {
        'titulo': 'Editar Factura',
        'obj': factura,
        'metodos': METODOS,
    })

@login_required
def eliminar_factura(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    if request.method == 'POST':
        factura.delete()
        messages.success(request, 'Factura eliminada.')
        return redirect('lista_facturas')
    return render(request, 'gestion/confirmar_eliminar.html', {'nombre': f'Factura #{factura.id}', 'volver': 'lista_facturas'})

# ── DETALLE ORDEN (agregar/quitar platos) ─────
@login_required
def agregar_platos_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    platos = Plato.objects.filter(disponible=True)
    if request.method == 'POST':
        if 'finalizar' in request.POST:
            if orden.detalles.count() == 0:
                messages.error(request, 'Debes agregar al menos un plato.')
            else:
                messages.success(request, f'Orden #{orden.id} finalizada con {orden.detalles.count()} plato(s).')
                return redirect('lista_ordenes')
        else:
            plato = get_object_or_404(Plato, pk=request.POST['plato'])
            cantidad = int(request.POST.get('cantidad', 1))
            detalle_existente = orden.detalles.filter(plato=plato).first()
            if detalle_existente:
                detalle_existente.cantidad += cantidad
                detalle_existente.save()
            else:
                DetalleOrden.objects.create(orden=orden, plato=plato, cantidad=cantidad)
            messages.success(request, f'"{plato.nombre_plato}" agregado.')
    detalles = orden.detalles.select_related('plato').all()
    return render(request, 'gestion/orden_agregar_platos.html', {
        'orden': orden,
        'platos': platos,
        'detalles': detalles,
    })

@login_required
def eliminar_plato_orden(request, detalle_pk):
    detalle = get_object_or_404(DetalleOrden, pk=detalle_pk)
    orden_pk = detalle.orden.pk
    detalle.delete()
    messages.success(request, 'Plato eliminado.')
    return redirect('agregar_platos_orden', pk=orden_pk)

@login_required
def facturar_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    METODOS = ['Efectivo', 'Tarjeta', 'Transferencia', 'Nequi', 'Daviplata']
    if orden.estado_orden == 'Facturada':
        messages.error(request, 'Esta orden ya fue facturada.')
        return redirect('lista_ordenes')
    if orden.detalles.count() == 0:
        messages.error(request, 'No puedes facturar una orden sin platos.')
        return redirect('lista_ordenes')
    if request.method == 'POST':
        subtotal = orden.total
        impuesto = round(subtotal * Decimal('0.08'), 2)
        total_factura = subtotal + impuesto
        Factura.objects.create(
            orden=orden,
            subtotal=subtotal,
            impuesto=impuesto,
            total_factura=total_factura,
            metodo_pago=request.POST['metodo_pago'],
        )
        orden.estado_orden = 'Facturada'
        orden.save()
        messages.success(request, f'Orden #{orden.id} facturada exitosamente.')
        return redirect('lista_facturas')
    return render(request, 'gestion/facturar_orden.html', {
        'orden': orden,
        'metodos': METODOS,
    })