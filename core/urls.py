from django.urls import path
from django.contrib.auth import views as auth_views
from .views import IndexView, AlunoListaView, RelatorioDetalheView, RelatorioPdfView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', IndexView.as_view(), name='index'),
    path('alunos/', AlunoListaView.as_view(), name='alunos'),
    path('alunos/<uuid:pk>/', RelatorioDetalheView.as_view(), name='relatorio'),
    path('alunos/<uuid:pk>/pdf/', RelatorioPdfView.as_view(), name='relatorio_pdf'),
    
    path('relatorio/<uuid:pk>/', RelatorioDetalheView.as_view()),
    path('relatorio/<uuid:pk>/pdf/', RelatorioPdfView.as_view()),
]
