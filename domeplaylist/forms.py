from django import forms
from django.forms import BaseInlineFormSet

# from madquiz.models import StudyModule, ModulePage, PAGE_TYPE_CHOICES, Answer, VIDEO_TYPE_CHOICES
from domeplaylist.models import PlayList, PlayItem


# class StudyModuleForm(forms.ModelForm):
#     class Meta:
#         model = StudyModule
#         # 'published_at' used here for setting to None after editing
#         fields = (
#             'name', 'description', 'category', 'isbn', 'image',
#             'published_at'
#         )
#
#     def __init__(self, *args, **kwargs):
#         # TODO : move default values to FORM
#         self.request = kwargs.pop('request', None)
#         self.host = kwargs.pop('host', None)
#         self.instance = kwargs.get('instance', None)
#
#         super(StudyModuleForm, self).__init__(*args, **kwargs)
#
#         self.fields['name'].label = 'Module Name (Required)'
#         self.fields['name'].widget.attrs.update({'required': True})
#
#         self.fields['description'].label = 'Module Description (Required)'
#         self.fields['description'].required = True
#         self.fields['description'].widget.attrs.update({'required': True})
#
#         self.fields['category'].label = 'Category (Optional)'
#         self.fields['category'].required = False
#
#         self.fields['isbn'].label = 'Related ISBN (Optional)'
#         self.fields['image'].label = 'Cover Image (Optional)'
#
#         for key in self.fields:
#             self.fields[key].widget.attrs.update({'class': 'form-control'})
#
#     def save(self, *args, **kwargs):
#         return super(StudyModuleForm, self).save(*args, **kwargs)
#

class PlayListForm(forms.ModelForm):
    class Meta:
        model = PlayList
        # 'published_at' used here for setting to None after editing
        fields = (
            'id', 'title', 'zodiac_choice',
            # 'published_at'
        )

    def __init__(self, *args, **kwargs):
        # TODO : move default values to FORM
        self.request = kwargs.pop('request', None)
        # self.host = kwargs.pop('host', None)
        self.instance = kwargs.get('instance', None)

        super(PlayListForm, self).__init__(*args, **kwargs)

        # self.fields['name'].label = 'Module Name (Required)'
        # self.fields['name'].widget.attrs.update({'required': True})

        # self.fields['description'].label = 'Module Description (Required)'
        # self.fields['description'].required = True
        # self.fields['description'].widget.attrs.update({'required': True})
        #
        # self.fields['category'].label = 'Category (Optional)'
        # self.fields['category'].required = False
        #
        # self.fields['isbn'].label = 'Related ISBN (Optional)'
        # self.fields['image'].label = 'Cover Image (Optional)'

        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def save(self, *args, **kwargs):
        return super(PlayListForm, self).save(*args, **kwargs)






# class MonetizeForm(forms.ModelForm):
#     class Meta:
#         model = StudyModule
#         # 'published_at' used here for setting to None after editing
#         fields = (
#             'name', 'description', 'category', 'isbn', 'image',
#             'price', 'published_at'
#         )
#
#     def __init__(self, *args, **kwargs):
#         # TODO : move default values to FORM
#         self.request = kwargs.pop('request', None)
#         self.instance = kwargs.get('instance', None)
#
#         super(MonetizeForm, self).__init__(*args, **kwargs)
#
#         self.fields['name'].label = 'Module Name'
#         # self.fields['name'].widget.attrs.update({'required': False})
#         self.fields['name'].widget.attrs['readonly'] = True
#
#         self.fields['description'].label = 'Module Description'
#         # self.fields['description'].widget.attrs.update({'required': False})
#         self.fields['description'].widget.attrs['readonly'] = True
#
#         self.fields['category'].label = 'Category'
#         self.fields['category'].required = False
#         self.fields['isbn'].label = 'Related ISBN'
#         self.fields['isbn'].widget.attrs['readonly'] = True
#         self.fields['image'].label = 'Cover Image'
#         self.fields['price'].label = 'Price'
#
#         for key in self.fields:
#             self.fields[key].widget.attrs.update({'class': 'form-control'})
#
#         # self.fields['price'].widget.attrs.update({'class': 'form-control text-right'})
#
#     def save(self, *args, **kwargs):
#         module = self.instance
#
#         if self.request is not None:
#             if 'btn_pub_to_store' in self.request.POST or 'btn_pub_changes' in self.request.POST:
#                 module.save_and_publish()
#             elif 'btn_remove_from_store' in self.request.POST:
#                 module.save_and_unpublish()
#
#         # if module.frozen_at is None:
#         #     return super(MonetizeForm, self).save(*args, **kwargs)
#
#
# class ChoosePageTypeForm(forms.Form):
#     page_type = forms.ChoiceField(widget=forms.RadioSelect, choices=PAGE_TYPE_CHOICES)
#
#     def __init__(self, *args, **kwargs):
#         super(ChoosePageTypeForm, self).__init__(*args, **kwargs)
#
#
# class PageEditForm(forms.ModelForm):
#     class Meta:
#         model = ModulePage
#         fields = ('title', 'text', 'image', 'randomize')
#
#     def __init__(self, *args, **kwargs):
#         super(PageEditForm, self).__init__(*args, **kwargs)
#         self.fields['randomize'].label = 'Randomize Order During Study'
#
#         if 'user_randomize' in kwargs['initial']:
#             self.fields['randomize'].initial = kwargs['initial']['user_randomize']
#
#         self.fields['title'].label = 'Title or Question (Required)'
#         self.fields['title'].widget.attrs.update({'required': True})
#         self.fields['text'].label = 'Additional Text (Optional)'
#         for key in self.fields:
#             if key != 'randomize':
#                 self.fields[key].widget.attrs.update({'class': 'form-control'})
#
#     def save(self, *args, **kwargs):
#         return super(PageEditForm, self).save(*args, **kwargs)
#
#
# class VideoPageEditForm(forms.ModelForm):
#     video_type = forms.ChoiceField(widget=forms.RadioSelect, choices=VIDEO_TYPE_CHOICES, initial=0)
#
#     class Meta:
#         model = ModulePage
#         fields = ('title', 'video_type', 'video', 'video_vimeo')
#
#     def __init__(self, *args, **kwargs):
#         super(VideoPageEditForm, self).__init__(*args, **kwargs)
#         self.fields['title'].label = 'Title (Required)'
#         self.fields['title'].widget.attrs.update({'required': True})
#         for key in self.fields:
#             if key not in ['video_type']:
#                 self.fields[key].widget.attrs.update({'class': 'form-control'})
#
#     def save(self, *args, **kwargs):
#         return super(VideoPageEditForm, self).save(*args, **kwargs)
#
#     def clean_video(self):
#         video_type = self.cleaned_data['video_type']
#         video = self.cleaned_data['video']
#         if video_type == '0' and len(video.strip()) == 0:
#             self.add_error('video', 'This field is required if you chose YouTube video page type!')
#         return video.strip()
#
#     def clean_video_vimeo(self):
#         video_type = self.cleaned_data['video_type']
#         video_vimeo = self.cleaned_data['video_vimeo']
#         if video_type == '1' and len(video_vimeo.strip()) == 0:
#             self.add_error('video_vimeo', 'This field is required if you chose VIMEO video page type!')
#         return video_vimeo.strip()
#

# class AnswerForm(forms.ModelForm):
#     class Meta:
#         model = Answer
#         fields = ('order', 'title', 'is_correct')
#
#     def __init__(self, *args, **kwargs):
#         super(AnswerForm, self).__init__(*args, **kwargs)
#         self.fields['is_correct'].label = 'Correct answer'
#         self.fields['title'].widget.attrs.update({'class': 'form-control', 'required': True})


class PlayItemForm(forms.ModelForm):
    class Meta:
        model = PlayItem
        fields = ('id', 'title', 'text')

    def __init__(self, *args, **kwargs):
        super(PlayItemForm, self).__init__(*args, **kwargs)
        # self.fields['is_correct'].label = 'Correct answer'
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'required': True})


# class TextAnswerForm(forms.ModelForm):
#     class Meta:
#         model = Answer
#         fields = ('title',)
#
#     def __init__(self, *args, **kwargs):
#         super(TextAnswerForm, self).__init__(*args, **kwargs)
#         self.fields['title'].widget.attrs.update({'class': 'form-control', 'required': True})


class PlayItemInlineFormSet(BaseInlineFormSet):
    def add_fields(self, form, i):
        super(PlayItemInlineFormSet, self).add_fields(form, i)
        form.index = i


#
# class StoreSearchForm(forms.Form):
#     category = forms.ChoiceField(
#         required=False,
#         choices=[(x, x) for x in ['', ] + StudyModule.CATEGORIES],
#     )
#     name = forms.CharField(max_length=100, required=False)
#
#     def __init__(self, *args, **kwargs):
#         super(StoreSearchForm, self).__init__(*args, **kwargs)
#
#         for key in self.fields:
#             self.fields[key].widget.attrs.update({'class': 'form-control'})
