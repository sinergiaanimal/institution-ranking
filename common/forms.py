from django.forms.models import ModelForm
from django.forms.widgets import Textarea


class EmbedPluginForm(ModelForm):
    
    class Meta:
        widgets = {
            'content': Textarea(
                attrs={
                    'class': 'js-ckeditor-use-selected-text',
                    'style': 'min-height: 360px;'
                }
            ),
        }
