from django.db import models
import googlemaps
from test_task.settings import GOOGLE_API_KEY
from django.contrib.auth.models import AbstractUser, User as UserAuth
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos import Point


class User(models.Model):

    # Attributes
    address = models.CharField(max_length=100, verbose_name="Address")
    lat = models.FloatField(max_length=10, null=True, blank=True, verbose_name="Latitude")
    lng = models.FloatField(max_length=10, null=True, blank=True, verbose_name="Longitude")
    location = geomodels.PointField(null=True)

    # Relationships
    user = models.OneToOneField(UserAuth, on_delete=models.CASCADE)

    # Methods
    def __str__(self):
        return self.user.username

    # Calculate lat and lng attributes based on address through Google Maps Geocoding API
    def calc_lat_lng(self):
        # Getting geocode from Google Maps API
        gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
        geocode_result = gmaps.geocode(self.address)

        # Saving lat and lng into user instance
        self.lat = geocode_result[0]["geometry"]["location"]["lat"]
        self.lng = geocode_result[0]["geometry"]["location"]["lng"]
        self.location = Point(self.lng, self.lat)

    # Save user instance into database
    def save(self, silent=False, *args, **kwargs):
        if self.lat is None and self.lng is None:
            self.calc_lat_lng()

        return super(User, self).save(*args, **kwargs)


class Category(models.Model):

    # Attributes
    name = models.CharField(max_length=50, verbose_name="Name")
    slug = models.CharField(max_length=50, null=True, blank=True, verbose_name="Slug")

    # Methods
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

    # Save user instance into database
    def save(self, silent=False, *args, **kwargs):
        if self.slug is None or self.slug is "":
            self.slug = self.name.lower().replace(" ", "-")

        return super(Category, self).save(*args, **kwargs)


class Tag(models.Model):

    # Attributes
    name = models.CharField(max_length=50, verbose_name="Name")
    slug = models.CharField(max_length=50, null=True, blank=True, verbose_name="Slug")

    # Methods
    def __str__(self):
        return self.name

    # Save user instance into database
    def save(self, silent=False, *args, **kwargs):
        if self.slug is None or self.slug is "":
            self.slug = self.name.lower().replace(" ", "-")

        return super(Tag, self).save(*args, **kwargs)


class Blog(models.Model):
    # Attributes
    title = models.CharField(max_length=50, verbose_name="Title")
    content = models.CharField(max_length=10000, verbose_name="Content")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Date of creation")
    slug = models.CharField(max_length=50, null=True, blank=True, verbose_name="Slug")

    # Relationships
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Category")
    author = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Author")

    # Methods
    def __str__(self):
        return self.title

    # Save blog instance into database
    def save(self, silent=False, *args, **kwargs):
        if self.slug is None or self.slug is "":
            self.slug = self.title.lower().replace(" ", "-")

        return super(Blog, self).save(*args, **kwargs)


class Comment(models.Model):
    # Attributes
    comment = models.CharField(max_length=1000, verbose_name="Comment")

    # Relationships
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, verbose_name="User")
    blog = models.ForeignKey(Blog, null=False, on_delete=models.CASCADE, verbose_name="Blog")

    # Methods
    def __str__(self):
        return self.comment
