from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Transaction, Budget, Income
import mysite.settings as s

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Имя'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Фамилия'}))

	class Meta(User):
		model = User
		fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<ul class="form-text text-muted small"><li>Пользователь с таким именем уже существует.</li><li>Обязательно. 150 символов и менее. Только буквы, цифры и @/./+/-/_ .</li></ul>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Ваш пароль не должен повторять ваши данные.</li><li>Пароль должен содержать 8 и более символов.</li><li>Пароль слишком легко угадать.</li><li>Пароль не должен состоять только из цифр.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<ul class="form-text text-muted"><li>Повторите раннее введенный пароль для верификации.</li></ul>'


class AddBudgetForm(forms.ModelForm):
	name = forms.CharField(required=True, label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Название'}))
	limit = forms.FloatField(required=True, label ='',widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Лимит'}))
	class Meta:
		model = Budget
		exclude = ('user',)

class AddTransactionForm(forms.ModelForm):
	#sum = forms.FloatField(required=True, label ='',widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cумма'}))
	category = forms.CharField(required=True, label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'категория бюджета'}))
	#data = forms.DateField(required=True, input_formats=s.DATE_INPUT_FORMATS, label ='',widget=forms.DateTimeInput(attrs={'class':'form-control', 'placeholder':'Дата и время'}))
	class Meta:
		model = Transaction
		exclude = ('user',)

class AddIncomeForm(forms.ModelForm):
	name = forms.CharField(required=True, label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Название'}))
	sum = forms.FloatField(required=True, label ='',widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cумма'}))
	time = forms.DateField(required=True, input_formats=s.DATE_INPUT_FORMATS, label ='',widget=forms.DateInput(attrs={'class':'form-control', 'placeholder':'Дата начисления'}))
	class Meta:
		model = Income
		exclude = ('user',)