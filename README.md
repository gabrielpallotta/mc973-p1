# MC973 - Projeto 1

Para buildar o arquivo Dockerfile:
```
docker build -t 216392_212328_mc973_p1 .
```

Para executar o programa, com todos os casos de teste definidos na pasta `test`:
```
docker run -v .:/app 216392_212328_mc973_p1
```

O script "validate.sh" pode ser utilizado para comparar as saídas do programa com os sinais esperados em cada caso de teste, e irá reportar caso algum resultado esteja diferente:
```
./validate.sh
```