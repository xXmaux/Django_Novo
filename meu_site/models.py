from django.db import models
from django.contrib.auth.models import User
from django.db.models import ForeignKey


# Create your models here.

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    senha = models.CharField(max_length=100)
    telefone = models.CharField(max_length=12, null=True, blank=True)
    is_vendedor = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    categoria = models.ForeignKey('Categoria', on_delete=models.DO_NOTHING)
    imagem = models.ImageField(upload_to='produtos')
    qnt_estoque = models.IntegerField()
    vendedor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='produtos', null=True, blank=True)
    preco = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.nome


# Característica do produto (ex: "Bluetooth 5.0", "Bateria 30h")
class Caracteristica(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='caracteristicas')
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.produto.nome} - {self.descricao}"


# Especificação técnica (ex: "Marca: XYZ", "Modelo: 1234")
class EspecificacaoTecnica(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='especificacoes')
    nome = models.CharField(max_length=100)
    valor = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.produto.nome} - {self.nome}: {self.valor}"


class Avaliacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    nota = models.IntegerField()
    comentario = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.nome
