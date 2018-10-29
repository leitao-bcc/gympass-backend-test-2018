# Gympass Backend Test 2018

Esse projeto faz parte do processo seletivo para a vaga de backend no Gympass


## O Problema

O problema consiste em ler os dados de uma corrida de kart e extrair os resultados da mesma.

Esses dados estão contidos em um arquivo de log onde cada linha representa uma volta de um piloto.

Ao final é preciso mostrar as seguintes informações sobre cada piloto:

* Posição Chegada
* Código Piloto
* Nome Piloto
* Qtde Voltas Completadas 
* Tempo Total de Prova

Mais detalhes podem ser vistos no [repositório](https://github.com/Gympass/interview-test).

## A Solução

A solução foi desenvolvida utilizando a linguagem [Python 3.6](https://docs.python.org/3.6/). 

Os testes foram escritos utilizando o framework [unittest](https://docs.python.org/3.6/library/unittest.html?highlight=unittest#module-unittest)


#### Implementação

Foram criadas 4 classes para representar as informações do problema e a solução. 

* **Driver:** representa o objeto piloto contendo suas informções básicas
* **Lap:** representa cada uma das voltas da corrida com as informações como, tempo de volta e número da volta
* **Result:** representa o resultado final de cada um dos pilotos
* **Racing:** representa a corrida com todas as suas informações e os métodos para calcular o resultado


#### Exemplo de uso

```python
racing = Racing()

racing.parser_logfile(PATH_TO_LOG_FILE)

print(racing)
```

### Instruções de Execução

Para executar o projeto basta baixar o repositório e rodar o seguinte comando:

```
python3.6 example.py
```

### Instruções de Teste

Para executar os testes automatizados do projeto, basta rodar o seguinte comando:

```
python3.6 -m unittest discover
```