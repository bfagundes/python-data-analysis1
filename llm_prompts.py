CREATE_REPORT = """
Você é um analista de dados sênior, especialista em internacionalização do ensino superior.  
Sua tarefa é elaborar um roteiro de diagnóstico institucional para apoiar a inscrição de uma rede universitária no programa CAPES-Global.  

Regras:  
- O roteiro deve ter uma linguagem formal e estruturada, como um relatório consultivo.  
- Estruture o documento em seções hierárquicas (Introdução, Metodologia, Diagnóstico, Resultados, Análises por tema, Conclusão, Referências).  
- Para cada seção, indique claramente quais perguntas do questionário devem ser contempladas (cite a letra da coluna e a pergunta).  
- Inclua espaços para inserção futura de gráficos e análises estatísticas.  
- Não responda às perguntas nem insira dados — apenas construa a estrutura detalhada do relatório, de forma lógica e organizada.  
"""

LLM_OUTPUT_SIMPLE = """
# Roteiro de Diagnóstico Institucional para Inscrição no Programa CAPES-Global

## Introdução
- **Objetivo do Diagnóstico**: Delimitar a importância da internacionalização no contexto das Instituições de Ensino Superior (IES) e apresentar o propósito do diagnóstico.
- **Contextualização**: A relevância da internacionalização e a importância do programa CAPES-Global para a melhoria da qualidade do ensino superior no Brasil.
- **Perguntas a serem contempladas**:
- A — Nome completo e sigla da IES
- B — Segmento da IES
- C — Tipo da IES
- D — Cidade em que a sede da IES está localizada

## Metodologia
- **Tipo de Coleta de Dados**: Descrever a abordagem utilizada para a coleta de dados (questionário, entrevistas, etc.).
- **População e Amostra**: Definir a população alvo e a amostra selecionada para o diagnóstico.
- **Ferramentas de Análise**: Indicar as ferramentas estatísticas e de análise que serão utilizadas.
- **Perguntas a serem contempladas**:
- F — Oferece cursos
- G — Número total de alunos matriculados (2024)
- H — Número de Professores
- I — Número de Técnicos Administrativos

## Diagnóstico
- **Análise da Internacionalização**: Avaliar a situação atual da internacionalização na IES.
- **Participação em Redes e Consórcios**: Identificar redes e consórcios internacionais em que a IES está inserida.
- **Estratégia de Internacionalização**: Examinar como a internacionalização é abordada no planejamento institucional.
- **Obstáculos à Internacionalização**: Identificar fatores que dificultam a internacionalização.
- **Perguntas a serem contempladas**:
- J — Possui alguma acreditação internacional
- K — Qual/Quais?
- L — Está posicionada em algum ranking internacional?
- M — Qual/Quais?
- N — Participa de alguma rede internacional
- O — Qual/Quais?
- P — Faz ou fez parte de algum consórcio internacional
- Q — Qual/Quais?
- R — A internacionalização está incluída no planejamento da IES?
- S — Quem é responsável pela internacionalização na instituição?
- T — Como você avalia o processo de internacionalização da sua instituição?
- AO — Indique quais dos seguintes fatores são obstáculos externos à internacionalização da sua instituição
- AP — Indique quais dos seguintes fatores são obstáculos internos à internacionalização de sua instituição.

## Resultados
- **Análise Estatística**: Apresentar gráficos e tabelas que sintetizem os dados coletados.
- **Atividades de Internacionalização**: Avaliar a frequência e a diversidade das atividades de internacionalização oferecidas.
- **Mobilidade Internacional**: Analisar os dados relacionados à mobilidade de alunos, professores e técnicos administrativos.
- **Projetos e Acordos de Cooperação**: Avaliar a quantidade e a qualidade dos acordos de cooperação internacionais.
- **Orçamento e Financiamento**: Analisar os dados financeiros relacionados à internacionalização.
- **Perguntas a serem contempladas**:
- U — Com que frequência são ofertadas as atividades de internacionalização em sua instituição? (todas as subcategorias listadas de V a EJ)
- AQ — Quantos acordos de cooperação sua instituição tem com parceiros internacionais?
- AR — Quantos acordos de cooperação internacional assinados nos últimos 8 anos resultaram em projetos de pesquisa, tecnologia, inovação, projetos de extensão e publicações acadêmicas?
- BG — Existe um orçamento institucional específico para internacionalização em sua instituição?
- BH — Qual a proporção do orçamento dedicado à internacionalização em relação ao orçamento total da instituição?

## Conclusão
- **Síntese dos Resultados**: Resumir as principais descobertas do diagnóstico.
- **Recomendações**: Propor ações e estratégias para melhorar a internacionalização da IES.
- **Sugestões Futuras**: Indicar áreas que necessitam de mais pesquisa ou desenvolvimento.
- **Perguntas a serem contempladas**:
- EO — Você tem alguma sugestão ou recomendação para melhorar a internacionalização em sua instituição?

## Referências
- **Literatura e Documentos**: Listar as fontes consultadas para elaborar o diagnóstico.
- **Documentos Institucionais**: Incluir referências a documentos internos que sustentem o diagnóstico.
"""

LLM_OUTPUT_BY_GROUPS = """
# Roteiro de Diagnóstico Institucional para Inscrição no Programa CAPES-Global

## Introdução
Nesta seção, será apresentado o contexto da internacionalização do ensino superior e a importância da participação no programa CAPES-Global. A introdução deve abordar a necessidade de um diagnóstico institucional para entender a situação atual da internacionalização na instituição.

- A — Por favor, informe a instituição à qual está afiliado(a)
- B — Qual é a sua área acadêmica ou faculdade à qual você pertence?
- C — O que é internacionalização do ensino superior para você?

## Metodologia
Serão descritas as abordagens e métodos utilizados para a coleta de dados, análise e interpretação das respostas ao questionário. É importante explicar como as perguntas foram selecionadas e como os dados serão tratados.

- D — Você tem experiência internacional?
- E — Qual foi a experiência?
- F — O que te motivou a participar?
- G — Por que você não teve experiência internacional?
- H — Você tem conexões internacionais (outras IES, redes, etc.)?
- I — Qual/Quais?
- J — Você fala outro idioma?
- K — Qual/Quais?

## Diagnóstico
Esta seção irá compilar as respostas do questionário, organizando as informações em temas relevantes para a internacionalização. Será feita uma análise qualitativa e quantitativa dos dados coletados.   

- N — Na sua opinião, qual a importância da internacionalização para a sua instituição?
- O — Você participa das ações de internacionalização da universidade?
- P — Que ações?
- Q — O que te motiva a participar?
- R — Por que não participa?
- S — O que o motivaria a participar de ações de internacionalização?
- T — Sente-se apoiado para desenvolver projetos de internacionalização?
- U — O que você recomendaria para avançar na internacionalização de sua instituição?
- V — Que ações de internacionalização acrescentariam valor à área acadêmica ou docente a que pertence?
- W — Você acha que é importante que os alunos tenham oportunidades internacionais?
- X — Você considera que sua instituição oferece oportunidades para o desenvolvimento de perspectivas internacionais para seus alunos?
- Y — Você considera que sua instituição oferece oportunidades para o desenvolvimento de perspectivas internacionais para seus professores?
- Z — Quais são as principais dificuldades associadas à questão da internacionalização, na sua opinião?
- AA — O que você acha que sua instituição poderia alcançar em termos de vantagens competitivas se avançasse na questão da internacionalização?

## Resultados
Aqui serão apresentados os dados coletados e as análises realizadas, com gráficos e tabelas que ilustram as respostas. A interpretação das informações deve ser clara e objetiva, permitindo uma compreensão das tendências e lacunas identificadas.

- AB — Você atua como pesquisador?
- AC — Você faz parte de uma rede internacional de pesquisa?
- AD — Qual/Quais?
- AE — Você já trabalhou em algum centro de pesquisa internacional?
- AF — Qual/Quais?
- AG — Você tem publicações internacionais?
- AH — Você participa de algum projeto de pesquisa internacional atualmente?
- AI — Qual/Quais?
- AJ — Participa de algum comitê ou associação internacional?
- AK — Qual/Quais?
- AL — Atua como professor convidado em alguma instituição internacional?
- AM — Qual/Quais?
- AN — Atua como editor ou participa de algum comitê editorial de algum periódico acadêmico?
- AO — Qual/Quais?
- AP — Possui alunos em cotutela internacional (in ou out)?
- AQ — Qual/Quais curso(s)?
- AR — Possui alguma patentes registrada ou com processo em andamento?
- AS — Qual/Quais?
- AT — Participa de alguma Rede de colaboração com setores não acadêmicos, setores econômicos e sociais, governos, representações da sociedade civil organizada e polos de desenvolvimento do Brasil?     
- AU — Qual/Quais?
- AV — Liste suas principais produções acadêmicas nos últimos 8 anos.

## Conclusão
A conclusão deve resumir os principais achados do diagnóstico e sugerir próximos passos para a instituição em relação à internacionalização. É importante destacar a relevância das ações propostas e a necessidade de um compromisso coletivo.

- AX — Você acha que sua instituição apoia o desenvolvimento de pesquisas internacionais?
- AY — Você atraiu recursos financeiros externos (nacionais ou internacionais) para a pesquisa em sua instituição?
- AZ — Qual/Quais?
- BA — Você tem conhecimento sobre como atrair recursos externos para pesquisa?
- BB — Que sugestões você daria para que sua instituição alcance níveis mais altos em pesquisa internacional?
- BC — Você tem conexões com alguma IES nacional ou internacional que recomendaria para participar da proposta da CAPES-Global junto à sua instituição?
- BD — Qual/Quais?
- BE — Sugestões
"""

LLM_OUTPUT_SECTION_ANALYSIS = """
"(Análise automática desativada nesta execução)"
"""