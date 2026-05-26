# Fome Zero Company

# 1. Problema de Negócio

A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.
Recém contratado, o CEO Kleiton Guerra precisa entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a Fome Zero Company, e para isso, ele precisa que seja feita uma análise nos dados da empresa e que sejam gerados dashboards, a partir dessas análises, para responder às seguintes perguntas:

Visão geral da empresa:

1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?

Análise a partir dos países:

1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?
9. Qual o nome do país que possui, na média, a maior nota média registrada?
10. Qual o nome do país que possui, na média, a menor nota média registrada?
11. Qual a média de preço de um prato para dois por país?

Análise a partir dos cidades:

1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?

Análise a partir dos restaurantes:

1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?
6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?
7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)

Análise a partir das culinárias:

1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação?
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação?
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?
12. Qual o tipo de culinária que possui a maior nota média?
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?

O CEO também pediu que fosse gerado um dashboard que permitisse que ele
visualizasse as principais informações das perguntas que ele fez.

# 2. Premissas do Negócio

1. A análise foi realizada com dados entre 10/05/2026 e 18/05/2026.
2. Marketplace foi o modelo de negócio assumido.
3. As 4 principais visões do negócio foram: 
    1. visão geral da empresa
    2. análise a partir dos países
    3. análise a partir dos cidades
    4. análise a partir dos restaurantes
    5. análise a partir dos tipos de culinária

# 3. Estratégia da Solução

1. Coleta dos dados:
a. os dados foram coletados via Kaggle
2. Entender os dados que você está trabalhando:
    1. visualização geral dos dados para uma primeira impressão e análise superficial
    2. O que cada coluna representa, o que pode ser removido e o que pode ser melhorado do DataFrame
3. Limpeza nos dados:
    1. verificar se existem dados duplicados
    2. entender as variáveis disponíveis na base de dados fazendo uma tabela de estatística descritiva
    3. verificar se há dados faltantes
    4. aplicar as funções de renome das colunas
    5. aplicar funções de novas colunas para representação melhor da informação
        1. código país → nome país
        2. código cor → nome cor representando país
        3. coluna que representa nominalmente o preço dos pratos do restaurante
        4. simplificar a análise definindo apenas um tipo de culinária por restaurante
4. Explorar os dados para responder as perguntas de negócio solicitada:
    1. começando respondendo as perguntas sem usar programação, para planejamento da solução.
    2. utilizando gráficos para consolidar e validar a resposta.
    3. nos casos das perguntas que tenha dois registros como resposta,
    selecione sempre o registro com o valor da coluna "Restaurant ID” menor, ou seja, restaurante que está há mais tempo cadastrado no aplicativo.
5. Respostas disponíveis no Streamlit:
a. utilizando o Streamlit,  os insights e respostas estarão disponíveis para acessá-las, de forma organizada, tendo acesso através do menu, as 4 principais visões do negócio.

# 4. Top 3 Insights de Dados

1. A Índia é disparada o País com mais restaurantes cadastrados, representando 45% do total de restaurantes no mundo. Isso mostra uma grande concentração em apenas um país
2. Fora da Índia, a concentração de restaurantes cadastrados estão nos grandes centros de cada país, com destaque pra Birmingham e Doha, sendo as duas cidades com o maior número
3. A percepção de tipo de culinária muda muito de acordo com a geografia, podendo uma culinária performar bem em um país e mal em outro

# 5. O Produto Final do Projeto

Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet.
O painel pode ser acessado através desse link: [https://project-currycompany.streamlit.app/](https://fome-zero-company-projeto-final.streamlit.app/)

# 6. Conclusão

O objetivo desse projeto foi criar um conjunto de gráficos e tabelas para municiar da melhor maneira o CEO, afim de usar os dados para conhecer melhor a Fome Zero Company e tomar as melhores decisões.

A empresa por ser mundial, está nos grandes centros  de alguns países mas, concentra-se principalmente na Índia. 

# 7. Próximo Passo

1. Fazer cruzamentos para entender melhor as relações culinárias/notas/países
2. Fazer cruzamentos para entender melhor as relações preços/notas/países
3. Criar novos filtros.
4. Adicionar novas visões de negócio.
