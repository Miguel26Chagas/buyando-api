import os
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

from dotenv import load_dotenv
load_dotenv()

CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

cloudinary_uploader = cloudinary.uploader
cloudinary_url = cloudinary_url

cloudinary.config(
    cloud_name = 'dzccp72mu',
    api_key = CLOUDINARY_API_KEY,
    api_secret =CLOUDINARY_API_SECRET,
    secure=True,
)