from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

def cadastro_usuario(request):
    """
    View para registrar um novo usuário no banco de dados.
    """
    if request.method == 'POST':
        nome_completo = request.POST['nome_completo']
        email = request.POST['email']
        password = request.POST['password']

        # Verifica se já existe um usuário com o mesmo email
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Já existe uma conta com esse email.')
        else:
            # Cria o usuário no banco de dados
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=nome_completo
            )
            user.save()
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('login')  # Redireciona para a página de login
    return render(request, 'usuarios/cadastro.html')


def login_usuario(request):
    """
    View para autenticar o usuário e redirecionar para a página /agenda.
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Autentica o usuário
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Realiza o login e redireciona para /agenda
            login(request, user)
            return redirect('/agenda')  # Página protegida
        else:
            # Exibe uma mensagem de erro caso o login seja inválido
            messages.error(request, 'Email ou senha inválidos.')
    return render(request, 'usuarios/login.html')
