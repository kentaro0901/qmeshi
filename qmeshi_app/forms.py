from django.forms import ModelForm
from qmeshi_app.models import Impression


class ImpressionForm(ModelForm):
    """感想のフォーム"""
    class Meta:
        model = Impression
        fields = ('comment', )