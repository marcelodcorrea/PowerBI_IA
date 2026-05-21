# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Extrai arquivo PBIX em arquivos JSON de layout.

Uso:
    python pbix_extractor.py relatorio.pbix
    python pbix_extractor.py relatorio.pbix --output-dir ./extracted/
"""

import sys
import io
import zipfile
import json
import os
import argparse
from pathlib import Path

try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
except AttributeError:
    pass


def format_size(size_bytes):
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / 1024 / 1024:.1f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes} B"


def extract_pbix(pbix_file, output_dir="./extracted"):
    try:
        pbix_path = Path(pbix_file)

        if not pbix_path.exists():
            print(f"[ERRO] Arquivo '{pbix_file}' nao encontrado")
            return False

        if pbix_path.suffix.lower() != '.pbix':
            print(f"[ERRO] Arquivo deve ter extensao .pbix")
            return False

        if not zipfile.is_zipfile(pbix_file):
            print(f"[ERRO] '{pbix_file}' nao e um arquivo PBIX valido (ZIP invalido)")
            return False

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        file_size = format_size(pbix_path.stat().st_size)
        print(f"[INFO] Arquivo:  {pbix_file} ({file_size})")
        print(f"[INFO] Destino:  {output_dir}")

        with zipfile.ZipFile(pbix_file, 'r') as zf:
            entries = zf.namelist()
            zf.extractall(output_dir)

        # Contar paginas e visuais atraves da estrutura de diretorios extraida
        page_guids = set()
        visual_count = 0

        for root, dirs, files in os.walk(output_dir):
            root_path = Path(root)
            parts = root_path.parts

            for filename in files:
                if filename == 'visual.json':
                    visual_count += 1
                    # Subir na arvore para achar o guid da pagina (pasta apos 'pages')
                    for i, part in enumerate(parts):
                        if part.lower() == 'pages' and i + 1 < len(parts):
                            page_guids.add(parts[i + 1])
                            break

        print(f"[OK]  Arquivos extraidos: {len(entries)}")
        print(f"[OK]  Paginas encontradas: {len(page_guids)}")
        print(f"[OK]  Visuais encontrados: {visual_count}")
        print(f"[OK]  Extracao concluida.")
        print()
        print(f"Proximo passo:")
        print(f"  1. Edite os visual.json em: {output_dir}")
        print(f"  2. Recompacte com:")
        print(f"     python scripts/pbix_recompactor.py {output_dir} saida.pbix --original {pbix_file}")

        return True

    except zipfile.BadZipFile:
        print(f"[ERRO] '{pbix_file}' nao e um arquivo ZIP/PBIX valido")
        return False
    except PermissionError as e:
        print(f"[ERRO] Sem permissao de escrita: {e}")
        return False
    except Exception as e:
        print(f"[ERRO] {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Extrai arquivo PBIX em JSONs de layout"
    )
    parser.add_argument("pbix_file", help="Arquivo PBIX a extrair")
    parser.add_argument(
        "--output-dir",
        default="./extracted",
        help="Diretorio de saida (padrao: ./extracted)"
    )

    args = parser.parse_args()
    success = extract_pbix(args.pbix_file, args.output_dir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
