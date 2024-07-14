from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, tweet

admin.site.unregister(User)  # Desregistrar o modelo User padrão do Django

# Inline para exibir o perfil junto com o usuário na administração
class ProfileInline(admin.StackedInline):
    model = Profile

# Personalização do modelo User na administração
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']  # Campos exibidos para edição
    inlines = [ProfileInline]  # Exibir o perfil inline

# Registrar o modelo User personalizado na administração
admin.site.register(User, UserAdmin)

# Registrar o modelo Profile na administração
admin.site.register(Profile)

# Registrar o modelo Tweet na administração
admin.site.register(tweet)
