# 📓 Tense Memo

**Tense Memo** é uma aplicação web para o estudo e a fixação de tempos (tenses) verbais da língua inglesa (*Past Simple* e *Past Participle*). Desenvolvido em **Python**, foi utilizado **Pandas** para o processamento dos dados e **Streamlit** para a criação da interface.

A ideia do projeto surgiu de uma necessidade real observada pela desenvolvedora em sua atuação como professora de inglês: a dificuldade que os estudantes enfrentam para memorizar verbos irregulares. A base teórica que justifica a escolha dos 100 verbos mais frequentes está detalhada na seção **Fundamentação Pedagógica**.

---

## 📊 Pipeline de Processamento de Dados

A lógica da escolha dos dados se baseia na frequência de uso no dia a dia para que o estudante foque em um conjunto estatisticamente relevante. A base final **`top_100_verbs.csv`** é construída por meio da integração de duas fontes:

1. **`word-frequency-coca.csv`**: Dados do **COCA** (*Corpus of Contemporary American English*). O COCA é um banco de dados linguístico abrangente e confiável do inglês, contendo bilhões de palavras retiradas de contextos reais (linguagem falada, ficção, revistas, jornais e textos acadêmicos). Assim, a seleção dos verbos do app se baseia em dados estatísticos da frequência de uso no dia a dia.
2. **`verbs-dictionary.csv`**: Dados de diferentes dicionários de inglês contendo as flexões verbais, desenvolvido pelo professor e programador [Wiktor Jakubczyc](https://github.com/monolithpl).

### Etapas do Tratamento (`data_processing.py`)
1 - O corpus COCA foi utilizado para identificar e isolar os 100 lemas verbais mais frequentes, removendo verbos modais e auxiliares sem conjugação.
2 - Cruzamento dos lemas filtrados com o dicionário de verbos para mapear as formas de Infinitivo, 3ª pessoa do singular, Past Simple, Past Participle e Present Participle.
3 - Inserção manual e correção de variações específicas para os verbos "do" e "to be".
4 - Limpeza de strings, remoção de verbos compostos hifenizados e de duplicados.

---

## 🏗️ Arquitetura

### 1. Camada ETL (`data_processing.py`)
Módulo independente que processa dados brutos e gera a base final para o consumo pelo app.

### 2. Camada de Interface (`app.py` via Streamlit)
- **Session State:** Controla fluxo, pontuação e sorteio de itens.
- **Componentização:** UI dividida em funções independentes (header, sidebar, quiz, feedback).
- **CSS Dinâmico:** Injeção via `f-strings` para feedback visual e animações em tempo real.
- **Cache:** Uso de `@st.cache_data` para carregamento de dados.
- **Formulários:** Validação de respostas via `st.form`.

---

## 🎓 Fundamentação Pedagógica

O desenvolvimento do **Tense Memo** é baseado em princípios científicos de aquisição de linguagem, com foco na metodologia de Paul Nation e na hipótese do Filtro Afetivo de Stephen Krashen. 

Segundo Nation, aprender as 2.000 palavras mais frequentes permite ao estudante entender cerca de 80% de qualquer conversa ou texto em inglês. Focando nos 100 verbos mais comuns, o app foca na prática dos principais verbos no menor tempo de estudo possível. 

O linguista também considera o estudo focado em formas e significados (como em quizzes) como um método eficiente para consolidar o vocabulário essencial. O formato de quiz favorece o aprendizado baseado em recuperação da forma verbal da memória, o que favorece a retenção de longo prazo.

Para complementar, Krashen, afirma que o aprendizado é otimizado quando o Filtro Afetivo do aluno está baixo. A interface do Tense Memo reduz a ansiedade e o medo de errar ao não aplicar punições por falhas, permitindo refazer o exercício e fornecendo feedback visual imediato e positivo (validação de acertos). Isso cria um ambiente de prática seguro e reduz a ansiedade.

---

## 🛠️ Tecnologias
- Python 3.x
- Streamlit
- Pandas

---

## 💻 Execução

```bash
git clone https://github.com/larisanti/tense-memo.git
pip install -r requirements.txt
python src/data_processing.py # caso queira modificar a lista de verbos
streamlit run src/app.py
```

## 📚 Referências
- **DAVIES, M.** *The Corpus of Contemporary American English (COCA)*. <https://www.english-corpora.org/coca/>
- **KRASHEN, S. D.** *Principles and Practice in Second Language Acquisition*. Pergamon Press, 1982.
- **NATION, I. S. P.** *Learning Vocabulary in Another Language*. Cambridge University Press, 2013.

---

### Acesse: [https://tense-memo.streamlit.app](https://tense-memo.streamlit.app)
