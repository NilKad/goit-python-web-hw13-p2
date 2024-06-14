from django.forms import (
    ModelForm,
    CharField,
    Textarea,
    ImageField,
    TextInput,
    FileInput,
    URLField,
)
from django.utils.safestring import SafeString

from app_author.models import Author
from .models import Quote


class QuoteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы Bootstrap к каждому виджету поля
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "col-sm-10 ",
                }
            )
        self.fields["author"].queryset = Author.objects.order_by("fullname")

    class Meta:
        model = Quote
        fields = (
            "quote",
            "tags",
            "author",
        )

    def as_p(self):
        """Add CSS Styling to divs"""

        return SafeString(
            super()
            .as_p()
            .replace("<label", "<label class='col-sm-2 col-form-label'")
            .replace("<p>", "<p class='row'>")
        )
