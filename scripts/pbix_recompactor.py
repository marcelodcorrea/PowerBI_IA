#!/usr/bin/env python3
"""
Recompacta JSONs editados em arquivo PBIX.

Uso:
    python pbix_recompactor.py ./extracted/ novo.pbix
"""

import sys
import zipfile
import os
import argparse
from pathlib import Path


def recompact_pbix(extracted_dir, output_file):
    """
    Recompacta JSONs editados em PBIX.
    
    Args:
        extracted_dir: Diretório com arquivos descompactados
        output_file: Arquivo PBIX de saída
        
    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        # Validar diretório
        if not os.path.exists(extracted_dir):
            print(f"❌ Erro: Diretório '{extracted_dir}' não encontrado")
            return False
        
        # Remover arquivo de saída se existir (para não conflitar)
        if os.path.exists(output_file):
            os.remove(output_file)
        
        print(f"⏳ Recompactando PBIX...")
        
        # Recompactar
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(extracted_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, extracted_dir)
                    zipf.write(file_path, arcname)
        
        # Verificar sucesso
        file_size = os.path.getsize(output_file)
        print(f"✓ PBIX recompactado")
        print(f"✓ Arquivo: {output_file}")
        print(f"✓ Tamanho: {file_size / 1024:.1f} KB")
        print(f"\n✅ Sucesso! Pronto para publicar.")
        print(f"\n   Próximo passo:")
        print(f"   1. Suba o arquivo {output_file} no Power BI Service")
        print(f"   2. Ou abra no Power BI Desktop e publique")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Recompacta JSONs editados em arquivo PBIX"
    )
    parser.add_argument(
        "extracted_dir",
        help="Diretório com arquivos descompactados"
    )
    parser.add_argument(
        "output_file",
        help="Arquivo PBIX de saída"
    )
    
    args = parser.parse_args()
    
    success = recompact_pbix(args.extracted_dir, args.output_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
