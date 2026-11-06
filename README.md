# aws-lab-lambda-serverless

Lab prÃ¡tico â€” Processamento de arquivos com AWS Lambda, S3 e SNS
Escola da Nuvem Â· AWS re/Start

## O que foi feito
- Arquitetura 100% Serverless orientada a eventos (*Event-Driven Architecture*)
- FunÃ§Ã£o AWS Lambda em Python para contagem de palavras em arquivos de texto
- Gatilho automÃ¡tico configurado no Amazon S3 (`s3:ObjectCreated:*`) disparado ao fazer upload de arquivos `.txt`
- PublicaÃ§Ã£o de notificaÃ§Ãµes com o resultado do processamento via Amazon SNS diretamente para o e-mail cadastrado
- ExecuÃ§Ã£o sem necessidade de gerenciar servidores ou mÃ¡quinas virtuais

## Arquitetura

```
Upload de arquivo .txt
          â”‚
          â–¼
   [ Amazon S3 ]
   (Bucket com trigger de evento)
          â”‚
          â–¼
   [ AWS Lambda ]
   (FunÃ§Ã£o Python: processa o arquivo e conta palavras)
          â”‚
          â–¼
   [ Amazon SNS ]
   (TÃ³pico com inscriÃ§Ã£o por e-mail)
          â”‚
          â–¼
  NotificaÃ§Ã£o no E-mail
```

## Passo a passo no Console da AWS

### 1. Criar o TÃ³pico SNS para NotificaÃ§Ãµes
1. Acesse o **Amazon SNS** no console da AWS
2. Clique em **TÃ³picos** â†’ **Criar tÃ³pico**
3. Tipo: **PadrÃ£o**
4. Nome: `topico-notificacao-lab`
5. Clique em **Criar tÃ³pico**
6. Dentro do tÃ³pico criado, clique em **Criar assinatura**:
   - Protocolo: **E-mail**
   - Ponto de extremidade: seu e-mail pessoal
7. Clique em **Criar assinatura**
8. Acesse sua caixa de entrada e clique no link de confirmaÃ§Ã£o do e-mail recebido da AWS

### 2. Criar a FunÃ§Ã£o AWS Lambda
1. Acesse o **AWS Lambda** no console
2. Clique em **Criar funÃ§Ã£o**
3. Selecione **Criar do zero**
4. Nome da funÃ§Ã£o: `funcao-contagem-palavras`
5. Tempo de execuÃ§Ã£o (Runtime): **Python 3.12**
6. Clique em **Criar funÃ§Ã£o**
7. Na aba de cÃ³digo, substitua pelo cÃ³digo do arquivo `src/lambda_function.py` deste repositÃ³rio
8. Clique no botÃ£o **Deploy**

### 3. Configurar VariÃ¡vel de Ambiente e PermissÃµes IAM
1. Na funÃ§Ã£o Lambda, acesse a aba **ConfiguraÃ§Ã£o** â†’ **VariÃ¡veis de ambiente** â†’ **Editar**
2. Adicione:
   - Chave: `SNS_TOPIC_ARN`
   - Valor: o ARN do tÃ³pico SNS criado no Passo 1
3. Clique em **Salvar**
4. Acesse a aba **ConfiguraÃ§Ã£o** â†’ **PermissÃµes** e clique no nome da Role criada
5. No painel do IAM, clique em **Adicionar permissÃµes** â†’ **Anexar polÃ­ticas**
6. Anexe:
   - `AmazonS3ReadOnlyAccess`
   - `AmazonSNSFullAccess`

### 4. Criar o Bucket S3 e Configurar o Gatilho
1. Acesse o **Amazon S3** e crie um bucket exclusivo (ex: `lab-lambda-upload-cesar`)
2. Volte Ã  funÃ§Ã£o Lambda e clique em **Adicionar gatilho**
3. Selecione a fonte: **S3**
4. Selecione o bucket criado
5. Tipo de evento: **Todos os eventos de criaÃ§Ã£o de objeto** (`s3:ObjectCreated:*`)
6. Sufixo: `.txt` (processa somente arquivos de texto)
7. Marque o termo de confirmaÃ§Ã£o e clique em **Adicionar**

### 5. Testar a SoluÃ§Ã£o
1. Crie um arquivo de texto local:
   ```bash
   echo "AWS Lambda e computacao em nuvem com arquitetura orientada a eventos" > teste.txt
   ```
2. Acesse o bucket S3 e faÃ§a o upload de `teste.txt`
3. Em poucos segundos, um e-mail do SNS chegarÃ¡ informando o nome do arquivo, bucket e quantidade de palavras contadas!
4. Na aba **Monitorar** da funÃ§Ã£o Lambda, clique em **Exibir logs do CloudWatch** para visualizar o log de execuÃ§Ã£o
