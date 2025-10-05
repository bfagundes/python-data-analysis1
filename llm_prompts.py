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

"""
Roteiro de diagnóstico de internacionalização:

Você é um analista de dados que trabalha em uma consultoria especializada na internacionalização de instituições de ensino superior e em educação internacional. Esta consultoria possui mais de 30 anos de experiência e trabalha com uma rede global de especialistas. 

Atualmente você está atuando em um cliente auxiliando no processo de inscrição de proposta para o programa CAPES-Global. Você aplicou um questionário para coletar respostas sobre a percepção dos diretores de cada instituição do grupo com relação à internacionalização. Em anexo, as perguntas feitas (coluna B) e, ao lado (coluna A), a letra correspondente à coluna da planilha onde se encontram as respostas do questionário. 

Você poderia elaborar um roteiro de diagnóstico o mais completo possível para que a alta direção do grupo universitário consiga aplicar a inscrição ao programa CAPES-Global?
Por favor, insira quais perguntas devem contemplar cada sessão e qual a letra da coluna correspondente desta coluna.

Você deve pensar como um analista de dados sênior, especialista em educação

Interpretação de gráfico:
Chat, como parte desse relatório, utilizaremos gráficos para ilustrar os percentuais de cada resposta de algumas perguntas. Cada gráfico precisa estar devidamente identificado com:

Título: Acima do gráfico, precedido por "Figura", número e travessão. O título deve ser claro e descritivo, permitindo que o leitor compreenda a informação que será apresentada sem precisar consultar o texto
Texto analítico: Parágrafo interpretativo para acompanhar a Figura, no estilo analítico e textual corrido

Para compor o diagnóstico de internacionalização a ser apresentado para executivos da instituição em questão, pensando como um analista de dados senior, especialista em educação, você deve fazer a interpretação e me encaminhar um texto analítico para cada gráfico encaminhado a partir de agora. 

Depois do primeiro gráfico importado, utilizar apenas a parte abaixo: 
O gráfico em anexo corresponde aos dados da pergunta: o que é internacionalização para você?, que corresponde à sessão “Perfil Institucional e Estrutura Acadêmica”.

Interpretação de dados sem gráficos:
Chat, algumas perguntas não resultaram em gráficos, mas ainda assim seus dados precisam ser analisados e apresentados no estilo analítico e textual corrido.
A seguir, vou encaminhar a seção do relatório, junto com as perguntas e respostas que a compõem, você poderia me encaminhar um texto analítico corrido, integrado por seção, costurando todas as perguntas, com ênfase interpretativa e não apenas descritiva?

O texto da análise deve começar de forma mais direta e interpretativa, sem a expressão “os resultados dessa seção”, por exemplo

Categorias de: O que te motivou a participar da experiência internacional?
Chat, considerando que abaixo temos as categorias da pergunta: O que te motivou a participar da experiência internacional?, classifique as respostas em anexo na categoria que melhor se encaixa e me encaminhe em excel. 

Desenvolvimento Acadêmico – busca por conhecimento e atualização científica.
Pesquisa – novas possibilidades, projetos, colaboração científica.
Internacionalização – desejo de internacionalizar a carreira ou instituição.
Ampliação de Rede/Networking – contatos, parcerias internacionais.
Formação Pessoal e Profissional – enriquecimento geral, experiências formativas.
Diferencial Curricular – melhorar o currículo, destaque no mercado acadêmico.
Intercâmbio Cultural – conhecer novas realidades, culturas acadêmicas.
Ensino – desenvolver ou participar de atividades de ensino internacional.
Colaboração com Pesquisadores Estrangeiros – diálogo e trabalho conjunto.
Abertura de Horizontes – novas visões, descobertas, experiências.
Continuidade de Experiências Anteriores – quem já fez intercâmbio ou estágio.
Latinoamericanismo – foco em integração ou cooperação com a América Latina.
Outros/Motivação Genérica – respostas vagas ou pouco específicas.

Categorias de: O que é internacionalização do ensino superior para você?
Chat, considerando que abaixo temos as categorias da pergunta: O que é internacionalização do ensino superior para você?, classifique as respostas em anexo na categoria que melhor se encaixa e me encaminhe em excel. 

Troca de Conhecimento/Experiências – compartilhamento de saberes, vivências e metodologias.
Colaboração Acadêmica Internacional – projetos, redes, publicações e coautorias entre países.
Mobilidade Acadêmica – envio e recebimento de alunos/professores.
Currículo e Ensino Internacionalizado – inclusão de temas globais nos currículos.
Intercâmbio Cultural – contato com outras culturas e realidades educacionais.
Abertura Institucional ao Mundo – visão estratégica de abertura da universidade.
Integração de Instituições/Redes – cooperação institucional entre universidades.
Desenvolvimento Científico Global – avanço da ciência em contexto internacional.
Formação Crítica/Global do Estudante – preparar o aluno para o mundo globalizado.
Uso de Idiomas Estrangeiros – práticas de ensino e pesquisa em outros idiomas.
Tecnologias e Plataformas Internacionais – uso de ambientes virtuais e ferramentas globais.
Fomento Governamental/Institucional – políticas públicas e institucionais de incentivo.
Visão Ampla/Genérica sobre Internacionalização – respostas vagas, abrangentes ou filosóficas.

Categorias de: O que te motivou a participar das ações de internacionalização da universidade?
Desenvolvimento Acadêmico – busca por conhecimento, atualização científica, crescimento intelectual.
Pesquisa – novas possibilidades de pesquisa, produção científica, projetos colaborativos.
Internacionalização – interesse em integrar-se a processos ou redes internacionais.
Ampliação de Rede/Networking – contatos, parcerias, cooperação com outras instituições ou pesquisadores.
Formação Pessoal e Profissional – enriquecimento pessoal, crescimento geral, experiências formativas.
Diferencial Curricular – destaque no currículo, vantagem competitiva.
Intercâmbio Cultural – conhecer outras culturas, diversidade cultural.
Ensino – ações ligadas à docência, métodos e práticas de ensino.
Colaboração com Pesquisadores Estrangeiros – cooperação acadêmica internacional direta.
Abertura de Horizontes – novas perspectivas, expansão de visão.
Continuidade de Experiências Anteriores – extensão de ações já vividas ou iniciadas.
Engajamento Político e Ético – luta por causas, justiça, representatividade.
Outros/Motivação Genérica – respostas vagas ou que não se encaixam claramente nas demais.

Categorias de: Porque não participou das ações de internacionalização da universidade?
Falta de oportunidade – respostas que indicam que ainda não houve chance, chamada, ou abertura.
Desconhecimento das Ações/Processos – falta de informação sobre programas, requisitos ou existência das ações.
Barreira Linguística – falta de fluência em idiomas, principalmente o inglês.
Tempo/Agenda/Sobrecarga – falta de tempo, excesso de trabalho, rotinas que impedem participação.
Ingressante Recente – entrou recentemente no programa ou instituição.
Sem Vínculo Institucional Formal – professores aposentados ou não concursados.
Foco em Outras Atividades Acadêmicas – envolvidos em outros projetos ou funções acadêmicas.
Falta de Rede Internacional – ausência de contatos ou conexões no exterior.
Desmotivação ou Falta de Interesse – ausência de atrativos, interesse ou estímulo.
Aguardando Melhor Momento – planejamento para participar futuramente.
Participação Limitada/Experiência Pontual – já participou, mas apenas de forma isolada.
Atuação Restrita à Pós-Graduação – docentes com atuação limitada a um nível de ensino.
Outros – respostas vagas ou que não se encaixam nas anteriores.

Categorias de: O que o motivaria a participar de ações de internacionalização?
Desenvolvimento Acadêmico – aquisição de conhecimento, qualificação científica, formação continuada.
Pesquisa – interesse em publicações, projetos colaborativos e cooperação científica.
Intercâmbio Cultural – conhecer novas culturas, realidades educacionais ou sociais.
Ampliação de Rede/Networking – contato com outros pesquisadores e instituições.
Ensino – interesse em lecionar no exterior, atuar em outros idiomas ou ambientes educacionais.
Apoio Financeiro/Institucional – incentivos, bolsas, disponibilidade de recursos.
Formação no Exterior/Estágios – pós-doc, cursos, intercâmbios, congressos.
Domínio de Idiomas – aprender ou praticar línguas estrangeiras.
Formação Docente – melhorar currículo docente, beneficiar alunos, novas práticas pedagógicas.
Visibilidade Internacional – ampliar o alcance da produção acadêmica e científica.
Outros – respostas genéricas, vagas ou de difícil categorização.
Fórmula de: Na sua opinião, qual a importância da internacionalização para a sua instituição?
=SE([@[Na sua opinião, qual a importância da internacionalização para a sua instituição?]]=5;"Muito Importante";
SE([@[Na sua opinião, qual a importância da internacionalização para a sua instituição?]]=4;"Importante";
SE([@[Na sua opinião, qual a importância da internacionalização para a sua instituição?]]=3;"Razoavelmente Importante";
SE([@[Na sua opinião, qual a importância da internacionalização para a sua instituição?]]=2;"Pouco Importante";
SE([@[Na sua opinião, qual a importância da internacionalização para a sua instituição?]]=1;"Sem Importância";"")))))







CAPES:

O Programa Redes para Internacionalização Institucional – CAPES-Global.Edu com a finalidade de fomentar a criação de redes de cooperação entre instituições nacionais com estágios de internacionalização diversos para promover, por meio da cooperação internacional, o desenvolvimento de atividades estratégicas de pesquisa e pós-graduação dos participantes. 

O objetivo geral consiste em contribuir para o fortalecimento do protagonismo internacional do Brasil e consolidar sua posição como parceiro estratégico em iniciativas globais, além de promover a cooperação mútua, o diálogo intercultural e o desenvolvimento sustentável. 

Objetivo específicos 
I - promover parcerias entre instituições nacionais, de diferentes regiões do País e com diferentes estágios de internacionalização, visando a cooperação internacional e a aprendizagem mútua com instituições do Norte e do Sul Global; 

II - incentivar a construção, a implementação e a consolidação de planos estratégicos de internacionalização das instituições participantes, articulados com os respectivos Planos de Desenvolvimento Institucional – PDI; 

III - estimular a colaboração com organizações da sociedade civil, visando ampliar a relevância institucional em seu contexto. Este objetivo engloba ações com foco no ensino, pesquisa, extensão, inovação, liderança, empreendedorismo, economia criativa, sustentabilidade econômica, consciência social e ambiental; 

IV - promover oportunidades de experiência internacional, no Brasil e no Exterior, para pós-graduandos, pesquisadores, docentes e técnicos, visando a qualificação de profissionais de nível superior e o aumento da cooperação no ensino, na pesquisa, extensão e inovação nos cenários nacional e internacional; 

V - promover a cultura para a internacionalização que seja diversa, inclusiva e acolhedora nas Instituições participantes das redes; e 

VI - estimular o aprimoramento da governança da internacionalização nas IES/IP, assim como a formação de profissionais para a gestão internacional. 

Você é um analista de dados que trabalha como consultora especializada na internacionalização de instituições de ensino superior e em educação internacional. Esta consultoria possui mais de 30 anos de experiência e trabalha com uma rede global de especialistas. 

Atualmente você está atuando em um cliente auxiliando no processo de inscrição de proposta para o programa CAPES-Global. Você aplicou um questionário para coletar respostas sobre a percepção dos diretores de cada instituição do grupo com relação à internacionalização. Em anexo, as perguntas feitas (coluna B) e, ao lado (coluna A), a letra correspondente à coluna da planilha onde se encontram as respostas do questionário. 

Você poderia elaborar um roteiro de diagnóstico o mais completo possível para que a alta direção do grupo universitário consiga aplicar a inscrição ao programa CAPES-Global?
Por favor, insira quais perguntas devem contemplar cada sessão e qual a letra da coluna correspondente desta coluna.


Você deve pensar como um analista de dados sênior, especialista em educação
"""