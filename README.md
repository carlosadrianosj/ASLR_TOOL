# ASLR_TOOL
Script python para automatizar processo de verificação, desativação e ativação do ASLR em arquivos PE (Portable Executable).

## Sobre
O ASLR (Address Space Layout Randomization) é uma técnica de segurança que randomiza o endereço de memória onde os processos são executados. Isso torna mais difícil para um atacante prever a localização exata de uma função ou buffer específico. No entanto, para quem está aprendendo engenharia reversa, o ASLR pode ser um obstáculo. Esta ferramenta foi criada para ajudar a desativar o ASLR em arquivos PE, facilitando a análise.


## Requisitos
* Python 3
* Biblioteca pefile
  
Instale a biblioteca pefile usando pip:
```
pip install pefile
```

## Uso
```
python3 aslr_tool.py -h
```

## Opções:
* -f ou --file: Caminho do arquivo PE para DESATIVAR o ASLR.
* -v ou --verify: Caminho do arquivo PE para VERIFICAR o status do ASLR.
* -ON: Caminho do arquivo PE para ATIVAR o ASLR.

## Exemplos:
Para desativar o ASLR:
```
python3 aslr_tool.py -f caminho/do/arquivo.exe
```

Para verificar o status do ASLR:
```
python3 aslr_tool.py -v caminho/do/arquivo.exe
```

Para ativar o ASLR:
```
python3 aslr_tool.py -ON caminho/do/arquivo.exe
```

# Contribuições
Contribuições são bem-vindas! Por favor, faça um fork do repositório e crie um Pull Request com suas alterações.

# Licença
MIT

Desenvolvido com ❤️ por Carlos Adriano | Reverse Engineer.

