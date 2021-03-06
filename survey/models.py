from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
import os
from django.contrib.auth.models import User

class Blockwise(models.Model):
    email=models.TextField()
    created = models.DateTimeField(auto_now_add=True)

class Survey(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()

    def __unicode__(self):
        return (self.name)

    def questions(self):
        if self.pk:
            return Question.objects.filter(survey=self.pk)
        else:
            return None


class Category(models.Model):
    name = models.CharField(max_length=400)
    survey = models.ForeignKey(Survey)

    def __unicode__(self):
        return (self.name)


def validate_list(value):
    '''takes a text value and verifies that there is at least one comma '''
    values = value.split(',')
    if len(values) < 2:
        raise ValidationError(
            "The selected field requires an associated list of choices. Choices must contain more than one item.")


class Question(models.Model):
    TEXT = 'text'
    RADIO = 'radio'
    SELECT = 'select'
    SELECT_MULTIPLE = 'select-multiple'
    INTEGER = 'integer'

    QUESTION_TYPES = (
        (TEXT, 'text'),
        (RADIO, 'radio'),
        (SELECT, 'select'),
        (SELECT_MULTIPLE, 'Select Multiple'),
        (INTEGER, 'integer'),
    )

    text = models.TextField()
    required = models.BooleanField()
    category = models.ForeignKey(Category, blank=True, null=True, )
    survey = models.ForeignKey(Survey)
    question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)
    # the choices field is only used if the question type
    choices = models.TextField(blank=True, null=True,
                               help_text='if the question type is "radio," "select," or "select multiple" provide a comma-separated list of options for this question .')

    def save(self, *args, **kwargs):
        if (self.question_type == Question.RADIO or self.question_type == Question.SELECT
            or self.question_type == Question.SELECT_MULTIPLE):
            validate_list(self.choices)
        super(Question, self).save(*args, **kwargs)

    def get_choices(self):
        ''' parse the choices field and return a tuple formatted appropriately
        for the 'choices' argument of a form widget.'''
        choices = self.choices.split(',')
        choices_list = []
        for c in choices:
            c = c.strip()
            choices_list.append((c, c))
        choices_tuple = tuple(choices_list)
        return choices_tuple

    def __unicode__(self):
        return (self.text)


class Response(models.Model):
    # a response object is just a collection of questions and answers with a
    # unique interview uuid
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    survey = models.ForeignKey(Survey, null=True)
    title = models.CharField('Idea Name', max_length=400, blank=True, null=True)
    # interviewee = models.CharField('Name of Interviewee', max_length=400, blank=True, null=True)
    # conditions = models.TextField('Conditions during interview', blank=True, null=True)
    # comments = models.TextField('Any additional Comments', blank=True, null=True)
    interview_uuid = models.CharField("Interview unique identifier", max_length=36)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    filelist = models.TextField(blank=True, null=True)
    draft = models.BooleanField(blank=True, default=True)

    def __unicode__(self):
        return ("response %s" % self.interview_uuid)

    def __str__(self):
       return self.title + "-" + self.author.username

# class UploadFile(models.Model):
#     file = models.FileField(upload_to='files/%Y/%m')

class AnswerBase(models.Model):
    question = models.ForeignKey(Question)
    response = models.ForeignKey(Response)
    # files=models.ForeignKey(UploadFile)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


# these type-specific answer models use a text field to allow for flexible
# field sizes depending on the actual question this answer corresponds to. any
# "required" attribute will be enforced by the form.
class AnswerText(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerRadio(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerSelect(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerSelectMultiple(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerInteger(AnswerBase):
    body = models.IntegerField(blank=True, null=True)


class FileUpload(models.Model):
    docFile = models.FileField(upload_to='Data_Files', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)

    @property
    def filename(self):
        return os.path.basename(self.docFile.name)

    def __str__(self):
       return os.path.basename(self.docFile.name) + " - " + self.author.username

class Comment(models.Model):
    response = models.ForeignKey(Response, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    #writer = models.ForeignKey(User,blank=True, null=True)
    #approved_comment = models.BooleanField(default=False)

    # def approve(self):
        #     self.approved_comment = True
    #     self.save()

    def __str__(self):
        return self.text
