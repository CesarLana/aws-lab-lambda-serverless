import boto3
import os
import urllib.parse

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    sns = boto3.client('sns')
    
    # Pega o bucket e o arquivo do evento
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    # Baixa o arquivo
    response = s3.get_object(Bucket=bucket, Key=key)
    conteudo = response['Body'].read().decode('utf-8')
    
    # Conta as palavras
    total_palavras = len(conteudo.split())
    
    # Envia notificacao via SNS
    mensagem = f'Arquivo: {key}\nBucket: {bucket}\nTotal de palavras: {total_palavras}'
    sns.publish(
        TopicArn=os.environ['SNS_TOPIC_ARN'],
        Subject='Contagem de Palavras - Lambda',
        Message=mensagem
    )
    
    print(f'Arquivo {key} processado. Palavras: {total_palavras}')
    return {'palavras': total_palavras}
