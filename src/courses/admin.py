from django.contrib import admin

# Register your models here.
from .models import Course, Lesson
from django.utils.html import format_html
from cloudinary import CloudinaryImage
import helpers


class LessonInline(admin.StackedInline):    #admin.TabularInline
    model = Lesson
    readonly_fields = ['public_id','updated','display_image','display_video']
    extra = 0

    def display_image(self, obj, *args, **kwargs):
        url = helpers.get_cloudinary_image_object(
            obj, 
            field_name="thumbnail",
            width=200)
        return format_html(f"<img src={url} />")
    
    display_image.short_description = "Current Image"


    def display_video(self, obj, *args, **kwargs):
        video_embed_html = helpers.get_cloudinary_video_object(
            obj, 
            field_name="video",
            width=550,
            as_html=True)
        return video_embed_html
        
    display_video.short_description = "Current Video"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display=['title', 'status', 'access']
    list_filter=['status','access']
    fields = ['public_id','title','description','status','image','access','display_image']
    readonly_fields = ['display_image','public_id']


    def display_image(self, obj, *args, **kwargs):
        # url = obj.image_admin_url
        url = helpers.get_cloudinary_image_object(
            obj, 
            field_name="image",
            width=200)
        return format_html(f"<img src={url} />")
        
        # # Alternative:
        # # # print(obj.image.url)
        # url = obj.image.url
        # cloudinary_id = str(obj.image)
        # cloudinary_html = CloudinaryImage(cloudinary_id).image(width=200)
        # # return format_html(f"<img src='{url}' style='max-width: 200px; height: auto;' />")
        # return format_html(cloudinary_html)
    
    display_image.short_description = "Current Image"


# admin.site.register(Course, CourseAdmin)