import os
import pefile
import argparse
import sys

banner = '''                                                                                               
 @@@@@@    @@@@@@   @@@       @@@@@@@                  @@@@@@@   @@@@@@    @@@@@@   @@@       
@@@@@@@@  @@@@@@@   @@@       @@@@@@@@                 @@@@@@@  @@@@@@@@  @@@@@@@@  @@@       
@@!  @@@  !@@       @@!       @@!  @@@                   @@!    @@!  @@@  @@!  @@@  @@!       
!@!  @!@  !@!       !@!       !@!  @!@                   !@!    !@!  @!@  !@!  @!@  !@!       
@!@!@!@!  !!@@!!    @!!       @!@!!@!                    @!!    @!@  !@!  @!@  !@!  @!!       
!!!@!!!!   !!@!!!   !!!       !!@!@!                     !!!    !@!  !!!  !@!  !!!  !!!       
!!:  !!!       !:!  !!:       !!: :!!                    !!:    !!:  !!!  !!:  !!!  !!:       
:!:  !:!      !:!    :!:      :!:  !:!                   :!:    :!:  !:!  :!:  !:!   :!:      
::   :::  :::: ::    :: ::::  ::   :::  :::::::::::::     ::    ::::: ::  ::::: ::   :: ::::  
 :   : :  :: : :    : :: : :   :   : :  :::::::::::::     :      : :  :    : :  :   : :: : :  

 
 
 
 
 '''                                                                                              



def has_aslr_enabled(pe):
    """Verifica se o ASLR está ativado para o arquivo PE fornecido."""
    return bool(pe.OPTIONAL_HEADER.DllCharacteristics & pefile.DLL_CHARACTERISTICS["IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE"])

def disable_aslr(file_path):
    """Desativa o ASLR do arquivo PE fornecido."""
    pe = pefile.PE(file_path)
    if not has_aslr_enabled(pe):
        print("ASLR já está desativado para este arquivo.\n\n\n")
        return

    backup_and_modify(file_path, pe, False)

def enable_aslr(file_path):
    """Ativa o ASLR do arquivo PE fornecido."""
    pe = pefile.PE(file_path)
    if has_aslr_enabled(pe):
        print("ASLR já está ativado para este arquivo.\n\n\n")
        return

    backup_and_modify(file_path, pe, True)

def backup_and_modify(file_path, pe, enable):
    """Faz backup e modifica o ASLR do arquivo PE fornecido."""
    backup_dir = "backup"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    backup_file_path = os.path.join(backup_dir, os.path.basename(file_path))
    with open(file_path, "rb") as original_file, open(backup_file_path, "wb") as backup_file:
        backup_file.write(original_file.read())

    if enable:
        pe.OPTIONAL_HEADER.DllCharacteristics |= pefile.DLL_CHARACTERISTICS["IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE"]
    else:
        pe.OPTIONAL_HEADER.DllCharacteristics &= ~pefile.DLL_CHARACTERISTICS["IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE"]

    modified_file_path = os.path.splitext(file_path)[0] + ("_aslr_on" if enable else "_aslr_off") + os.path.splitext(file_path)[1]
    pe.write(filename=modified_file_path)

    print(f"Backup salvo em: {backup_file_path}")
    print(f"\n\n\nArquivo modificado salvo em: {modified_file_path}")

def verify_aslr(file_path):
    """Verifica o status do ASLR do arquivo PE fornecido."""
    pe = pefile.PE(file_path)
    if has_aslr_enabled(pe):
        print("ASLR ATIVADO\n\n\n")
    else:
        print("ASLR DESATIVADO\n\n\n")

if __name__ == "__main__":
    print(banner)
    parser = argparse.ArgumentParser(description="Ferramenta para verificar, desativar e ativar ASLR em arquivos PE.", add_help=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="Caminho do arquivo PE para DESATIVAR o ASLR.", type=str)
    group.add_argument("-v", "--verify", help="Caminho do arquivo PE para VERIFICAR o status do ASLR.", type=str)
    group.add_argument("-ON", help="Caminho do arquivo PE para ATIVAR o ASLR.", type=str)
    group.add_argument("-h", "-help", "--help", action="help", default=argparse.SUPPRESS, help="Mostra essa mensagem de ajuda e sai.")

    try:
        args = parser.parse_args()
    except SystemExit:
        print("Erro: Nenhum argumento fornecido. Use '-h' para ver as opções disponíveis.\n\n\n")
        sys.exit(1)

    if args.file:
        disable_aslr(args.file)
    elif args.verify:
        verify_aslr(args.verify)
    elif args.ON:
        enable_aslr(args.ON)
