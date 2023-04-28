from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    image = models.ImageField(upload_to='media/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [("can_create_post", "Can create post")]

    def __str__(self):
        return self.title

    def delete_post(self):
        self.delete()


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    image = models.ImageField(upload_to='media/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [("can_create_event", "Can create event")]

    def __str__(self):
        return self.title

    def delete_event(self):
        self.delete()


class EventVisitor(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} ({self.email}) registered for {self.event}"


@receiver(post_save, sender=EventVisitor)
def add_user_to_event(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        if user:
            instance.name = user.first_name
            instance.email = user.email
            instance.save()


class PostForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 40, 'cols': 40}), label=_("Description"))

    class Meta:
        model = Post
        fields = '__all__'


class EventForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 40, 'cols': 40}), label=_("Description"))

    class Meta:
        model = Post
        fields = '__all__'
