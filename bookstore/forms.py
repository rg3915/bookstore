from django import forms

from .models import Author, Book, Publisher


class _BaseModelForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(_BaseModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class AuthorForm(_BaseModelForm):

    class Meta:
        model = Author
        fields = '__all__'


class PublisherForm(_BaseModelForm):

    class Meta:
        model = Publisher
        fields = '__all__'


class BookForm(_BaseModelForm):

    class Meta:
        model = Book
        fields = '__all__'
