from .models import UserProfile, Post
from modeltranslation.translator import TranslationOptions,register

@register(UserProfile)
class UserProfileTranslationOptions(TranslationOptions):
    fields = ('bio',)

@register(Post)
class PostProfileTranslationOptions(TranslationOptions):
    fields = ('description',)
