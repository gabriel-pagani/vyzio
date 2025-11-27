from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ValidationError
from .validators import valid_cpf, valid_phone, valid_zipcode, valid_url


class Dashboards(models.Model):
    SECTORS = [
        ('Almoxarifado', 'Almoxarifado'),
        ('Comercial', 'Comercial'),
        ('Controle', 'Controle'),
        ('Compras', 'Compras'),
        ('Contabilidade', 'Contabilidade'),
        ('Custos', 'Custos'),
        ('Diretoria', 'Diretoria'),
        ('Engenharia', 'Engenharia'),
        ('Financeiro', 'Financeiro'),
        ('Fiscal', 'Fiscal'),
        ('Gestão de Pessoas', 'Gestão de Pessoas'),
        ('Gestão Industrial', 'Gestão Industrial'),
        ('Industria de Apontamento', 'Industria de Apontamento'),
        ('Industria de Eletrônicos', 'Industria de Eletrônicos'),
        ('Industria de Esferas', 'Industria de Esferas'),
        ('Industria Metalúrgica', 'Industria Metalúrgica'),
        ('Industria de Placas', 'Industria de Placas'),
        ('Industria de Tachas', 'Industria de Tachas'),
        ('Industria de Tintas', 'Industria de Tintas'),
        ('Jurídico', 'Jurídico'),
        ('Licitação', 'Licitação'),
        ('Logística', 'Logística'),
        ('Manutenção', 'Manutenção'),
        ('Marketing', 'Marketing'),
        ('Monitoramentos', 'Monitoramentos'),
        ('Obras', 'Obras'),
        ('Projetos', 'Projetos'),
        ('Qualidade', 'Qualidade'),
        ('Recebimentos', 'Recebimentos'),
        ('Recursos Humanos', 'Recursos Humanos'),
        ('Secretaria', 'Secretaria'),
        ('Segurança do Trabalho', 'Segurança do Trabalho'),
        ('Tecnologia', 'Tecnologia'),
        ('Trânsito', 'Trânsito'),
    ]

    STATUS = [
        ('D', 'Em Desenvolvimento'),
        ('M', 'Em Manutenção'),
        ('F', 'Em Funcionamento'),
    ]

    title = models.CharField(max_length=150, unique=True)
    sector = models.CharField(max_length=150, choices=SECTORS)
    metabase_code = models.PositiveSmallIntegerField(blank=True, null=True, unique=True)
    powerbi_url = models.CharField(blank=True, null=True, unique=True, validators=[valid_url])
    status = models.CharField(max_length=1, choices=STATUS, default="D")
    fav_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorited_dashboards', blank=True)

    def clean(self):
        if self.metabase_code and self.powerbi_url:
            raise ValidationError(
                'Fill in only the "Metabase code" or the "Powerbi url" field.'
            )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboards'
        ordering = ['sector', 'title']
        permissions = [
            ("view_all_dashboards", "Can view all dashboards"),
        ]


class Users(AbstractUser):
    STATES = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]
    
    email = models.EmailField(blank=True, null=True)
    cpf = models.CharField(max_length=11, blank=True, null=True, validators=[valid_cpf])
    phone = models.CharField(max_length=11, blank=True, null=True, validators=[valid_phone])
    date_birth = models.DateField(blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=25, blank=True, null=True)
    complement = models.CharField(max_length=200, blank=True, null=True)
    neighborhood = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True, choices=STATES)
    zip_code = models.CharField(max_length=8, blank=True, null=True, validators=[valid_zipcode])
    observations = models.TextField(blank=True, null=True)
    dashboards = models.ManyToManyField(Dashboards, related_name='assigned_users', blank=True)

    def clean(self):
        super().clean()
        if self.email:
            email = Users.objects.filter(email=self.email).exclude(pk=self.pk)
            if email.exists():
                raise ValidationError({'email': 'A user with this email already exists.'})

class GroupDashboards(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    dashboards = models.ManyToManyField(Dashboards, related_name='assigned_groups', blank=True)

    def __str__(self):
        return self.group.name
