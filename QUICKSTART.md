# 🎀 Nathalia Otero - Quiz de Estilo

## 🚀 Início Rápido

### 1. Instalar Dependências

Abra o PowerShell ou Terminal nesta pasta e execute:

```bash
pip install -r requirements.txt
```

### 2. Criar arquivo .env

```bash
# Copie o arquivo de exemplo
copy .env.example .env
```

### 3. Inicializar o Banco de Dados

```bash
python init_db.py
```

### 4. Executar a Aplicação

```bash
python app.py
```

### 5. Abrir no Navegador

Visite: http://localhost:5000

## 📱 Funcionalidades

✅ Quiz interativo com design colorido  
✅ 6 tipos de personalidade de moda  
✅ Coleta de dados de clientes  
✅ Painel administrativo  
✅ Exportação de dados  
✅ Responsivo para mobile  
✅ Pronto para QR code  

## 🎨 Tipos de Personalidade

1. **Romântica** - Delicada e feminina
2. **Ousada** - Vibrante e confiante
3. **Elegante** - Sofisticada e atemporal
4. **Boêmia** - Livre e autêntica
5. **Minimalista** - Simples e funcional
6. **Moderna** - Antenada nas tendências

## 🔧 Próximos Passos

1. **Personalizar Perguntas**
   - Edite `init_db.py` com suas perguntas
   - Veja `COMO_ATUALIZAR_PERGUNTAS.md` para detalhes

2. **Fazer Deploy**
   - Siga `DEPLOYMENT.md` para publicar online
   - Recomendado: Render.com (gratuito)

3. **Criar QR Code**
   - Use qr-code-generator.com
   - Cole a URL do seu app deployado
   - Personalize com cores da marca

## 📊 Acessar Painel Administrativo

Visite: http://localhost:5000/admin

Aqui você pode:
- Ver total de respostas
- Ver distribuição de personalidades
- Ver lista de clientes
- Exportar dados em JSON

## 🎯 Para o Evento

**Checklist:**
- [ ] Atualizar perguntas com as definitivas
- [ ] Fazer deploy do app
- [ ] Criar e testar QR code
- [ ] Testar em diferentes celulares
- [ ] Imprimir QR code grande (A4)
- [ ] Ter plano B (formulários em papel)

## 🆘 Problemas Comuns

**Erro ao executar python:**
```bash
# Use python3 ou py
py app.py
```

**Porta 5000 em uso:**
- Edite `app.py` e mude `port=5000` para outra porta (ex: 5001)

**Dependências não instalam:**
```bash
# Crie um ambiente virtual primeiro
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 📞 Estrutura do Projeto

```
Natforms/
├── app.py                 # Aplicação Flask principal
├── models.py              # Modelos do banco de dados
├── config.py              # Configurações
├── init_db.py             # Inicialização do BD
├── requirements.txt       # Dependências Python
├── templates/             # Templates HTML
│   ├── index.html         # Página do quiz
│   └── admin.html         # Painel admin
├── static/                # Arquivos estáticos
│   ├── css/
│   │   ├── style.css      # Estilos do quiz
│   │   └── admin.css      # Estilos do admin
│   └── js/
│       ├── app.js         # Lógica do quiz
│       └── admin.js       # Lógica do admin
└── DEPLOYMENT.md          # Guia de deployment
```

## 🎨 Customização de Cores

Para ajustar as cores da marca, edite `static/css/style.css`:

```css
:root {
    --primary-color: #FF6B9D;    /* Rosa principal */
    --secondary-color: #C44569;  /* Rosa escuro */
    --accent-1: #FFA07A;         /* Coral */
    --accent-2: #98D8C8;         /* Verde água */
    --accent-3: #F7B731;         /* Amarelo */
    --accent-4: #5F27CD;         /* Roxo */
}
```

---

**Feito com 💖 para Nathalia Otero**
