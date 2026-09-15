# Base de Conhecimento

## Dados Utilizados


| Arquivo | Formato | Como o ECO utiliza? |
|---------|---------|---------------------|
| `historico_interacoes.csv` | CSV | Contextualiza interações anteriores |
| `perfil_usuario.json` | JSON | Personaliza as recomendações para o usuário |
| `transacoes.csv` | CSV | Analisa padrão de gastos do cliente e usa essas informações para sugerir ações |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Foi adicionada a meta "Comprar um novo computador" junto ao objetivo de guardar mais dinheiro pro fundo de emergência.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas possibilidades, injetar os dados diretamente no prompt (Ctrl + C, Ctrl + V) ou carregar os arquivos via código, como no exemplo:

```python
import pandas as pd
import json

#CSVs

historico = pd.read_csv('data/historico_interacoes.csv')
transacoes = pd.read_csv('data/transacoes.csv')

#JSONs

with open('data/perfil_investidor.json','r', econding='utf-8') as f:
    perfil = json.load(f)
    
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Para simplificar, podemos "injetar" os dados no prompt. Vale lembrar que para soluções mais robustas, o ideal é que as informações sejam carregadas dinamicamente para obter maior flexibilidade.

```text
DADOS DO USUÁRIO:
{
  "nome": "John Smith",
  "idade": 22,
  "profissao": "Engenheiro de Software Júnior",

  "renda": {
    "salario_bruto": 3200.00,
    "renda_extra_minima": 500.00,
    "renda_extra_maxima": 1500.00,
    "descricao_renda_extra": "Freelances de desenvolvimento de sites e outros serviços na área de tecnologia"
  },

  "moradia": {
    "tipo": "aluguel",
    "valor_mensal": 1000.00
  },

  "objetivo_principal": "Organizar melhor os gastos e aumentar a economia mensal",

  "metas": [
    {
      "meta": "Criar uma reserva de emergência",
      "valor_objetivo": 10000.00,
      "valor_atual": 2000.00,
      "prazo": "2027-12"
    },
    {
      "meta": "Guardar dinheiro para comprar um computador novo",
      "valor_objetivo": 6000.00,
      "valor_atual": 500.00,
      "prazo": "2027-06"
    }
  ],

  "preferencias_financeiras": {
    "valor_desejado_para_economizar_por_mes": 500.00,
    "prioridade": "Evitar gastos desnecessários sem abrir mão completamente de lazer"
  }
}

TRANSAÇÕES DO USUÁRIO:
data,descricao,categoria,valor,tipo
2026-08-01,Salário,receita,3500.00,entrada
2026-08-03,Freelance - Landing Page,freelance,900.00,entrada
2026-08-05,Aluguel,moradia,1000.00,saida
2026-08-06,Conta de Luz,moradia,145.00,saida
2026-08-06,Internet,moradia,100.00,saida
2026-08-07,Conta de Água,moradia,70.00,saida
2026-08-08,Supermercado,alimentacao,380.00,saida
2026-08-10,Spotify,assinatura,21.90,saida
2026-08-12,Ferramenta de IA,assinatura,100.00,saida
2026-08-13,Plano de Celular,comunicacao,80.00,saida
2026-08-14,Uber,transporte,42.00,saida
2026-08-15,Delivery,alimentacao,68.00,saida
2026-08-16,Restaurante,alimentacao,82.00,saida
2026-08-17,Cinema,lazer,45.00,saida
2026-08-18,Uber,transporte,37.00,saida
2026-08-19,Supermercado,alimentacao,165.00,saida
2026-08-20,Parcela Monitor,tecnologia,200.00,saida
2026-08-22,Delivery,alimentacao,74.00,saida
2026-08-23,Roupa,compras,180.00,saida
2026-08-24,Farmácia,saude,64.00,saida
2026-08-26,Uber,transporte,51.00,saida
2026-08-27,Delivery,alimentacao,98.00,saida
2026-08-28,Supermercado,alimentacao,190.00,saida
2026-08-30,Jogo para PC,lazer,79.90,saida

HISTÓRICO DO USUÁRIO:
data,tipo,tema,resumo,acao
2026-08-05,analise,Alimentação,Gastos com delivery aumentaram no mês,ECO sugeriu reduzir pedidos
2026-08-12,alerta,Assinaturas,Usuário possui várias assinaturas recorrentes,ECO sugeriu revisar serviços pouco utilizados
2026-08-20,consulta,Meta financeira,Usuário perguntou quanto conseguiria guardar até dezembro,ECO realizou uma simulação
2026-09-01,relatorio_mensal,Orçamento,Gastos do mês ficaram acima do planejado,ECO identificou principais categorias responsáveis
2026-09-08,meta,Reserva de emergência,Usuário decidiu guardar R$ 300 por mês,Meta registrada

```

---

## Exemplo de Contexto Montado

> Exemplo de como os dados são formatados para o agente.

O exmeplo abaixo usa os dados da base de conhecimento resumidos, deixando apenas as informações mais importantes otimizando o consumo de tokens. Vale ressaltar que é importante balancear o consumo de tokensc com a quantidade de informações relevantes do usuário.

```
Dados do Usuário:
- Nome: John Smith
- Meta: Guardar R$ 500 por mês
- Saldo disponível: R$ 4.725
- Reseva: R$ 8.300

Entradas:
- 23/09: Freelance Landing Page - R$ 550
- 30/09: Site Completo - R$ 1.550
- 03/10: Salário - R$ 3.200

Últimas gastos:
- 19/09: Delivery - R$ 35
- 20/09: Jogo - R$ 155
- 26/09: Uber - R$ 15
- 28/09: Roupas - R$ 180
- 01/10: Supermercado - R$ 450
- 03/10: Streaming - R$ 55
...
```
