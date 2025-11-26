"""
URL configuration for Aula_Django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from meu_site.views import (
    IndexTemplateView,
    CatalogoListView,
    UsuarioCreateView,
    UpdateUsu,
    DeleteUsu,
    ProdutoListView,
    ProdutoCreateView,
    LoginVendedorView,
    cadastrar,
    detalhe_produto,
    ProdutoUpdateView,
    ProdutoDeleteView,
    login_usuario,
    esqueceu_senha,
)

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexTemplateView.as_view(), name='home'),

    path('add_usu/', UsuarioCreateView.as_view(), name='novo_usuario'),
    path('edit_usuario/<int:pk>/', UpdateUsu.as_view(), name='editar_usuario'),
    path('delete_usuario/<int:pk>/', DeleteUsu.as_view(), name='remover_usuario'),

    path('produtos/', ProdutoListView.as_view(), name='produtos'),
    path('add_produto/', ProdutoCreateView.as_view(), name='novo_produto'),
    path('catalogo/', CatalogoListView.as_view(), name='catalogo'),

    path('produtos/<int:pk>/', detalhe_produto, name='detalhe_produto'),

    #login do usuario normal
    path('login/', login_usuario, name='login_usuario'),
    path('cadastrar/', cadastrar, name='cadastrar'),
    path('esqueceu-senha/', esqueceu_senha, name='esqueceu_senha'),

    path('vendedor/login/', LoginVendedorView.as_view(), name='vendedor_login'),
    # path('vendedor/cadastrar/', CadastroVendedorView.as_view(), name='vendedor_cadastrar'),
    path('produtos/<int:pk>/editar/', ProdutoUpdateView.as_view(), name='editar_produto'),
    path('produtos/<int:pk>/deletar/', ProdutoDeleteView.as_view(), name='delete_produto'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
