from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# when new models are created the user will need to run python3 manage.py makemigrations
# followed by python3 manage.py migrate
class Place(models.Model):
    # if user is deleted remove all associated places
    user = models.ForeignKey('auth.user', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo'
        notes_str = self.notes[100:] if self.notes else 'no notes'
        return f'{self.pk}:  {self.name}, visited? {self.visited} on {self.date_visited}. Notes: {notes_str}.\nPhoto {photo_str}'
