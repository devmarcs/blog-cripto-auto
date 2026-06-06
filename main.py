"""
Uso:
  python main.py           → gera e publica um post
  python main.py --dry-run → apenas mostra o post, sem publicar
"""
import sys
from blog_agent import gerar_conteudo_post
from blogger_client import publicar_post


def main():
    dry_run = "--dry-run" in sys.argv

    try:
        post = gerar_conteudo_post()

        titulo = post["title"]
        conteudo = post["content"]
        labels = post.get("labels", [])

        print(f"\nTítulo: {titulo}")
        print(f"Tags: {', '.join(labels)}")
        print(f"Tamanho do conteúdo: {len(conteudo)} caracteres")

        if dry_run:
            print("\n--- MODO DRY-RUN: post não publicado ---")
            print("\nPRÉVIA DO CONTEÚDO:")
            print(conteudo[:500] + "...")
            return

        print("\nPublicando no Blogger...")
        url = publicar_post(titulo, conteudo, labels)
        print(f"Post publicado com sucesso!\nURL: {url}")

    except Exception as e:
        print(f"ERRO: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
