import os

# --- CONFIGURAÇÕES PARA OS BADGES (Corrigido) ---
URL_BASE_NO_SERVIDOR = "/imagens/badges/"
NOME_DA_TABELA = "Badge"

# Nomes das colunas conforme você especificou
COLUNA_NOME = "nome"
COLUNA_REQUISITO = "requisito"
COLUNA_ICONE = "icone" # Atualizei de 'caminho_foto' para 'icone'

# !! ATENÇÃO: Valor padrão para a coluna 'requisito' !!
# Edite esta string se quiser um valor padrão diferente de vazio.
VALOR_PADRAO_REQUISITO = "" 

CAMINHO_DA_PASTA_LOCAL = r"/home/iasmin/Documentos/Estudos/xpLearn/xplearn-backend/xplearn-backend/app/static/imagens/badges"
# ------------------------------------

def gerar_sql_inserts():
    """
    Gera comandos SQL INSERT (nome, requisito, icone) a partir dos
    arquivos de imagem encontrados no CAMINHO_DA_PASTA_LOCAL.
    """
    comandos_sql = []

    try:
        nomes_dos_arquivos = os.listdir(CAMINHO_DA_PASTA_LOCAL)
    except FileNotFoundError:
        print(f"Erro: Pasta não encontrada em:")
        print(f"{CAMINHO_DA_PASTA_LOCAL}")
        print("Por favor, verifique se a constante CAMINHO_DA_PASTA_LOCAL está correta.")
        return

    # Filtra apenas arquivos de imagem
    arquivos_de_imagem = [f for f in nomes_dos_arquivos if f.endswith(('.png', '.jpg', '.jpeg', '.webp', '.svg'))]

    if not arquivos_de_imagem:
        print(f"Nenhum arquivo de imagem encontrado em {CAMINHO_DA_PASTA_LOCAL}")
        return

    arquivos_de_imagem.sort()

    # Atualiza a declaração INSERT para incluir as 3 colunas
    comandos_sql.append(f"INSERT INTO {NOME_DA_TABELA} ({COLUNA_NOME}, {COLUNA_REQUISITO}, {COLUNA_ICONE}) VALUES")

    valores = []
    for nome_arquivo in arquivos_de_imagem:
        
        # --- Lógica de nome (ex: 'H-comportamento.fw.png') ---
        nome_base = nome_arquivo.split('.')[0]
        
        nome_limpo = (
            nome_base.replace(' ', '')
            .replace('_', '')
            .replace('-', '')
            .replace('(', '')
            .replace(')', '')
        )
        nome_amigavel = nome_limpo.capitalize()
        # --------------------------------------------------------

        url_final_no_banco = f"{URL_BASE_NO_SERVIDOR}{nome_arquivo}"
        
        # Adiciona o valor padrão do requisito no insert
        valores.append(f"('{nome_amigavel}', '{VALOR_PADRAO_REQUISITO}', '{url_final_no_banco}')")

    comandos_sql.append(",\n".join(valores) + ";")

    nome_arquivo_saida = "inserts_de_badges_gerados.sql"
    with open(nome_arquivo_saida, "w", encoding="utf-8") as f:
        f.write("\n".join(comandos_sql))

    print(f"✅ Sucesso! {len(arquivos_de_imagem)} registros foram gerados e salvos em:")
    print(f"{os.path.abspath(nome_arquivo_saida)}")
    print("\n⚠️ Lembrete: Você precisa editar o arquivo SQL gerado para preencher a coluna 'requisito' de cada badge.")

if __name__ == "__main__":
    gerar_sql_inserts()