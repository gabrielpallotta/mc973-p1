# MC973 - Projeto 1

Para buildar o arquivo Dockerfile:
```
docker build -t 216392_212328_mc973_p1 .
```

Para executar o programa, com todos os casos de teste definidos na pasta `test`:
```
docker run -v .:/app 216392_212328_mc973_p1
```