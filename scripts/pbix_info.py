# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Inspeciona um arquivo PBIX sem extrair tudo.
Exibe estrutura interna, paginas, visuais e status.

Uso:
    python pbix_info.py relatorio.pbix
"""

import sys
import io
import zipfile
import json
import argparse
from pathlib import Path

try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
except AttributeError:
    pass

COMPRESS_NAMES = {
    zipfile.ZIP_STORED: 'STORED',
    zipfile.ZIP_DEFLATED: 'DEFLATED',
    8: 'DEFLATED',
}


def format_size(size_bytes):
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / 1024 / 1024:.1f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes} B"


def inspecionar(pbix_file):
    try:
        pbix_path = Path(pbix_file)

        if not pbix_path.exists():
            print(f"[ERRO] Arquivo '{pbix_file}' nao encontrado")
            return False

        if not zipfile.is_zipfile(pbix_file):
            print(f"[ERRO] '{pbix_file}' nao e um arquivo PBIX valido (ZIP invalido)")
            return False

        file_size = pbix_path.stat().st_size

        with zipfile.ZipFile(pbix_file, 'r') as zf:
            entries = zf.infolist()
            namelist = zf.namelist()

            # Versao Power BI
            pbi_version = "desconhecida"
            if 'Version' in namelist:
                pbi_version = zf.read('Version').decode('utf-8', errors='replace').strip()

            print(f"\n=== INFORMACOES DO PBIX ===")
            print(f"Arquivo: {pbix_file}")
            print(f"Tamanho: {format_size(file_size)}")
            print(f"Versao Power BI: {pbi_version}")

            # Estrutura interna
            print(f"\n=== ESTRUTURA INTERNA ===")
            print(f"Total de entradas ZIP: {len(entries)}")

            visual_entries = [e for e in entries if e.filename.endswith('visual.json')]
            other_entries = [e for e in entries if not e.filename.endswith('visual.json')]

            for item in other_entries:
                ctype = COMPRESS_NAMES.get(item.compress_type, str(item.compress_type))
                size_str = format_size(item.file_size)
                print(f"  [{ctype:8s}] {item.filename} ({size_str})")

            if visual_entries:
                ctype = COMPRESS_NAMES.get(visual_entries[0].compress_type, str(visual_entries[0].compress_type))
                print(f"  [{ctype:8s}] visual.json (x{len(visual_entries)})")

            # Paginas e visuais
            print(f"\n=== PAGINAS E VISUAIS ===")

            # Coletar guids de paginas preservando ordem de aparicao
            page_guids = []
            seen = set()
            for item in entries:
                parts = item.filename.split('/')
                if 'pages' in parts:
                    idx = parts.index('pages')
                    if idx + 1 < len(parts):
                        guid = parts[idx + 1]
                        if guid and '.' not in guid and guid not in seen:
                            page_guids.append(guid)
                            seen.add(guid)

            print(f"Paginas encontradas: {len(page_guids)}")

            for i, page_guid in enumerate(page_guids, 1):
                # Tentar ler page.json para obter nome da pagina
                page_name = f"{page_guid[:16]}..."
                page_json_name = next(
                    (n for n in namelist if page_guid in n and n.endswith('page.json')),
                    None
                )
                if page_json_name:
                    try:
                        page_data = json.loads(zf.read(page_json_name).decode('utf-8'))
                        page_name = page_data.get('displayName', page_name)
                    except Exception:
                        pass

                # Visuais nessa pagina
                page_visuals = [e for e in entries if page_guid in e.filename and e.filename.endswith('visual.json')]

                print(f"  Pagina {i}: \"{page_name}\" (guid: {page_guid[:16]}...)")
                print(f"    Visuais: {len(page_visuals)}")

                # Contar tipos de visual
                type_count = {}
                for ve in page_visuals:
                    try:
                        vdata = json.loads(zf.read(ve.filename).decode('utf-8'))
                        vtype = vdata.get('visual', {}).get('visualType', 'unknown')
                        type_count[vtype] = type_count.get(vtype, 0) + 1
                    except Exception:
                        pass

                for vtype, count in sorted(type_count.items()):
                    print(f"      - {vtype} x{count}")

            # Status
            print(f"\n=== STATUS ===")

            if 'SecurityBindings' in namelist:
                sb_size = zf.getinfo('SecurityBindings').file_size
                if sb_size == 0:
                    print(f"[AVISO] SecurityBindings zerado (arquivo editado externamente — comportamento esperado)")
                else:
                    print(f"[OK]  SecurityBindings presente (assinatura DPAPI ativa, {sb_size} bytes)")
            else:
                print(f"[AVISO] SecurityBindings ausente")

            if 'DataModel' in namelist:
                model_size = format_size(zf.getinfo('DataModel').file_size)
                print(f"[OK]  DataModel presente ({model_size})")
            else:
                print(f"[AVISO] DataModel ausente")

            print(f"[OK]  Estrutura valida")
            print()
            return True

    except zipfile.BadZipFile:
        print(f"[ERRO] '{pbix_file}' nao e um arquivo ZIP/PBIX valido")
        return False
    except Exception as e:
        print(f"[ERRO] {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Inspeciona um arquivo PBIX sem extrair"
    )
    parser.add_argument("pbix_file", help="Arquivo PBIX a inspecionar")

    args = parser.parse_args()
    success = inspecionar(args.pbix_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
