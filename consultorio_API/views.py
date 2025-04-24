##VIEWS FRONT DIRECTO
from django.contrib.auth.views import LoginView
from .forms import EditarUsuarioForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import RegistroUsuarioForm
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Usuario
from .forms import RegistroUsuarioForm, EditarUsuarioForm 

class RegistroUsuarioView(CreateView):
    form_class = RegistroUsuarioForm
    template_name = 'PAGES/registro.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.rol = 'medico'  
        user.save()
        return super().form_valid(form)


from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

class CustomLoginView(LoginView):
    template_name = "PAGES/login.html"
    authentication_form = LoginForm

    def form_valid(self, form):
        """
        Después de autenticar verificamos si el usuario tiene consultorio.
        Los admin pasan siempre; médicos/asistentes deben estar asignados.
        """
        response = super().form_valid(form)
        user = self.request.user

        if user.rol in ("medico", "asistente") and user.consultorio is None:
            # Forzamos logout y mostramos aviso
            logout(self.request)
            messages.error(
                self.request,
                "Cuenta aún no dada de alta. "
                "Un administrador debe asignarte a un consultorio."
            )
            return redirect(reverse("login"))

        return response

    def get_success_url(self):
        user = self.request.user
        if user.rol == "medico":
            return "/medico/dashboard/"
        elif user.rol == "asistente":
            return "/asistente/dashboard/"
        elif user.rol == "admin":
            return "/adm/dashboard/"
        return "/"



@method_decorator(login_required, name='dispatch')
class DashboardMedico(View):
    def get(self, request):
        return render(request, 'PAGES/dashboard.html', {
            'usuario': request.user,
            'rol': 'Médico'
        })

@method_decorator(login_required, name='dispatch')
class DashboardAsistente(View):
    def get(self, request):
        return render(request, 'PAGES/dashboard.html', {
            'usuario': request.user,
            'rol': 'Asistente'
        })

@method_decorator(login_required, name='dispatch')
class DashboardAdmin(View):
    def get(self, request):
        return render(request, 'PAGES/dashboard.html', {
            'usuario': request.user,
            'rol': 'Administrador'
        })


##CRUD ADMINS
# SOLO ADMINS CABRONES
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol == 'admin'


# Lista de usuarios (excepto admins)
class UsuarioListView(AdminRequiredMixin, ListView):
    model = Usuario
    template_name = 'PAGES/usuarios/lista.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        return Usuario.objects.exclude(rol='admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user  
        return context



# Crear usuario (médico o asistente)
class UsuarioCreateView(AdminRequiredMixin, CreateView):
    model = Usuario
    form_class = RegistroUsuarioForm
    template_name = 'PAGES/usuarios/crear.html'
    success_url = reverse_lazy('usuarios_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user  
        return context


# Editar usuario
class UsuarioUpdateView(AdminRequiredMixin, UpdateView):
    model = Usuario
    form_class = EditarUsuarioForm 
    template_name = 'PAGES/usuarios/editar.html'
    success_url = reverse_lazy('usuarios_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user  # Para navbar/sidebar
        return context


# Eliminar usuario
class UsuarioDeleteView(AdminRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'PAGES/usuarios/eliminar.html'
    success_url = reverse_lazy('usuarios_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context



##VIEWS PARA LAS APIS
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import UsuarioSerializer

class LoginAPI(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if "token" not in response.data:
            return response       

        token = Token.objects.get(key=response.data["token"])
        user  = token.user

        if user.rol in ("medico", "asistente") and user.consultorio is None:
            token.delete()          
            return Response(
                {"error": "Cuenta aún no dada de alta; falta asignar consultorio."},
                status=403
            )

        return Response({
            "token": token.key,
            "user":  UsuarioSerializer(user).data
        })

