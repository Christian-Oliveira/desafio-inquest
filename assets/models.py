from django.db import models
from django.utils.translation import ugettext_lazy as _

from people.models import PeopleModel

# Create your models here.

class BaseModel(models.Model):
	created_at  = models.DateTimeField(_("Criado_em"), auto_now_add=True)
	updated_at  = models.DateTimeField(_("Atualizado_em"), auto_now=True)
	active      = models.BooleanField(_("Ativo"), default=True)

	class Meta:
		abstract = True

class AssetsModel(BaseModel):
    """
    Assets Model
    Define os atributos de um Bem (Ativo)
    """
    class AssetsType(models.TextChoices):
        INT = 'INT', _('INTANGIVEIS')
        MOV = 'MOV', _('MOVEIS')
        IMO = 'IMO', _('IMOVEIS')

    class AcquisitionForm(models.TextChoices):
        COM = 'COM', _('COMPRADO')
        DOA = 'DOA', _('DOADO')
        HER = 'HER', _('HERDADO')

    person            = models.ForeignKey(PeopleModel, related_name='assets', blank=True, on_delete=models.CASCADE)
    assets_type       = models.CharField(_('Tipo de Ativo'), max_length=3, choices=AssetsType.choices)
    code              = models.PositiveSmallIntegerField(_('Código'))
    description       = models.TextField(_('Descrição'))
    acquisition_form  = models.CharField(_('Forma de Aquisição'), max_length=3, choices=AcquisitionForm.choices)
    acquisition_value = models.DecimalField(_('Valor de Aquisição'), max_digits=16, decimal_places=2, null=True, blank=True)
    localization      = models.CharField(_('Localização'), max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Ativo"
        verbose_name_plural = "Ativos"

    def __str__(self):
        return str(self.code) + ": " + self.description