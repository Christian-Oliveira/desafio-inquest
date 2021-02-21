from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class BaseModel(models.Model):
	created_at  = models.DateTimeField(_("Criado_em"), auto_now_add=True)
	updated_at = models.DateTimeField(_("Atualizado_em"), auto_now=True)
	active    = models.BooleanField(_("Ativo"), default=True)

	class Meta:
		abstract = True

class PeopleModel(BaseModel):
	"""
    People Model
    Define os atributos de uma Pessoa
    """
	# Pessoa Fisica ou Juridica
	PEOPLE_TYPE = (
		('F', 'FISICA'),
		('J', 'JURIDICA'),
	)
  
	people_type = models.CharField(_("Tipo"), max_length=1, choices=PEOPLE_TYPE)
	name        = models.CharField(_("Nome"), max_length=150)
	cpf					= models.CharField(_("CPF"), max_length=11, null=True, blank=True, unique=True)
	cnpj				= models.CharField(_("CNPJ"), max_length=14, null=True, blank=True, unique=True)
	email				= models.EmailField(_("E-mail"), max_length=150, unique=True)

	class Meta:
		verbose_name = "Pessoa"
		verbose_name_plural = "Pessoas"

	def __str__(self):
		return self.name
	
