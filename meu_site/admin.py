from django.contrib import admin
from meu_site.models import Produto, Usuario, Avaliacao, Categoria, Caracteristica, EspecificacaoTecnica

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'senha']

class CaracteristicaInline(admin.TabularInline):
    model = Caracteristica
    extra = 1  # quantidade de linhas vazias para adicionar

class EspecificacaoTecnicaInline(admin.TabularInline):
    model = EspecificacaoTecnica
    extra = 1

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'categoria', 'imagem', 'qnt_estoque']
    inlines = [CaracteristicaInline, EspecificacaoTecnicaInline]

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'produto', 'nota', 'comentario', 'data']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']
