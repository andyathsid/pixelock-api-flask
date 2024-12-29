import boto3
from decouple import config
from io import BytesIO
from PIL import Image
import numpy as np

s3_client = boto3.client(
    's3',
    aws_access_key_id=config('AWS_ACCESS_KEY'),
    aws_secret_access_key=config('AWS_SECRET_KEY'),
    region_name=config('AWS_REGION')
)

def upload_image(image_array: np.ndarray, filename: str) -> str:
    """Upload image to S3 and return its URL"""
    bucket = config('AWS_BUCKET')
    
    # Convert numpy array to PIL Image
    image = Image.fromarray(image_array)
    
    # Save image to bytes buffer
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Upload to S3
    s3_client.upload_fileobj(
        buffer,
        bucket,
        f'uploads/{filename}',
        ExtraArgs={'ContentType': 'image/png'}
    )
    
    return f"https://{bucket}.s3.{config('AWS_REGION')}.amazonaws.com/uploads/{filename}"

def get_image(filename: str) -> BytesIO:
    """Get image from S3"""
    bucket = config('AWS_BUCKET')
    buffer = BytesIO()
    
    s3_client.download_fileobj(
        bucket,
        f'uploads/{filename}',
        buffer
    )
    buffer.seek(0)
    return buffer