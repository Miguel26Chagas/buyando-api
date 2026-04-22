import os
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

import asyncio

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

PHOTO_PROFILES = {
    "thumbnail": {"width": 100, "height": 100, "crop": "thumb"},
    "order_list": {"width": 300, "height": 300, "crop": "fill"},
    "full_hd": {"width": 1920, "height": 1080, "crop": "fit"},
    "standard": {"width": 600, "height": 600, "crop": "fill"}
}

def transform_cloudinary_url(public_id: str | None, profile:str = 'standard') -> str:   
    config = PHOTO_PROFILES.get(profile, PHOTO_PROFILES['standard'])
    url, _ = cloudinary_url(
        public_id,
        **config,
        gravity="auto",
        fetch_format="auto",
        quality="auto"
    )

    return url

async def add_any_photos_in_cloudinary(files_urls):
    loop = asyncio.get_running_loop()
    try:
        async def upload_wrapper(file):
            content = await file.read()
            return await loop.run_in_executor(None, lambda: cloudinary_uploader.upload(content))
        responses = await asyncio.gather(*(upload_wrapper(f) for f in files_urls))
    except Exception as e:
        print(f'Erro ao adicionar imagens no cloudnary: {e}')
        raise e
    return responses

