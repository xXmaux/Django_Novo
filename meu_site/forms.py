
from django import forms
from meu_site.models import Usuario, Produto
from django.forms import inlineformset_factory
from meu_site.models import Caracteristica, EspecificacaoTecnica

class UsuarioForms(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'

class ProdutoForms(forms.ModelForm):
    class Meta:
        model = Produto
        exclude = ['vendedor']  # o vendedor vai ser preenchido automaticamente na view
        labels = {'nome': 'Nome do Produto'}
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-group form-control',
                'placeholder': 'Informe o nome do produto',
                'title': 'Nome do produto',
                'maxlength': '100'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-group form-control',
                'placeholder': 'Descreva o produto...',
                'rows': '4',
                'maxlength': '500'
            }),
            'qnt_estoque': forms.NumberInput(attrs={
                'class': 'form-group form-control',
                'min': 0,
                'title': 'Quantidade em estoque'
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'form-group form-control',
                'min': 0,
                'step': '0.01',
                'title': 'Preço do produto'
            }),
        }

CaracteristicaFormSet = inlineformset_factory(
    Produto,
    Caracteristica,
    fields=['descricao'],
    extra=1,
    min_num=1,
    validate_min=True,
    widgets={
        'descricao': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Bluetooth 5.0, Resistente à água',
            'maxlength': '200'
        })
    }
)

EspecificacaoFormSet = inlineformset_factory(
    Produto,
    EspecificacaoTecnica,
    fields=['nome', 'valor'],
    extra=1,
    min_num=1,
    validate_min=True,
    widgets={
        'nome': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Marca, Modelo, Peso',
            'maxlength': '100'
        }),
        'valor': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Sony, XYZ-123, 250g',
            'maxlength': '200'
        })
    }
)