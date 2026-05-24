from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('inicio/', views.inicio, name='inicio'),

    # Listas
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('empleados/', views.lista_empleados, name='lista_empleados'),
    path('mesas/', views.lista_mesas, name='lista_mesas'),
    path('platos/', views.lista_platos, name='lista_platos'),
    path('ordenes/', views.lista_ordenes, name='lista_ordenes'),
    path('facturas/', views.lista_facturas, name='lista_facturas'),

    # CRUD Clientes
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:pk>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:pk>/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),
    path('clientes/<int:pk>/', views.detalle_cliente, name='detalle_cliente'),

    # CRUD Platos
    path('platos/nuevo/', views.crear_plato, name='crear_plato'),
    path('platos/<int:pk>/editar/', views.editar_plato, name='editar_plato'),
    path('platos/<int:pk>/eliminar/', views.eliminar_plato, name='eliminar_plato'),
    path('platos/<int:pk>/', views.detalle_plato, name='detalle_plato'),
    
    # CRUD Empleados
    path('empleados/', views.lista_empleados, name='lista_empleados'),
    path('empleados/nuevo/', views.crear_empleado, name='crear_empleado'),
    path('empleados/<int:pk>/', views.detalle_empleado, name='detalle_empleado'),
    path('empleados/<int:pk>/editar/', views.editar_empleado, name='editar_empleado'),
    path('empleados/<int:pk>/eliminar/', views.eliminar_empleado, name='eliminar_empleado'),
    
    # CRUD Mesas
    path('mesas/', views.lista_mesas, name='lista_mesas'),
    path('mesas/nueva/', views.crear_mesa, name='crear_mesa'),
    path('mesas/<int:pk>/', views.detalle_mesa, name='detalle_mesa'),
    path('mesas/<int:pk>/editar/', views.editar_mesa, name='editar_mesa'),
    path('mesas/<int:pk>/eliminar/', views.eliminar_mesa, name='eliminar_mesa'),

  # CRUD Ordenes
    path('ordenes/', views.lista_ordenes, name='lista_ordenes'),
    path('ordenes/nueva/', views.crear_orden, name='crear_orden'),
    path('ordenes/<int:pk>/', views.detalle_orden, name='detalle_orden'),
    path('ordenes/<int:pk>/platos/', views.agregar_platos_orden, name='agregar_platos_orden'),
    path('ordenes/<int:pk>/editar/', views.editar_orden, name='editar_orden'),
    path('ordenes/<int:pk>/eliminar/', views.eliminar_orden, name='eliminar_orden'),
    path('ordenes/<int:pk>/facturar/', views.facturar_orden, name='facturar_orden'),
    path('ordenes/detalle/<int:detalle_pk>/eliminar/', views.eliminar_plato_orden, name='eliminar_plato_orden'),

    # CRUD Facturas
    path('facturas/', views.lista_facturas, name='lista_facturas'),
    path('facturas/nueva/', views.crear_factura, name='crear_factura'),
    path('facturas/<int:pk>/', views.detalle_factura, name='detalle_factura'),
    path('facturas/<int:pk>/editar/', views.editar_factura, name='editar_factura'),
    path('facturas/<int:pk>/eliminar/', views.eliminar_factura, name='eliminar_factura'),

 # Gestión usuarios
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/<int:user_id>/rol/', views.cambiar_rol, name='cambiar_rol'),   
    
    
]