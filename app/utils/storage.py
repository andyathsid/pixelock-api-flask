import uuid
from datetime import datetime

def generate_filename() -> str:
    """Generate a unique filename using timestamp and UUID"""
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}-{unique_id}.png"