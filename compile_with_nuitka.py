#!/usr/bin/env python3
"""
QuasarProtect Advanced - Script de Compilação com Nuitka
=========================================================

Este script compila o servidor Python em um executável standalone
usando Nuitka, que oferece proteção adicional ao código fonte.

Requisitos:
- Python 3.11+
- Nuitka instalado: pip install nuitka
- Compilador C (gcc/clang no Linux/Mac, MSVC no Windows)

Uso:
    python compile_with_nuitka.py

O executável será gerado na pasta 'dist/' com o nome:
- Linux/Mac: quasar_server
- Windows: quasar_server.exe
"""

import os
import sys
import subprocess
import platform

def check_nuitka():
    """Verifica se Nuitka está instalado"""
    try:
        subprocess.run(['python', '-m', 'nuitka', '--version'], 
                      capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

def install_nuitka():
    """Instala Nuitka via pip"""
    print("📦 Instalando Nuitka...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'nuitka'], check=True)
        print("✅ Nuitka instalado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar Nuitka: {e}")
        return False

def compile_server():
    """Compila quasar_server.py com Nuitka"""
    print("🔧 Compilando QuasarProtect Advanced com Nuitka...")
    print("⚠️  Este processo pode levar alguns minutos...\n")
    
    # Opções de compilação Nuitka
    nuitka_options = [
        sys.executable,
        '-m', 'nuitka',
        '--standalone',                    # Gera executável standalone
        '--onefile',                       # Gera um único arquivo executável
        '--output-dir=dist',              # Diretório de saída
        '--assume-yes-for-downloads',     # Auto-confirma downloads necessários
        '--enable-plugin=anti-bloat',     # Otimização de tamanho
        '--show-progress',                # Mostra progresso da compilação
        '--warn-implicit-exceptions',     # Avisos de exceções
        '--warn-unusual-code',            # Avisos de código incomum
        '--prefer-source-code',           # Usa código fonte quando possível
        'quasar_server.py'
    ]
    
    # Adiciona opções específicas do Windows
    if platform.system() == 'Windows':
        nuitka_options.extend([
            '--windows-disable-console',   # Remove janela de console (opcional)
            '--windows-icon-from-ico=icon.ico'  # Ícone customizado (se existir)
        ])
    
    try:
        subprocess.run(nuitka_options, check=True)
        print("\n✅ Compilação concluída com sucesso!")
        print(f"📁 Executável gerado em: dist/")
        
        # Lista arquivos gerados
        if os.path.exists('dist'):
            files = os.listdir('dist')
            print("\n📦 Arquivos gerados:")
            for f in files:
                size = os.path.getsize(os.path.join('dist', f))
                size_mb = size / (1024 * 1024)
                print(f"  - {f} ({size_mb:.2f} MB)")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro durante a compilação: {e}")
        return False
    except FileNotFoundError:
        print("\n❌ Nuitka não encontrado. Tentando instalar...")
        if install_nuitka():
            return compile_server()  # Tenta compilar novamente
        return False

def main():
    print("=" * 60)
    print("  QuasarProtect Advanced - Compilação com Nuitka")
    print("=" * 60)
    print()
    
    # Verifica se o arquivo existe
    if not os.path.exists('quasar_server.py'):
        print("❌ Arquivo quasar_server.py não encontrado!")
        print("   Execute este script no diretório do projeto.")
        sys.exit(1)
    
    # Verifica/instala Nuitka
    if not check_nuitka():
        print("⚠️  Nuitka não está instalado")
        install = input("Deseja instalar Nuitka agora? (s/n): ")
        if install.lower() in ['s', 'sim', 'y', 'yes']:
            if not install_nuitka():
                print("\n❌ Falha ao instalar Nuitka. Abortando.")
                sys.exit(1)
        else:
            print("\n❌ Nuitka é necessário para compilar. Abortando.")
            sys.exit(1)
    
    # Compila o servidor
    if compile_server():
        print("\n" + "=" * 60)
        print("🎉 Compilação finalizada!")
        print("=" * 60)
        print("\n📖 Próximos passos:")
        print("  1. O executável está em: dist/")
        print("  2. Copie os arquivos HTML para o mesmo diretório do executável")
        print("  3. Execute o binário gerado")
        print("\n💡 Dica: O executável pode ser distribuído sem Python instalado!")
    else:
        print("\n❌ Compilação falhou. Verifique os erros acima.")
        sys.exit(1)

if __name__ == '__main__':
    main()
