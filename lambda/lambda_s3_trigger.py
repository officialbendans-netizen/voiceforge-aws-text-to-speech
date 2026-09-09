import boto3
import json
import uuid
from urllib.parse import unquote_plus

def lambda_handler(event, context):
    try:
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = unquote_plus(event['Records'][0]['s3']['object']['key'])
        
        print(f"Processing file: {object_key} from bucket: {bucket_name}")
        
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        text_content = response['Body'].read().decode('utf-8')
        
        print(f"Text to convert: {text_content}")
        
        polly_client = boto3.client('polly')
        polly_response = polly_client.synthesize_speech(
            Text=text_content,
            OutputFormat='mp3',
            VoiceId='Joanna',
            Engine='neural'
        )
        
        audio_filename = f"audio_{str(uuid.uuid4())}.mp3"
        output_bucket = 'tts-audio-output-benjamin'
        
        s3_client.put_object(
            Bucket=output_bucket,
            Key=audio_filename,
            Body=polly_response['AudioStream'].read(),
            ContentType='audio/mpeg'
        )
        
        print(f"Audio saved as: {audio_filename}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Text converted successfully',
                'audioFile': audio_filename
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
