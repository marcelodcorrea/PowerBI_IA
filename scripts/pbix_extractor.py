#!/usr/bin/env python3
"""
Extrai arquivo PBIX em JSONs de layout.

Uso:
    python pbix_extractor.py relatorio.pbix [--output-dir ./extracted/]
"""

import sys
import zipfile
import os
import argparse
from pathlib import Path


def extract_pbix(pbix_file, output_dir="./extracted"):
    """
    Descompacta PBIX e extrai JSONs de layout.
    
    Args:
        pbix_file: Caminho do arquivo PBIX
        output_dir: Diretório de saída
        
    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        # Validar arquivo
        if not os.path.exists(pbix_file):
            print(f"❌ Erro: Arquivo '{pbix_file}' não encontrado")
            return False
            
        if not pbix_file.endswith('.pbix'):
            print(f"❌ Erro: Arquivo deve ser .pbix")
            return False
        
        # Criar diretório de saída
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Descompactar
        print(f"⏳ Descompactando {pbix_file}...")
        with zipfile.ZipFile(pbix_file, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        
        # Verificar estrutura
        print(f"✓ PBIX descompactado")
        print(f"✓ Arquivos extraídos para: {output_dir}")
        print(f"✓ Estrutura:")
        
        # Listar principais arquivos
        report_dir = os.path.join(output_dir, 'report')
        if os.path.exists(report_dir):
            print(f"  ├── report/")
            definition_dir = os.path.join(report_dir, 'definition')
            if os.path.exists(definition_dir):
                print(f"  │   ├── definition/")
                pages_dir = os.path.join(definition_dir, 'pages')
                if os.path.exists(pages_dir):
                    page_count = len(os.listdir(pages_dir))
                    print(f"  │   │   └── {page_count} página(s)")
        
        print(f"\n✅ Sucesso! Pronto para editar com VSCode.")
        print(f"\n   Próximo passo:")
        print(f"   1. code . (abra VSCode)")
        print(f"   2. Solicite mudança ao Claude")
        print(f"   3. Recompacte com: python scripts/pbix_recompactor.py extracted/ novo.pbix")
        
        return True
        
    except zipfile.BadZipFile:
        print(f"❌ Erro: {pbix_file} não é um arquivo PBIX válido")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Extrai arquivo PBIX em JSONs de layout"
    )
    parser.add_argument(
        "pbix_file",
        help="Arquivo PBIX a descompactar"
    )
    parser.add_argument(
        "--output-dir",
        default="./extracted",
        help="Diretório de saída (padrão: ./extracted)"
    )
    
    args = parser.parse_args()
    
    success = extract_pbix(args.pbix_file, args.output_dir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
