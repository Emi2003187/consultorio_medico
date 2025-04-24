from django.urls import path
from .views import CustomLoginView, DashboardMedico, DashboardAsistente, DashboardAdmin, RegistroUsuarioView, UsuarioCreateView, UsuarioDeleteView, UsuarioListView, UsuarioUpdateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Dashboards por rol
    path('medico/dashboard/', DashboardMedico.as_view(), name='dashboard_medico'),
    path('asistente/dashboard/', DashboardAsistente.as_view(), name='dashboard_asistente'),
    path('adm/dashboard/', DashboardAdmin.as_view(), name='dashboard_admin'),


    ##ADMIN USUARIOS CRUDS
    path('adm/usuarios/', UsuarioListView.as_view(), name='usuarios_lista'),
    path('adm/usuarios/crear/', UsuarioCreateView.as_view(), name='usuarios_crear'),
    path('adm/usuarios/<int:pk>/editar/', UsuarioUpdateView.as_view(), name='usuarios_editar'),
    path('adm/usuarios/<int:pk>/eliminar/', UsuarioDeleteView.as_view(), name='usuarios_eliminar'),
]
