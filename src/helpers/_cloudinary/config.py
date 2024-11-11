# helpers/_cloudinary/config.py

import cloudinary
from django.conf import settings

def cloudinary_init():
    # Access the settings within the function to avoid initialization issues
    CLOUDINARY_CLOUD_NAME = settings.CLOUDINARY_CLOUD_NAME
    CLOUDINARY_API_KEY = settings.CLOUDINARY_API_KEY
    CLOUDINARY_SECRET_KEY = settings.CLOUDINARY_SECRET_KEY
    
    '''
    Since you are accessing settings.CLOUDINARY_CLOUD_NAME in helpers/_cloudinary/config.py, 
    it may be better to ensure the settings are loaded when needed by moving the Cloudinary configuration inside the function. 
    This will prevent accessing the settings before they are properly set up.
    '''
    if not all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_SECRET_KEY]):
        raise ValueError("Cloudinary settings are not properly configured.")
    
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_SECRET_KEY,
        secure=True
    )


