from openai_module import generate_response
from helpers import get_question_list

def ask_ai(prompt: str) -> str:
    """
    Generic wrapper to call the active AI provider.
    For now, it delegates to OpenAI. In the future,
    swap out the import with another provider.
    """
    try:
        return generate_response(prompt)
    except Exception as e:
        return f"Failed to generate the response. Exception: {e}"
    
def get_report_building_prompt():
    questions_text = get_question_list()
    return f"""
    Você é um analista de dados sênior, especialista em internacionalização do ensino superior.
    Sua tarefa é elaborar um roteiro de diagnóstico institucional para apoiar a inscrição de uma rede universitária no programa CAPES-Global.

    Aqui estão as perguntas do questionário e suas colunas:
    {questions_text}

    Regras:
    - Estruture o documento em seções hierárquicas (Introdução, Metodologia, Diagnóstico, Resultados, Conclusão, Referências).
    - Para cada seção, indique claramente quais perguntas devem ser contempladas (use a letra da coluna e o texto da pergunta).
    - Sempre liste as perguntas no formato: "- [COLUNA] — [Texto da pergunta]"
    - Exemplo: "- A — Nome completo e sigla da IES"
    - Não use dois pontos, hífens simples ou qualquer outra marcação.
    - Inclua placeholders para gráficos e análises estatísticas.
    - Não responda às perguntas nem insira dados — apenas construa a estrutura detalhada do relatório.
    """

def get_section_analyzer_prompt(section_name: str, data: dict) -> str:
    data_str = "\n".join([f"- {k}: {v:.1f}%" for k, v in data.items()])
    
    return f"""
    Você é um analista de dados sênior, especialista em educação.
    Sua tarefa é escrever a análise textual e interpretativa da seção "{section_name}" 
    do relatório institucional, com base nos seguintes dados (em porcentagens):

    {data_str}

    Regras:
    - O texto deve ser formal, analítico e corrido (sem bullet points).
    - Comece direto, sem frases introdutórias como “os resultados mostram que...”.
    - Conecte os dados a implicações institucionais, oportunidades e desafios.
    - O texto deve ter entre 2 e 4 parágrafos.
    """