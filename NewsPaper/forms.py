from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from NewsPaper.models import Post

######################################################################################################################


class FormCreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'type_post',
            'category',
            'title',
            'text',
        ]
        labels = {
            'type_post': 'Тип записи',
            'category': 'Тематика записи',
            'title': 'Заголовок записи',
            'text': 'Текст записи',
        }
        widgets = {
            'type_post': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Укажите заголовок записи',
                }
            ),
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Напишите текст записи',
                }
            ),
        }


######################################################################################################################


class FormSearchPost(forms.Form):
    search = forms.CharField(
        label='Поиск',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Введите запрос для поиска в заголовке или тексте записи',
                'type': 'text',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    ordering = forms.ChoiceField(
        label='Сортировка',
        widget=forms.RadioSelect(
            attrs={
                'class': 'form-check-input',
            }
        ),
        choices=(
            ('-create_date', 'Новые сверху'),
            ('create_date', 'Старые сверху'),
            ('author', 'Авторы от А до Я'),
            ('-author', 'Авторы от Я до А'),
        ),
        initial='-create_date',
        required=False,
    )


######################################################################################################################


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get_or_create(name='basic')[0]
        basic_group.user_set.add(user)
        return user


######################################################################################################################


class RegisterForm(UserCreationForm):
    # first_name = forms.CharField(label = "Имя") # опционально
    # last_name = forms.CharField(label = "Фамилия") # опционально
    password1 = forms.CharField(
        max_length=16,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль'
    )
    password2 = forms.CharField(
        max_length=16,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Повторите пароль'
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )
        labels = {
            'username': 'Логин',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return super().clean()


######################################################################################################################


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите логин пользователя',
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'type': 'password',
                    'class': 'form-control',
                    'autocomplete': 'off',
                    'placeholder': 'Введите пароль пользователя',
                }
            ),
        }
        labels = {
            'username': 'Логин пользователя',
            'password': 'Пароль пользователя',
        }
        help_texts = {
            'username': 'Обязательное поле. Только английские буквы.',
        }


######################################################################################################################
