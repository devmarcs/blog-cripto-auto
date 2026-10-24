"""
Gera o áudio da narração (MP3) dos roteiros em roteiros/ usando a API do Cartesia.

Uso:
  python narrar.py                     → narra todos os roteiros que ainda não têm MP3
  python narrar.py roteiros/x-longo.md → narra só esse arquivo (refaz se já existir)

Lê a seção "NARRAÇÃO COMPLETA" do Markdown, então dá para revisar/editar o texto
antes de gastar créditos. O MP3 sai ao lado do .md, com o mesmo nome.
"""
import os
import re
import sys
import glob
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "roteiros")
VOZ_PADRAO = "07b6f895-78b9-4921-8e10-8a21c99c2e8a"  # Rafael - Dynamic Speaker (pt-BR)
MODELO = "sonic-3"


def extrair_narracao(caminho: str) -> str:
    with open(caminho, encoding="utf-8") as f:
        texto = f.read()
    m = re.search(r"## NARRAÇÃO COMPLETA[^\n]*\n(.*?)\n## ", texto, re.S)
    if not m:
        raise ValueError(f"seção NARRAÇÃO COMPLETA não encontrada em {caminho}")
    return m.group(1).strip()


def gerar_audio(narracao: str, destino: str):
    corpo = {
        "model_id": MODELO,
        "transcript": narracao,
        "voice": {"mode": "id", "id": os.getenv("CARTESIA_VOICE_ID", VOZ_PADRAO)},
        "language": "pt",
        "output_format": {"container": "mp3", "sample_rate": 44100, "bit_rate": 128000},
    }
    req = urllib.request.Request(
        "https://api.cartesia.ai/tts/bytes",
        data=json.dumps(corpo).encode(),
        headers={
            "X-API-Key": os.getenv("API_VOICE"),
            "Cartesia-Version": "2025-04-16",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            audio = resp.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Cartesia respondeu {e.code}: {e.read().decode(errors='ignore')}")
    with open(destino, "wb") as f:
        f.write(audio)


def main():
    if not os.getenv("API_VOICE"):
        print("Defina API_VOICE no .env com a chave do Cartesia.")
        return

    if sys.argv[1:]:
        alvos = sys.argv[1:]
    else:
        alvos = [
            md for md in sorted(glob.glob(os.path.join(PASTA, "*.md")))
            if not os.path.exists(md[:-3] + ".mp3")
        ]
    if not alvos:
        print("Nenhum roteiro sem áudio em roteiros/.")
        return

    for md in alvos:
        narracao = extrair_narracao(md)
        destino = md[:-3] + ".mp3"
        print(f"Narrando ({len(narracao)} caracteres): {os.path.basename(md)}")
        gerar_audio(narracao, destino)
        print(f"  salvo em {destino}")


if __name__ == "__main__":
    main()
