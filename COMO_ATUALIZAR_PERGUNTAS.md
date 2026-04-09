# Como Atualizar as Perguntas do Quiz

## Método: Editar o arquivo init_db.py

1. Abra o arquivo `init_db.py` no seu editor

2. Encontre a seção `sample_questions` (linha ~20)

3. Substitua as perguntas de exemplo pelas suas perguntas reais

4. Execute o script para reinicializar o banco de dados:

```bash
# No terminal/PowerShell
python init_db.py
```

**ATENÇÃO**: Isso irá apagar todas as respostas existentes e criar novas perguntas!

## Formato das Perguntas

```python
{
    "text": "Sua pergunta aqui?",
    "options": [
        {"text": "Resposta 1", "type": "romantic"},
        {"text": "Resposta 2", "type": "bold"},
        {"text": "Resposta 3", "type": "elegant"},
        {"text": "Resposta 4", "type": "bohemian"},
        {"text": "Resposta 5", "type": "minimalist"},
        {"text": "Resposta 6", "type": "trendy"}
    ]
}
```

## Tipos de Personalidade Disponíveis

| Código | Nome | Descrição |
|--------|------|-----------|
| `romantic` | Romântica | Feminina, delicada, sonhadora |
| `bold` | Ousada | Vibrante, confiante, marcante |
| `elegant` | Elegante | Sofisticada, clássica, atemporal |
| `bohemian` | Boêmia | Livre, criativa, autêntica |
| `minimalist` | Minimalista | Simples, funcional, versátil |
| `trendy` | Moderna | Antenada, inovadora, fashion forward |

## Dicas para Criar Boas Perguntas

1. **Seja específica**: Perguntas claras geram respostas melhores
2. **Varie os temas**: Roupas, cores, acessórios, estilo de vida, etc.
3. **6 opções por pergunta**: Uma para cada tipo de personalidade
4. **Linguagem amigável**: Use uma linguagem que faça sentido para seu público
5. **5-8 perguntas**: Quantidade ideal para não cansar o usuário

## Exemplo de Questões Recomendadas

### Sobre Roupas
- Qual roupa você escolhe para um evento especial?
- O que você veste em um dia casual?
- Qual peça não pode faltar no seu guarda-roupa?

### Sobre Cores
- Qual combinação de cores te representa?
- Qual cor você mais usa?
- Qual paleta de cores te atrai?

### Sobre Acessórios
- Qual acessório completa seu look?
- Como você escolhe suas joias?
- Que tipo de bolsa você prefere?

### Sobre Estilo
- Como você descreveria seu estilo?
- Qual palavra define seu jeito de se vestir?
- O que é mais importante para você na moda?

### Sobre Tecidos/Texturas
- Qual tecido você prefere?
- Que tipo de textura te atrai?

## Testando as Mudanças

Depois de atualizar as perguntas:

1. Execute `python init_db.py`
2. Execute `python app.py`
3. Abra http://localhost:5000
4. Teste o quiz completo
5. Verifique se os resultados fazem sentido

## Personalizando os Resultados

Para alterar as descrições dos tipos de personalidade, edite o arquivo `models.py`:

```python
PERSONALITY_TYPES = {
    "romantic": {
        "name": "Romântica",  # Nome exibido
        "description": "Sua descrição aqui...",  # Descrição longa
        "style_tips": "Dicas de estilo aqui...",  # Dicas
        "color": "#FFB6C1"  # Cor em hexadecimal
    },
    # ... outros tipos
}
```

## Precisa de Ajuda?

Se tiver dúvidas sobre como formatar as perguntas ou tipos de personalidade, entre em contato!
