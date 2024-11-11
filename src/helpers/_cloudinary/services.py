from django.template.loader import get_template
from django.conf import settings

def get_cloudinary_image_object(instance, 
                                field_name="image",
                                as_html=False,
                                format=None,
                                width=1200
                                ):
    if not hasattr(instance, field_name):
         return None
    image_object = getattr(instance, field_name)
    if not image_object:
        return None
    image_options = {
        "width": width
    }
    if format is not None:
        image_options['format'] = format
    if as_html:
        return image_object.image(**image_options)
    url = image_object.build_url(**image_options)
    # print("==========url==========",url)
    return url


# video_html = """
# <video controls autoplay>
# <source src="{video_url}">
# </video>
# """

def get_cloudinary_video_object(instance, 
                                field_name="video",
                                as_html=False,
                                width=None,
                                height=None,
                                sign_url=True, # for private videos
                                fetch_format="auto",
                                quality="auto",
                                contorls=True,
                                autoplay=True,
                                ):
    if not hasattr(instance, field_name):
         return None
    video_object = getattr(instance, field_name)
    if not video_object:
        return None
    video_options = {
        "sign_url": sign_url,
        "fetch_format": fetch_format,
        "quality": quality,
        "contorls": contorls,
        "autoplay": autoplay,
    }
    if width is not None:
         video_options['width']=width
    if height is not None:
         video_options['height']=height
    if width and height:
         video_options['crop']="limit"
    url = video_object.build_url(**video_options)
    if as_html:
        template_name = "videos/snippets/embed.html"
        tmpl = get_template(template_name)
        cloud_name = settings.CLOUDINARY_CLOUD_NAME
        _html = tmpl.render({'video_url': url, 'cloud_name': cloud_name, 'base_color': "#007cae"})
        #  return video_html.format(video_url=url).strip()
        return _html
    return url

