from django.db import models
from cloudinary.models import CloudinaryField

#self-made libary
import helpers
import courses  
'''
Courses:
    - Title
    - Description
    - Thumbnail/Image
    - Access:
        - Anyone
        - Email required
        - Purchase required
        - User required (n/a)
    - Status:
        - Published
        - Coming Soon
        - Draft
    - Lessons
        - Title
        - Description
        - Video
        - Status: Published, Coming Soon, Draft
'''

# Create your models here.

# to initialize cloudinary configuration
helpers.cloudinary_init()

class PublishStatus(models.TextChoices):
    PUBLISHED = 'pub', 'Published'
    COMING_SOON = 'soon', 'Coming Soon'
    DRAFT = 'draft', 'Draft'

class AccessRequirement(models.TextChoices):
    ANYONE = 'any', 'Anyone'
    EMAIL_REQUIRED = 'email', 'Email Required'
    # PURCHASE_REQUIRED =  '', 'Purchase Required'
    # USER_REQUIRED = '', 'User Required'


def handle_upload(instance, filename):
    return f"{filename}"





class Course(models.Model):
    # pass
    title = models.CharField(max_length = 120)
    description = models.TextField(blank=True, null=True)
    # #django image upload
    # image = models.ImageField(upload_to=handle_upload, blank=True, null=True)
    #cloudinary image upload
    public_id = models.CharField(max_length = 130, blank=True, null=True, db_index=True)
    # uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    # uuid = models.UUIDField(default=uuid.uuid1, unique=True)  #uuid1 is based off timestampe so most likey is unique already
    image = CloudinaryField(
        "image", 
        null=True, 
        public_id_prefix=courses.get_public_id_prefix,
        display_name=courses.get_display_name,
        tags=["course", "thumbnail"]
    )
    access = models.CharField(max_length=5, choices=AccessRequirement.choices, default=AccessRequirement.EMAIL_REQUIRED)
    status = models.CharField(max_length=10, choices=PublishStatus.choices, default=PublishStatus.DRAFT)

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 

    #django save model
    def save(self, *args, **kwargs):    #save public_id in Course
        # before save
        if self.public_id == "" or self.public_id is None:
            self.public_id = courses.generate_public_id(self)
        super().save()
        # after save

    def get_absolute_url(self):
        return self.path
    
    @property
    def path(self):
        return f"/courses/{self.public_id}"
    
    def get_display_name(self):
        return f"{self.title} - Course"

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED
    
    def get_thumbnail(self):
        if not self.image:
            return None
        return helpers.get_cloudinary_image_object(
            self,
            field_name='image',
            as_html=False,
            width=382
        )
    
    def get_display_image(self):
        if not self.image:
            return None
        return helpers.get_cloudinary_image_object(
            self,
            field_name='image',
            as_html=False,
            width=750
        )
    
    # @property
    # #attribute
    # #return an URL (string)
    # def image_admin_url(self):
    #     return helpers.get_cloudinary_image_object(
    #         self,
    #         field_name="image",
    #         as_html=False,
    #         width=200
    #     )
        
    #     # #before using helpers
    #     # if not self.image:
    #     #     return None
    #     # image_options = {
    #     #     "width": 200
    #     # }
    #     # url = self.image.build_url(**image_options)
    #     # return url
    
    # #instance
    # #return URL or HTML (<img> tag)
    # def get_image_thumbnail(self, as_html=False, width=500): 
    #     return helpers.get_cloudinary_image_object(
    #         self,
    #         field_name="image",
    #         as_html=False,
    #         width=width
    #     )
        
    #     # #before using helpers        
    #     # if not self.image:
    #     #     return None
    #     # image_options = {
    #     #     "width": width
    #     # }
    #     # if as_html:
    #     #     # CloudinaryImage(str(self.image)).image(**image_options)
    #     #     return self.image.image(**image_options)
    #     # # CloudinaryImage(str(self.image)).build_url(**image_options)
    #     # url = self.image.build_url(**image_options)
    #     # return url
    

    # def get_image_detail(self, as_html=False, width=750):
    #     return helpers.get_cloudinary_image_object(
    #         self,
    #         field_name="image",
    #         as_html=False,
    #         width=width
    #     )
        
    #     # #before using helpers  
    #     # if not self.image:
    #     #     return None
    #     # image_options = {
    #     #     "width": width
    #     # }
    #     # if as_html:
    #     #     # CloudinaryImage(str(self.image)).image(**image_options)
    #     #     return self.image.image(**image_options)
    #     # # CloudinaryImage(str(self.image)).build_url(**image_options)
    #     # url = self.image.build_url(**image_options)
    #     # return url
    

"""
- Lessons
    - Title
    - Description
    - Video
    - Status: Published, Coming Soon, Draft
"""

# Lesson.objects.all() # lesson queryset -> all rows
# Lesson.objects.first()
# course_obj = Course.objects.first()
# course_qs = Course.objects.filter(id=course_obj.id)
# Lesson.objects.filter(course__id=course_obj.id)
# course_obj.lesson_set.all()
# lesson_obj = Lesson.objects.first()
# ne_course_obj = lesson_obj.course
# ne_course_lessons = ne_course_obj.lesson_set.all()
# lesson_obj.course_id
# course_obj.lesson_set.all().order_by("-title")

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # course_id 
    title = models.CharField(max_length=120)
    public_id = models.CharField(max_length = 130, blank=True, null=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField("image",
                public_id_prefix=courses.get_public_id_prefix,
                display_name=courses.get_display_name,
                tags=['thumbnail','lesson'],
                blank=True, 
                null=True
                )
    video = CloudinaryField("video", 
            public_id_prefix=courses.get_public_id_prefix,
            display_name=courses.get_display_name, 
            blank=True, 
            null=True, 
            type='private',
            tags=['video','lesson'],
            resource_type='video'
            )
    order = models.IntegerField(default=0)
    can_preview = models.BooleanField(default=False, help_text="If user does not have access to course, can they see this?")
    status = models.CharField(
        max_length=10, 
        choices=PublishStatus.choices,
        default=PublishStatus.PUBLISHED
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-updated']    #'-updated: most recent to oldest'


    def save(self, *args, **kwargs):    #save public_id in Lesson
        # before save
        if self.public_id == "" or self.public_id is None:
            self.public_id = courses.generate_public_id(self)
        super().save()
        # after save

    def get_absolute_url(self):
        return self.path

    @property
    def path(self):
        course_path = self.course.path
        if course_path.endswith("/"):
            course_path = course_path[:-1]
        return f"{course_path}/lessons/{self.public_id}"
    
    def get_display_name(self):
        return f"{self.title} - {self.course.get_display_name()}"
    
    @property
    def is_coming_soon(self):
        return self.status == PublishStatus.COMING_SOON
    
    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED
    
    @property
    def has_video(self):
        return self.video is not None
    
    @property
    def requires_email(self):
        return self.course.access == AccessRequirement.EMAIL_REQUIRED

    def get_thumbnail(self):
        width=382
        if self.thumbnail:
            return helpers.get_cloudinary_image_object(
                self,
                field_name='thumbnail',
                format='jpg',
                as_html=False,
                width=width
            )
        elif self.video:
            return helpers.get_cloudinary_image_object(
                self,
                field_name='video',
                format='jpg',
                as_html=False,
                width=width
            )
        else:
            return None