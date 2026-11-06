# Lab AWS - Processamento Serverless Orientado a Eventos (Lambda + S3 + SNS)

Lab prático  Processamento de arquivos com AWS Lambda, S3 e SNS
Escola da Nuvem · AWS re/Start

## O que foi feito
- Arquitetura 100% Serverless orientada a eventos (*Event-Driven Architecture*)
- Função AWS Lambda em Python para contagem de palavras em arquivos de texto
- Gatilho automático configurado no Amazon S3 (`s3:ObjectCreated:*`) disparado ao fazer upload de arquivos `.txt`
- Publicação de notificações com o resultado do processamento via Amazon SNS diretamente para o e-mail cadastrado
- Execução sem necessidade de gerenciar servidores ou máquinas virtuais

## Arquitetura

```
Upload de arquivo .txt
          
          
   [ Amazon S3 ]
   (Bucket com trigger de evento)
          
          
   [ AWS Lambda ]
   (Função Python: processa o arquivo e conta palavras)
          
          
   [ Amazon SNS ]
   (Tópico com inscrição por e-mail)
          
          
  Notificação no E-mail
```

## Passo a passo no Console da AWS

### 1. Criar o Tópico SNS para Notificações
1. Acesse o **Amazon SNS** no console da AWS
2. Clique em **Tópicos**  **Criar tópico**
3. Tipo: **Padrão**
4. Nome: `topico-notificacao-lab`
5. Clique em **Criar tópico**
6. Dentro do tópico criado, clique em **Criar assinatura**:
   - Protocolo: **E-mail**
   - Ponto de extremidade: seu e-mail pessoal
7. Clique em **Criar assinatura**
8. Acesse sua caixa de entrada e clique no link de confirmação do e-mail recebido da AWS

### 2. Criar a Função AWS Lambda
1. Acesse o **AWS Lambda** no console
2. Clique em **Criar função**
3. Selecione **Criar do zero**
4. Nome da função: `funcao-contagem-palavras`
5. Tempo de execução (Runtime): **Python 3.12**
6. Clique em **Criar função**
7. Na aba de código, substitua pelo código do arquivo `src/lambda_function.py` deste repositório
8. Clique no botão **Deploy**

### 3. Configurar Variável de Ambiente e Permissões IAM
1. Na função Lambda, acesse a aba **Configuração**  **Variáveis de ambiente**  **Editar**
2. Adicione:
   - Chave: `SNS_TOPIC_ARN`
   - Valor: o ARN do tópico SNS criado no Passo 1
3. Clique em **Salvar**
4. Acesse a aba **Configuração**  **Permissões** e clique no nome da Role criada
5. No painel do IAM, clique em **Adicionar permissões**  **Anexar políticas**
6. Anexe:
   - `AmazonS3ReadOnlyAccess`
   - `AmazonSNSFullAccess`

### 4. Criar o Bucket S3 e Configurar o Gatilho
1. Acesse o **Amazon S3** e crie um bucket exclusivo (ex: `lab-lambda-upload-cesar`)
2. Volte à função Lambda e clique em **Adicionar gatilho**
3. Selecione a fonte: **S3**
4. Selecione o bucket criado
5. Tipo de evento: **Todos os eventos de criação de objeto** (`s3:ObjectCreated:*`)
6. Sufixo: `.txt` (processa somente arquivos de texto)
7. Marque o termo de confirmação e clique em **Adicionar**

### 5. Testar a Solução
1. Crie um arquivo de texto local:
   ```bash
   echo "AWS Lambda e computacao em nuvem com arquitetura orientada a eventos" > teste.txt
   ```
2. Acesse o bucket S3 e faça o upload de `teste.txt`
3. Em poucos segundos, um e-mail do SNS chegará informando o nome do arquivo, bucket e quantidade de palavras contadas!
4. Na aba **Monitorar** da função Lambda, clique em **Exibir logs do CloudWatch** para visualizar o log de execução
