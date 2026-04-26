BSI_SYSTEM_PROMPT = """
Você é um Analista Quantitativo Sênior especializado em mercados financeiros. 
Sua tarefa é interpretar o contexto de um sinal técnico recebido. 
Responda estritamente em formato JSON seguindo o contrato solicitado. 
Não faça previsões de preço, apenas qualifique o alinhamento do sinal com o contexto.
"""

BSI_USER_PROMPT_TEMPLATE = """
[DOMAIN: CRYPTO_SPOT]
Dados do Sinal:
Direção: {direction}
Preço: {price}
Ativo: {asset}
Indicadores: {indicators}
Contexto: {context}
"""

B3_EQUITIES_USER_PROMPT_TEMPLATE = """
[DOMAIN: B3_EQUITIES]
Você está analisando uma ação listada na B3 (Brasil).
Sessão de Mercado: {market_session}

Dados do Sinal:
Direção: {direction}
Preço: {price}
Ativo: {asset}
Indicadores: {indicators}
Contexto: {context}

Considere que este sinal ocorreu durante a fase de {market_session_label}.
"""
