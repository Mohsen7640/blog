from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label='Name')
    from_email = forms.EmailField(
        label='From', initial='me.mohsen@gmail.com', required=False, disabled=True
    )
    to_email = forms.EmailField(label='To')
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.Form):
    name = forms.CharField(max_length=48, label='Name')
    email = forms.EmailField(label='Email')
    body = forms.CharField(widget=forms.Textarea, label='Body')


class SearchForm(forms.Form):
    query = forms.CharField(max_length=120, label='Search')
