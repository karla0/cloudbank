import boto3
import logging

from flask import g
from werkzeug.utils import secure_filename

from . import config

import uuid
logging.basicConfig(level=logging.INFO)

s3_client = boto3.client('s3')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in config.DEV_ALLOWED_EXTENSIONS

def get_uploaded_file(request):
    try:
        if "file" not in request.files:
            return "No file uploaded."

        file = request.files['file']
        if file.filename == '':
            return "No File Selected"
    
        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)
            uploaded_to_path = upload_to_s3(file)
            logging.info(f'File Uploaded to: {uploaded_to_path}')
            return uploaded_to_path
                
    except Exception as e:
        logging.info(f'Unable to upload file - Error: {e}')

def upload_to_s3(file):
    generated_key = uuid.uuid4()
    file_extension = file.filename.rsplit('.',1)[1].lower()
    upload_key = f'uploads/{g.user["id"]}/{generated_key}.{file_extension}'
    try:
        response = s3_client.put_object(
            Body=file,
            Bucket=config.DEV_BUCKET_NAME,
            Key=upload_key,
            ContentType=file.content_type,
            Metadata={
                'Status' : 'UNPROCESSED'
            }
            )
        return f's3://{config.DEV_BUCKET_NAME}/{upload_key}'
    except Exception as e:
        logging.info(f"Something Happened file was not uploaded: Error - {e}")
