import boto3
import os
import urllib.parse

s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    try:
        # Extrair informacoes do bucket e objeto a partir do evento S3
        record = event['Records'][0]
        bucket_name = record['s3']['bucket']['name']
        object_key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        
        print(f"Processando arquivo: {object_key} do bucket: {bucket_name}")
        
        # Download do conteudo do arquivo no S3
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        conteudo = response['Body'].read().decode('utf-8')
        
        # Contagem de palavras
        palavras = conteudo.split()
        total_palavras = len(palavras)
        
        # Mensagem formatada
        mensagem = (
            f"Relatorio de Processamento Serverless:\n\n"
            f"- Arquivo: {object_key}\n"
            f"- Bucket: {bucket_name}\n"
            f"- Total de palavras: {total_palavras}\n\n"
            f"Processado via AWS Lambda e notificado via Amazon SNS."
        )
        
        # Publicar notificacao no topico SNS
        topic_arn = os.environ.get('SNS_TOPIC_ARN')
        if topic_arn:
            sns_client.publish(
                TopicArn=topic_arn,
                Subject=f"Resultado: {object_key}",
                Message=mensagem
            )
            print("Notificacao SNS enviada com sucesso.")
            
        return {
            'statusCode': 200,
            'body': f"Arquivo {object_key} processado com sucesso. Palavras: {total_palavras}"
        }
        
    except Exception as e:
        print(f"Erro ao processar: {str(e)}")
        raise e
