from django.urls import path, include, re_path
from . import views
from .views import agregarfoto
#from .views import ContratosList
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView

# router = routers.DefaultRouter()
# router.register(r'contratos', views.ContratosList)

router = routers.DefaultRouter()
router.register(r'subirfotos', views.agregarfoto)

urlpatterns = [
    # path('', views.index, name='index'),
    # path('interacciones', views.interaccionesss, name='interacciones'),
    # path('editarcontrato/<str:contrato_id>/', views.editarcontrato, name='editarcontrato'),
    # path('eliminarusuario/<int:cedula_id>/', views.eliminarusuario, name='eliminarusuario'),
    # path('eliminarhorario/<int:id_web>', views.eliminarhorario, name='eliminarhorario'),
    # path('editarusuario/<int:cedula_id>', views.editarusuario, name='editarusuario'),
    # path('agregarcontrato', views.agregarcontrato, name='agregarcontrato'),
    # path('eliminarcontrato/<str:contrato_id>/', views.eliminarcontrato, name='eliminarcontrato'),
    # path('editarcontrato', views.seleccionarcontrato, name='seleccionarcontrato'),
    # path('eliminarfoto/<int:cedula_id>/', views.eliminarfoto, name='eliminarfoto'),
    path('api', include(router.urls)),
    #re_path(r'^contratos/$', views.seleccionarcontratoapi),
    #re_path(r'^editarcontratoapi/(?P<contrato_id>\w+)$', views.editarcontratoapi),
    re_path(r'^agregarcontratosapi/$', views.agregarcontratosapi),
    #re_path(r'^removercontratosapi/(?P<contrato_id>[\w\s]+)/$', views.eliminarcontratos),
    #re_path(r'^removercontratosapi/(?P<contrato_id>.*)/$', views.eliminarcontratos),
    re_path(r'^removercontratosapi/(?P<contrato_id>[\w\ ]+)/$', views.eliminarcontratos),
    re_path(r'^seleccionarcontratoapi/(?P<contrato_id>[\w\ ]+)/$', views.seleccionarcontratoapi),
    re_path(r'^editcontrato/agregarusuario/$', views.agregarusuarioapi),
    re_path(r'^editcontrato/eliminarusuario/(?P<cedula_id>[\w\ ]+)/$', views.eliminarusuarioapi),
    re_path(r'^editcontrato/buscarusuario/(?P<cedula_id>[\w\ ]+)/$', views.buscarusuarioapi),
    re_path(r'^editusuario/horarios/(?P<cedula_id>[\w\ ]+)/$', views.editarhorariosapi),
    re_path(r'^editusuario/foto/(?P<cedula_id>[\w\ ]+)/$', views.editarfotosapi),
    re_path(r'^actividad/$', views.interaccionesapi),
    re_path(r'^(?P<path>.*)/$', views.index),
]   