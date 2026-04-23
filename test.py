from solipsys import VaultClient, SemanticParser

def main():
    print("Inicializando o Cofre Solipsys...")
    vault = VaultClient(base_path="./meu_teste_vault")
    parser = SemanticParser()
    
    #Teste de PDF
    pdf_teste = "teste.pdf"
    
    doc_id = parser.process_and_ingest(client=vault, filepath=pdf_teste, macro_tag="#Conhecimento_Puro")
    
    print("\n--- TESTE DE RECUPERAÇÃO SEMÂNTICA ---")
    pergunta = "Oq define uma Ia conseguir ler um pdf?"
    print(f"Buscando por: '{pergunta}'")
    
    resultados = vault.search_semantic(query=pergunta, n_results=2)
    
    if not resultados:
        print("Nenhuma conexão matemática encontrada. Aumente o threshold ou faça perguntas melhores.")
        
    for i, res in enumerate(resultados, 1):
        print(f"\n[Resultado {i}] - Página {res['metadata']['page']}")
        print(f"Texto: {res['text']}...")
        print(f"Tags: {res['metadata']['tags']}")
        print(f"Distância: {res['distance']:.4f}")

if __name__ == "__main__":
    main()