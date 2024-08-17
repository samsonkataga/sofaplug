from app1.models import *
from django.forms import ModelForm


class ContactForm(ModelForm):


	class Meta:
		model=Contact
		fields='__all__'



class SettlementForm(ModelForm):

	class Meta:
		model=Settlement
		fields='__all__'
class ItemForm(ModelForm):


	class Meta:
		model=Item
		fields='__all__'

