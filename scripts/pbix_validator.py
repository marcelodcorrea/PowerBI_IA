#!/usr/bin/env python3
"""
Valida integridade de arquivo PBIX.

Uso:
    python pbix_validator.py relatorio.pbix
"""

import sys
import zipfile
import os
import json
import argparse


def validate_pbix(pbix_file):
    """
    Valida integridade de arquivo PBIX.
    
    Args:
        pbix_file: Caminho do arquivo PBIX
        
    Returns:
        bool: True se válido, False se inválido
    """
    try:
        print(f"⏳ Validando {pbix_file}...")
        
        # Validar arquivo
        if not os.path.exists(pbix_file):
            print(f"❌ Erro: Arquivo '{pbix_file}' não encontrado")
            return False
        
        if not pbix_file.endswith('.pbix'):
            print(f"❌ Erro: Arquivo deve ser .pbix")
            return False
        
        # Validar ZIP
        if not zipfile.is_zipfile(pbix_file):
            print(f"❌ Erro: Arquivo não é PBIX válido (não é ZIP)")
            return False
        
        # Validar estrutura interna
        with zipfile.ZipFile(pbix_file, 'r') as zip_ref:
            # Verificar se tem arquivos de relatório
            files = zip_ref.namelist()
            
            # Verificar estrutura básica
            has_report = any('report' in f for f in files)
            has_model = any('semanticModel' in f for f in files)
            
            if not has_report:
                print(f"⚠️  Aviso: Estrutura de 'report' não encontrada")
            
            if not has_model:
                print(f"⚠️  Aviso: Estrutura de 'semanticModel' não encontrada")
            
            # Contar páginas
            pages = [f for f in files if 'pages' in f and 'visual.json' in f]
            
            print(f"✓ PBIX válido")
            print(f"✓ Estrutura OK")
            print(f"✓ Arquivos: {len(files)}")
            if pages:
                print(f"✓ Páginas: {len(set(p.split('/')[:-1] for p in pages))}")
            
            print(f"\n✅ Arquivo validado com sucesso")
            return True
        
    except zipfile.BadZipFile:
        print(f"❌ Erro: {pbix_file} não é um arquivo PBIX válido")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Erro: JSON inválido - {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Valida integridade de arquivo PBIX"
    )
    parser.add_argument(
        "pbix_file",
        help="Arquivo PBIX a validar"
    )
    
    args = parser.parse_args()
    
    success = validate_pbix(args.pbix_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
