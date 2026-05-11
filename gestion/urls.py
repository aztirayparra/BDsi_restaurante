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
]