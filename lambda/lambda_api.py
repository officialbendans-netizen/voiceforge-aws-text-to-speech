import boto3
import json
import uuid

def lambda_handler(event, context):

    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': ''
        }

    try:
        if 'body' in event:
            body = event['body']
            if isinstance(body, str):
                body = json.loads(body)
            elif body is None:
                body = {}
        else:
            body = event

        text = body.get('text', '')
        voice = body.get('voice', 'Joanna')

        print(f"Received text: {text[:50]}")
        print(f"Using voice: {voice}")

        if not text:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'No text provided'})
            }

        if len(text) > 3000:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Text too long. Maximum 3000 characters.'})
            }

        polly_client = boto3.client('polly')
        polly_response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice,
            Engine='neural'
        )

        audio_filename = f"audio_{str(uuid.uuid4())}.mp3"
        output_bucket = 'tts-audio-output-benjamin'

        s3_client = boto3.client('s3')
        s3_client.put_object(
            Bucket=output_bucket,
            Key=audio_filename,
            Body=polly_response['AudioStream'].read(),
            ContentType='audio/mpeg'
        )

        audio_url = f"https://{output_bucket}.s3.amazonaws.com/{audio_filename}"

        print(f"Audio saved: {audio_filename}")

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'message': 'Success',
                'audioUrl': audio_url,
                'audioFile': audio_filename
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
