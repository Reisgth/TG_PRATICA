from fpdf import FPDF

# Criar um novo PDF para os 20 documentos adicionais de MARKETING
pdf_marketing_3 = FPDF()

# Função para adicionar documentos ao PDF
def adicionar_documentos_marketing(categoria, assunto, corpo):
    pdf_marketing_3.add_page()
    pdf_marketing_3.set_font("Arial", size=12)
    pdf_marketing_3.cell(200, 10, txt=categoria, ln=True, align="C")
    pdf_marketing_3.ln(10)
    pdf_marketing_3.multi_cell(0, 10, txt=f"Assunto: {assunto}\n\n{corpo}")

# 10 exemplos adicionais fictícios da área de MARKETING
documentos_marketing_3 = [
    ("MARKETING", "Proposta de Colaboração com Influenciadores Locais",
     "Prezada Diretoria,\n\nProponho uma colaboração com influenciadores locais para promover nossa nova linha de produtos. Acredito que isso pode aumentar nosso alcance na comunidade.\n\nAtenciosamente,\nRafael Pinto\nGerente de Marketing Digital"),

    ("MARKETING", "Solicitação de Criação de Conteúdo para Redes Sociais",
     "Prezada Equipe de Conteúdo,\n\nSolicito a criação de posts para redes sociais sobre as funcionalidades do nosso novo produto. Devem ser atrativos e informativos.\n\nAtenciosamente,\nSofia Martins\nAnalista de Mídias Sociais"),

    ("MARKETING", "Relatório de Tendências de Mercado",
     "Prezada Diretoria,\n\nSegue o relatório com as principais tendências de mercado que podem impactar nosso setor nos próximos meses. Recomendo uma análise mais aprofundada.\n\nAtenciosamente,\nRicardo Freitas\nAnalista de Marketing"),

    ("MARKETING", "Convite para Conferência de Marketing Digital",
     "Prezada Equipe,\n\nGostaria de convidar todos para a conferência de marketing digital que ocorrerá na próxima semana. É uma excelente oportunidade de aprendizado e networking.\n\nAtenciosamente,\nPatrícia Oliveira\nGerente de Marketing Digital"),

    ("MARKETING", "Solicitação de Aprovação para Anúncios em Revistas",
     "Prezada Diretoria,\n\nSolicito a aprovação dos anúncios que serão veiculados nas principais revistas do setor no próximo trimestre. Anexei as artes para apreciação.\n\nAtenciosamente,\nFelipe Gomes\nCoordenador de Publicidade"),

    ("MARKETING", "Relatório de Análise de Campanha de Email",
     "Prezada Equipe,\n\nSegue o relatório de análise da última campanha de email. Os dados mostram uma taxa de abertura de 35%, superior à média do setor.\n\nAtenciosamente,\nGustavo Rocha\nAnalista de Email Marketing"),

    ("MARKETING", "Proposta de Criação de Blog Corporativo",
     "Prezada Diretoria,\n\nProponho a criação de um blog corporativo para compartilhar conteúdos relevantes sobre nossa área de atuação. Isso pode aumentar nossa autoridade no mercado.\n\nAtenciosamente,\nAna Carolina\nEspecialista em Marketing de Conteúdo"),

    ("MARKETING", "Pedido de Aumento de Orçamento para Campanha de Anúncios",
     "Prezada Diretoria,\n\nSolicito um aumento no orçamento para a campanha de anúncios digitais, pois identificamos um retorno muito positivo nas primeiras semanas.\n\nAtenciosamente,\nRenato Souza\nGerente de Marketing Digital"),

    ("MARKETING", "Relatório de Resultados de Promoções em Redes Sociais",
     "Prezada Equipe,\n\nSegue o relatório com os resultados das promoções realizadas nas redes sociais. Notamos um aumento considerável no engajamento e nas vendas.\n\nAtenciosamente,\nTatiane Lima\nCoordenadora de Mídia Social"),

    ("MARKETING", "Proposta de Workshop sobre Marketing de Conteúdo",
     "Prezada Diretoria,\n\nGostaria de propor a realização de um workshop sobre marketing de conteúdo para a equipe. Acredito que isso ajudará a aprimorar nossas estratégias.\n\nAtenciosamente,\nLucas Almeida\nAnalista de Marketing de Conteúdo")
]

# Adicionar cada documento ao PDF
for documento in documentos_marketing_3:
    adicionar_documentos_marketing(*documento)

# Salvar o PDF
pdf_marketing_3.output("documentos_marketing_3.pdf")