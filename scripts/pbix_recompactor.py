# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Recompacta arquivos JSON editados em um arquivo PBIX valido.

Uso:
    python pbix_recompactor.py extracted/ saida.pbix --original original.pbix

Nota sobre SecurityBindings:
    O Power BI armazena neste arquivo uma assinatura DPAPI do conteudo do relatorio.
    Qualquer alteracao nos JSONs invalida essa assinatura. Por isso, o script zera
    o SecurityBindings ao recompactar. O Power BI Desktop abre normalmente sem ele.
"""

import sys
import io
import zipfile
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


def detectar_modificados(extracted_dir, original_pbix):
    """
    Compara conteudo dos arquivos extraidos com o original.
    Retorna dict: {arcname: bytes_novo_conteudo} para arquivos alterados.
    """
    modified = {}

    with zipfile.ZipFile(original_pbix, 'r') as orig:
        for item in orig.infolist():
            filepath = Path(extracted_dir) / item.filename.replace('/', os.sep)
            if filepath.exists():
                novo = filepath.read_bytes()
                original = orig.read(item.filename)
                if novo != original:
                    modified[item.filename] = novo

    return modified


def recompactar(extracted_dir, output_file, original_pbix):
    try:
        if not os.path.exists(extracted_dir):
            print(f"[ERRO] Diretorio '{extracted_dir}' nao encontrado")
            return False

        if not os.path.exists(original_pbix):
            print(f"[ERRO] PBIX original '{original_pbix}' nao encontrado")
            return False

        if not zipfile.is_zipfile(original_pbix):
            print(f"[ERRO] '{original_pbix}' nao e um arquivo PBIX valido")
            return False

        print(f"[INFO] Carregando arquivos de: {extracted_dir}")
        print(f"[INFO] PBIX original: {original_pbix}")

        modified = detectar_modificados(extracted_dir, original_pbix)

        # Relatar apenas arquivos realmente modificados (excluir SecurityBindings do relatorio)
        mod_report = [k for k in modified if k != 'SecurityBindings']
        print(f"[INFO] Arquivos modificados detectados: {len(mod_report)}")
        for fname in mod_report:
            print(f"  - {fname}")
        # Novos arquivos sao reportados apos o loop principal

        if os.path.exists(output_file):
            os.remove(output_file)

        with zipfile.ZipFile(original_pbix, 'r') as orig:
            entries = orig.infolist()

            # DataModel vai por ultimo com ZIP_STORED
            normais = [item for item in entries if item.filename != 'DataModel']
            datamodel = next((item for item in entries if item.filename == 'DataModel'), None)

            with zipfile.ZipFile(output_file, 'w') as out:

                for item in normais:

                    if item.filename == 'SecurityBindings':
                        # CRITICO: zerar assinatura DPAPI.
                        # Qualquer modificacao de conteudo invalida o hash original.
                        # O Power BI Desktop abre normalmente sem a assinatura.
                        out.writestr(item, b'')

                    elif item.filename in modified:
                        # Usar novo conteudo, preservando metadados ZIP do item original
                        out.writestr(item, modified[item.filename])

                    else:
                        # Arquivo inalterado: copiar como esta
                        out.writestr(item, orig.read(item.filename))

                # Arquivos novos: existem em extracted/ mas nao no PBIX original
                original_arcnames = {item.filename for item in entries}
                for root, _, files in os.walk(extracted_dir):
                    for file in files:
                        filepath = Path(root) / file
                        arcname = str(filepath.relative_to(extracted_dir)).replace(os.sep, '/')
                        if arcname not in original_arcnames:
                            out.write(str(filepath), arcname)
                            modified[arcname] = None  # registrar para relatorio

                # DataModel por ultimo (ZIP_STORED, sem compressao)
                if datamodel:
                    datamodel.compress_type = zipfile.ZIP_STORED
                    out.writestr(datamodel, orig.read('DataModel'))

        size_str = format_size(os.path.getsize(output_file))
        print(f"[INFO] SecurityBindings zerado (assinatura DPAPI removida)")
        print(f"[INFO] DataModel adicionado por ultimo (ZIP_STORED)")
        print(f"[OK]  PBIX gerado: {output_file} ({size_str})")
        print(f"[OK]  Concluido. Arquivo pode ser aberto no Power BI Desktop.")
        return True

    except zipfile.BadZipFile:
        print(f"[ERRO] ZIP invalido: verifique se o arquivo original e um PBIX valido")
        return False
    except PermissionError as e:
        print(f"[ERRO] Sem permissao: {e}")
        return False
    except Exception as e:
        print(f"[ERRO] {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Recompacta JSONs editados em arquivo PBIX"
    )
    parser.add_argument("extracted_dir", help="Diretorio com arquivos extraidos")
    parser.add_argument("output_file", help="Arquivo PBIX de saida")
    parser.add_argument(
        "--original",
        required=True,
        help="PBIX original (referencia de metadados ZIP)"
    )

    args = parser.parse_args()
    success = recompactar(args.extracted_dir, args.output_file, args.original)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
