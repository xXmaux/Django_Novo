from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password, check_password
from .forms import ProdutoForms, CaracteristicaFormSet, EspecificacaoFormSet
from django.views import View
from django.contrib.auth import authenticate, login
from .forms import UsuarioForms, ProdutoForms
from .models import Usuario, Produto, Categoria
from django.contrib.auth.models import User as AuthUser
from django.db import IntegrityError


class IndexTemplateView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categorias_nomes = ['Eletrônicos', 'Moda', 'Casa & Decor', 'Presentes']
        context['categorias_principais'] = Categoria.objects.filter(nome__in=categorias_nomes)
        return context


class CatalogoListView(ListView):
    model = Produto
    template_name = 'catalogo.html'
    context_object_name = 'produtos'
    extra_context = {'form_titulo': 'Catálogo de Produtos'}

    def get_queryset(self):
        queryset = Produto.objects.all()
        busca = self.request.GET.get('q', '').strip()

        if busca:
            queryset = queryset.filter(nome__icontains=busca)

        categoria_id = self.request.GET.get('categoria', '').strip()
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)

        preco_min = self.request.GET.get('preco_min', '').strip()
        if preco_min:
            try:
                queryset = queryset.filter(preco__gte=float(preco_min))
            except ValueError:
                pass

        preco_max = self.request.GET.get('preco_max', '').strip()
        if preco_max:
            try:
                queryset = queryset.filter(preco__lte=float(preco_max))
            except ValueError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context


class UsuarioCreateView(CreateView):
    form_class = UsuarioForms
    template_name = 'formulario.html'
    extra_context = {'form_titulo': 'Cadastro Usuário'}
    success_url = reverse_lazy('alunos')


class UpdateUsu(UpdateView):
    model = Usuario
    form_class = UsuarioForms
    template_name = 'formulario.html'
    extra_context = {'form_titulo': 'Editar Usuário'}
    success_url = reverse_lazy('alunos')


class DeleteUsu(DeleteView):
    model = Usuario
    template_name = 'excluir_registro.html'
    success_url = reverse_lazy('alunos')
    context_object_name = 'registro'
    extra_context = {'form_titulo': 'Remover Usuário', 'entidade': 'Usuario'}


class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'produtos.html'
    context_object_name = 'Produtos'
    extra_context = {'form_titulo': 'Lista de Produtos'}

    def get_queryset(self):
        # MOSTRAR APENAS OS PRODUTOS DO VENDEDOR LOGADO
        return Produto.objects.filter(vendedor=self.request.user)


class ProdutoCreateView(LoginRequiredMixin, View):
    template_name = 'formulario_produto.html'

    def get(self, request):
        form = ProdutoForms()
        caracteristicas = CaracteristicaFormSet()
        especificacoes = EspecificacaoFormSet()

        return render(request, self.template_name, {
            "form": form,
            "caracteristicas": caracteristicas,
            "especificacoes": especificacoes,
            "form_titulo": "Cadastro de Produto"
        })

    def post(self, request):
        form = ProdutoForms(request.POST, request.FILES)
        caracteristicas = CaracteristicaFormSet(request.POST)
        especificacoes = EspecificacaoFormSet(request.POST)

        if form.is_valid() and caracteristicas.is_valid() and especificacoes.is_valid():
            produto = form.save(commit=False)
            produto.vendedor = request.user
            produto.save()

            caracteristicas.instance = produto
            caracteristicas.save()

            especificacoes.instance = produto
            especificacoes.save()

            messages.success(request, "Produto cadastrado com sucesso!")
            return redirect('produtos')

        return render(request, self.template_name, {
            "form": form,
            "caracteristicas": caracteristicas,
            "especificacoes": especificacoes,
            "form_titulo": "Cadastro de Produto"
        })


class ProdutoUpdateView(LoginRequiredMixin, View):
    template_name = 'formulario_produto.html'

    def get(self, request, pk):
        produto = get_object_or_404(Produto, pk=pk, vendedor=request.user)

        form = ProdutoForms(instance=produto)
        caracteristicas = CaracteristicaFormSet(instance=produto)
        especificacoes = EspecificacaoFormSet(instance=produto)

        return render(request, self.template_name, {
            "form": form,
            "caracteristicas": caracteristicas,
            "especificacoes": especificacoes,
            "form_titulo": "Editar Produto"
        })

    def post(self, request, pk):
        produto = get_object_or_404(Produto, pk=pk, vendedor=request.user)

        form = ProdutoForms(request.POST, request.FILES, instance=produto)
        caracteristicas = CaracteristicaFormSet(request.POST, instance=produto)
        especificacoes = EspecificacaoFormSet(request.POST, instance=produto)

        if form.is_valid() and caracteristicas.is_valid() and especificacoes.is_valid():
            form.save()
            caracteristicas.save()
            especificacoes.save()
            messages.success(request, "Produto editado com sucesso!")
            return redirect('produtos')

        return render(request, self.template_name, {
            "form": form,
            "caracteristicas": caracteristicas,
            "especificacoes": especificacoes,
            "form_titulo": "Editar Produto"
        })


class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = "excluir_registro.html"
    context_object_name = "registro"
    success_url = reverse_lazy('produtos')

    def get_queryset(self):
        return Produto.objects.filter(vendedor=self.request.user)


class LoginUsuarioView(LoginView):
    template_name = "login.html"


def detalhe_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'detalhes_produtos.html', {'produto': produto})


class CadastroUsuarioView(CreateView):
    template_name = "cadastrar.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        usuario = form.save()
        return super().form_valid(form)


def cadastrar(request):
    if request.method == 'POST':
        nome = (request.POST.get('username') or "").strip()
        email = (request.POST.get('email') or "").strip().lower()
        senha1 = request.POST.get('password1') or ""
        senha2 = request.POST.get('password2') or ""
        is_vendedor = request.POST.get('is_vendedor') == 'on'

        if not nome or not email or not senha1 or not senha2:
            messages.warning(request, "Preencha todos os campos.")
            return render(request, 'cadastrar.html', {
                'username': nome,
                'email': email,
            })

        if senha1 != senha2:
            messages.warning(request, "As senhas não conferem.")
            return render(request, 'cadastrar.html', {
                'username': nome,
                'email': email,
            })

        if len(senha1) < 6:
            messages.warning(request, "A senha deve ter ao menos 6 caracteres.")
            return render(request, 'cadastrar.html', {
                'username': nome,
                'email': email,
            })

        if Usuario.objects.filter(email=email).exists():
            messages.warning(request, "Este e-mail já está cadastrado.")
            return render(request, 'cadastrar.html', {
                'username': nome,
                'email': email,
            })

        # 1) Cria o auth.User (tratando possíveis conflitos de username)
        username_base = nome or email.split('@')[0]
        username = username_base
        suffix = 1
        while AuthUser.objects.filter(username=username).exists():
            username = f"{username_base}{suffix}"
            suffix += 1

        try:
            auth_user = AuthUser.objects.create_user(username=username, email=email, password=senha1)
        except IntegrityError:
            # fallback: cria usuário com nome único adicionando timestamp
            import time
            username = f"{username_base}{int(time.time())}"
            auth_user = AuthUser.objects.create_user(username=username, email=email, password=senha1)

        # 2) Cria o Usuario (seu model) normalmente, armazenando a senha hasheada também
        usuario = Usuario(
            nome=nome,
            email=email,
            senha=make_password(senha1),
            is_vendedor=is_vendedor
        )
        usuario.save()

        messages.success(request, "Cadastro realizado com sucesso! Faça login.")
        return redirect('login_usuario')

    return render(request, 'cadastrar.html')


def login_usuario(request):
    if request.method == 'POST':
        email = (request.POST.get('email') or "").strip().lower()
        senha = request.POST.get('senha') or ""

        if not email or not senha:
            messages.warning(request, "Preencha todos os campos.")
            return render(request, 'login.html')

        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            messages.error(request, "E-mail ou senha incorretos.")
            return render(request, 'login.html')

        # primeiro verifica a senha guardada no seu model Usuario
        if not check_password(senha, usuario.senha):
            messages.error(request, "E-mail ou senha incorretos.")
            return render(request, 'login.html')

        # tenta achar um AuthUser com o mesmo e-mail
        try:
            auth_user = AuthUser.objects.get(email=usuario.email)
        except AuthUser.DoesNotExist:
            auth_user = None

        if auth_user:
            # se o AuthUser existe, tenta autenticar usando username dele
            user = authenticate(request, username=auth_user.username, password=senha)
            if user is None:
                # pode ser que a senha do AuthUser não esteja sincronizada (senha inutilizável ou diferente)
                messages.warning(request, "Conta encontrada, mas senha incorreta no sistema de autenticação. Use 'esqueci a senha' para redefinir.")
                return render(request, 'login.html')
            # autentica no Django
            login(request, user)
        else:
            messages.warning(request, "Conta encontrada no sistema, mas não há uma conta de autenticação ativa. Por favor, efetue o cadastro ou peça recuperação de senha.")
            return render(request, 'login.html')

        # informações de sessão (mantém seu comportamento atual)
        request.session['usuario_nome'] = usuario.nome
        request.session['usuario_email'] = usuario.email
        request.session['usuario_is_vendedor'] = usuario.is_vendedor
        request.session.set_expiry(60 * 60 * 24 * 7)

        if usuario.is_vendedor:
            return redirect('produtos')
        else:
            return redirect('home')

    return render(request, 'login.html')


def esqueceu_senha(request):
    if request.method == 'POST':
        email = (request.POST.get('email') or "").strip().lower()

        if not email:
            messages.warning(request, "Por favor, digite seu e-mail.")
            return render(request, 'esqueceu_senha.html')

        try:
            usuario = Usuario.objects.get(email=email)

            import random
            import string
            nova_senha = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            usuario.senha = make_password(nova_senha)
            usuario.save()
            messages.success(
                request,
                f"Sua nova senha temporária é: {nova_senha}"
            )

            return redirect('login_usuario')

        except Usuario.DoesNotExist:
            messages.error(request, "E-mail não encontrado.")
            return render(request, 'esqueceu_senha.html')

    return render(request, 'esqueceu_senha.html')


class LoginVendedorView(LoginView):
    template_name = "vendedor_login.html"

    def get_success_url(self):
        return reverse_lazy('produtos')


def catalogo(request):
    produtos = Produto.objects.all()
    busca = request.GET.get('q')

    if busca:
        produtos = produtos.filter(nome__icontains=busca)

    return render(request, 'catalogo.html', {'produtos': produtos})
