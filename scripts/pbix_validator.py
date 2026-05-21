# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Valida integridade de arquivo PBIX.

Uso:
    python pbix_validator.py relatorio.pbix
"""

import sys
import io
import zipfile
import os
import json
import argparse

try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
except AttributeError:
    pass


def validate_pbix(pbix_file):
    try:
        print(f"[INFO] Validando {pbix_file}...")

        if not os.path.exists(pbix_file):
            print(f"[ERRO] Arquivo '{pbix_file}' nao encontrado")
            return False

        if not pbix_file.endswith('.pbix'):
            print(f"[ERRO] Arquivo deve ter extensao .pbix")
            return False

        if not zipfile.is_zipfile(pbix_file):
            print(f"[ERRO] Arquivo nao e PBIX valido (ZIP invalido)")
            return False

        with zipfile.ZipFile(pbix_file, 'r') as zip_ref:
            files = zip_ref.namelist()

            has_report = any('Report' in f or 'report' in f for f in files)
            has_model = 'DataModel' in files

            if not has_report:
                print(f"[AVISO] Estrutura de 'Report' nao encontrada")

            if not has_model:
                print(f"[AVISO] DataModel nao encontrado")

            visuals = [f for f in files if f.endswith('visual.json')]
            pages = set()
            for v in visuals:
                parts = v.split('/')
                if 'pages' in parts:
                    idx = parts.index('pages')
                    if idx + 1 < len(parts):
                        pages.add(parts[idx + 1])

            print(f"[OK]  PBIX valido")
            print(f"[OK]  Entradas ZIP: {len(files)}")
            print(f"[OK]  Paginas: {len(pages)}")
            print(f"[OK]  Visuais: {len(visuals)}")
            print(f"[OK]  Arquivo validado com sucesso")
            return True

    except zipfile.BadZipFile:
        print(f"[ERRO] '{pbix_file}' nao e um arquivo PBIX valido")
        return False
    except json.JSONDecodeError as e:
        print(f"[ERRO] JSON invalido: {e}")
        return False
    except Exception as e:
        print(f"[ERRO] {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Valida integridade de arquivo PBIX"
    )
    parser.add_argument("pbix_file", help="Arquivo PBIX a validar")

    args = parser.parse_args()
    success = validate_pbix(args.pbix_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
