import boto3
from decouple import config
from app.utils.colors import green, red

def test_s3_connection():
    try:
        print("\n=== Testing S3 Connection ===")
        print("Connecting to AWS S3...")
        
        s3 = boto3.client(
            's3',
            aws_access_key_id=config('AWS_ACCESS_KEY'),
            aws_secret_access_key=config('AWS_SECRET_KEY'),
            region_name=config('AWS_REGION')
        )
        
        print("Getting bucket list...")
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        target_bucket = config('AWS_BUCKET')
        
        print(f"\nAvailable buckets: {', '.join(buckets)}")
        print(f"Target bucket: {target_bucket}")
        
        assert target_bucket in buckets
        print(f"\n{green('✅ Test passed! Successfully connected to S3')}")
        print(f"{green(f'✅ Bucket \'{target_bucket}\' is accessible')}")
        
    except Exception as e:
        print(f"\n{red('❌ Test failed:')} {str(e)}")
        raise

if __name__ == "__main__":
    test_s3_connection()