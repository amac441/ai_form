from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.contrib import messages
import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required

from survey.models import Comment, Question, Survey, Category, FileUpload,Response,AnswerBase
from survey.forms import ResponseForm

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import base64
from django.core.files.base import ContentFile

# protect the view with require_POST decorator
from django.views.decorators.http import require_POST
from django import forms

def decode64(imgstr,num):
    #http://stackoverflow.com/questions/39576174/save-base64-image-in-django-file-field
    # format, imgstr = data.split(';base64,')
    ext = 'png'
    datanew = ContentFile(base64.b64decode(imgstr), name='drawing_%s.%s' % (num,ext)) # You can save this as file istance.
    return datanew

def send_email(subject,msg):
    # server = smtplib.SMTP('smtp.mail.yahoo.com:587')
    server = smtplib.SMTP('smtp.gmail.com:587')

    server.ehlo()
    server.starttls()

    To="team@appliedideas.io"
    # From="ajkrell@yahoo.com"
    From='appliedideas.message@gmail.com'
    # appliedideas.message@gmail.com

    msg = "\r\n".join([
      # "From: amc441@@aol.com",
      # "To: andy@appliedideas.io",
      "Subject: " + subject,
      "",
      msg
      ])


    # username = 'amac441@aol.com'
    # password = 'irishirish'

    # username = 'ajkrell@yahoo.com'
    # password = 'gogogo123!'

    username='appliedideas.message@gmail.com'
    password='slow1234'

    server.login(username,password)
    server.sendmail(From, To, msg)
    server.quit()

@require_POST
@csrf_exempt
def post_files(request):
    message="uploaded"
    if len(request.FILES) != 0:
        file=request.FILES['file[0]']

    elif len(request.POST) !=0:
        try:
            num=len(request.session['images'])
        except:
            num=1
        file=decode64(request.POST['image'],str(num))

    newdoc = FileUpload(docFile = file)
    newdoc.save();

    try:
        request.session['images'].append(newdoc.filename)
    except:
        request.session['images']=[newdoc.filename]

    return HttpResponse(message)


def add_files(request):
    # https://docs.djangoproject.com/en/1.10/topics/http/file-uploads/
    instance = ModelWithFileField(file_field=request.FILES['file'])
    instance.save()

def Index(request):
    return render(request, 'index.html')


def Maps(request):
    return render(request, 'maps.html')

def ResponseDetail(request, id):
    response = Response.objects.get(id=id)
    # a=response.AnswerBase()
    # for an in a:
    #     b=an.answertext
    if request.user==response.author:
        a=1
    answer = AnswerBase.objects.filter(response=response)
    c=answer[0].answertext.body
    for an in answer:
        b=an.answertext
    return render_to_response(request, 'response.html', {'response': response, 'answer': answer},context_instance=RequestContext(request))

def SurveyDetail(request, id):
    survey = Survey.objects.get(id=id)
    survey = Survey.objects.get(id=id)
    category_items = Category.objects.filter(survey=survey)
    categories = [c.name for c in category_items]
    print('categories for this survey:')
    print(categories)
    if request.method == 'POST':
        form = ResponseForm(request.POST, survey=survey)
        if form.is_valid():
            response = form.save()
            return HttpResponseRedirect("/confirm/%s" % response.interview_uuid)
    else:
        form = ResponseForm(survey=survey)
        print(form)
    # TODO sort by category
    return render(request, 'survey.html', {'response_form': form, 'survey': survey, 'categories': categories})


def Confirm(request, uuid):
    #email = settings.support_email
    return render(request, 'confirm.html', {'uuid': uuid})


def privacy(request):
    return render(request, 'privacy.html')


import json

@csrf_exempt
@login_required(login_url='/login/')
def dashboard(request, id=''):

    survey = Survey.objects.get(id=1)
    category_items = Category.objects.filter(survey=survey)
    categories = [c.name for c in category_items]
    # print('categories for this survey:')
    # print(categories)
    initialdata={}
    responsedata=None
    file_list_string=None

    if request.method == 'POST':
        #form = FileUploadForm(request.POST, request.FILES)
        #http://stackoverflow.com/questions/1110153/what-is-the-most-efficent-way-to-store-a-list-in-the-django-models

        if "draft" in request.POST:
            draft=True
            drafttext='draft'

        else:
            draft=False
            drafttext='success'

        try:
            filelist=request.session['images']
        except:
            filelist=[]

        # survey.filelist=json.dumps(filelist) #survey is model

        form = ResponseForm(request.POST, survey=survey)
        if form.is_valid():
            response = form.save(json.dumps(filelist), request.user, id, draft, commit=False)
            #return HttpResponseRedirect("/confirm/%s" % response.interview_uuid)
            send_email("New Idea - "+request.user.username.title(), "Title: "+ request.POST['title'])

            return HttpResponseRedirect('/dashboard/'+drafttext)
    #populate form with initial data
    elif id!='':

        if id == "draft":
            responsedata="Your Draft has been successfully saved! Access by viewing your Submissions"

        elif id == "success":
            responsedata="Your Idea has been successfully submitted!"

        else:
            try:
                response = Response.objects.get(id=int(id))
                rf=eval(response.filelist)
                if len(rf)>0:
                    file_list_string = "<b>Stored Files: </b>"+"|| ".join(rf)
                if request.user==response.author:

                    initialdata['title']=response.title
                    answer = AnswerBase.objects.filter(response=response)
                    c=answer[0].question.text
                    for an in answer:
                        i=an.question.id
                        key="question_"+str(i)
                        qtext=an.question.text
                        initialdata[key]=an.answertext.body
                        responsedata="<strong>Note:</strong> You are in edit mode for: <b>" + response.title + "</b>"
            except:
                pass
    # print(form)

    request.session['images']=[]
    form = ResponseForm(initialdata,survey=survey)
    form.fields['filelist'].widget = forms.HiddenInput()
    rlist=Response.objects.filter(author_id=request.user)
    # object_list = IgaiaContent.objects.filter(user=request.user)
    # return render_to_response('object_list_template.html', {'object_list': object_list})

    # TODO sort by category
    return render(request, 'dashboard.html', {'response_form': form, 'survey': survey, 'categories': categories,'data':rlist,'success':responsedata,'storedfiles':file_list_string})

import smtplib
# subject='test'


@csrf_exempt
def store_chat(request):

    """
    Saves the note content and position within the table.
    """
    # place = get_object_or_404(Space, url=space_name)
    # note_form = CommentForm(request.POST or None)

    if request.method == "POST" and request.is_ajax:
        comment = Comment()
        msg = request.POST['text']
        id = request.POST['id']
        id = id.strip("/").split('/')
        # if len(id)>1:
        #     # print (id[1])
        #     id = int(id[1])
        # else:
        #     id = int(request.POST['initial'])
        id = int(request.POST['initial'])
        user = request.user

        comment.response=Response.objects.get(id=id)
        comment.text=msg
        comment.author=user
        comment.save()

        send_email("New Chat From - "+user.username, msg)
        # msg = "Worked!"
        # print (request.POST)

    else:
        msg = "GET petitions are not allowed for this view."

    return HttpResponse(msg)