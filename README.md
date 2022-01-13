# Back-end-pyhton-maxtrack
Teste referente ao processo seletivo para desenvoldera back-end na Maxtrack

# Tecnologias Utilizadas
* tornado
* Mongodb
* sklearn

# Instação do projeto

1 - Clone o repositorio
```bash
git clone https://github.com/anapaulaaraujo/teste-back-end-maxtrack.git
```
2- Acesse a pasta do projeto pelo terminal
```bash
cd teste-back-end-maxtrack
```
3 - Inicie a API
```bash
python main.py
```
# EndPoint da API

|  Action  |  HTML | EndPoint              | payload |
|---       |---    |---                    |---      |
|  Read    | GET   | /api/retorna_metricas |  - |
|  Create  | POST  | /api/calcula_metricas | {"serial":"","datahora_inicio":"" "datahora_fim":""} |



