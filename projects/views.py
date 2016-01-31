# coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

# from django.views.generic import View, TemplateView
# from django.utils.decorators import method_decorator

from .models import Project, Reply
from .forms import CreateProjectForm, FilterStatusForm, AddProjectAttachmentForm, PerformersReplyForm


def all_projects(request):
    projects = Project.objects.filter(status='N').filter(privacy_type='PU').order_by('-pub_date')
    """if request.method == 'POST':
        status_form = FilterStatusForm(request.POST)
        if status_form.is_valid():
            if status_form.cleaned_data['status_type'] == '*':
                projects = Project.objects.all().filter(privacy_type='PU')
            else:
                projects = Project.objects.filter(
                                                  status=status_form.cleaned_data['status_type']
                                                  ).filter(
                                                  privacy_type='PU')
    args['filter_status_form'] = FilterStatusForm()"""
    args = {}
    args.update(csrf(request))
    args['projects'] = projects
    
    return render_to_response('projects_list.html', args)

def my_projects(request):
    me = request.user
    projects = Project.objects.filter(author_id=me.id).order_by('-pub_date')
    args = {}
    args['projects'] = projects
    
    return render_to_response('my_projects.html', args)

@login_required
def get_project(request, project_id):
    me = request.user
    project = Project.objects.get(project_id=project_id)
    skills = project.skill_req.all()
    performers = project.performers.all()
    replies = Reply.objects.filter(project=project_id)
    args = {}
    args['project'] = project
    args['skills'] = skills
    args['performers'] = performers
    args['replies'] = replies
    if User.objects.get(username=me).id == project.author_id:
        args['is_mine'] = True
    return render_to_response('get_project.html', args)


@login_required
def create_project(request):
    me = request.user
    if request.method == 'POST':
        tmp_form = CreateProjectForm(request.POST)
        if tmp_form.is_valid():
            form = tmp_form.save(commit=False)
            form.author = me
            form.save()
            tmp_form.save_m2m()
            return HttpResponseRedirect(reverse('projects:getProject', args=[form.project_id]))
        else:
            errors = tmp_form.errors
            args = {}
            args['me'] = me
            args['errors'] = errors
            return render_to_response('create_project.html', args)
    else:
        form = CreateProjectForm()
        args = {}
        args.update(csrf(request))
        args['me'] = me
        args['project_create_form'] = form
        return render_to_response('create_project.html', args)


def add_attachement_to_project(request, project_id):
    project = Project.objects.get(project_id=project_id)
    if request.method == 'POST':
        tmp_form = AddProjectAttachmentForm(request.POST, request.FILES)
        if tmp_form.is_valid():
            form = tmp_form.save(commit=False)
            form.project = project
            form.save()
            return HttpResponseRedirect(reverse('projects:getProject', args=[project_id]))
        else:
            errors = tmp_form.errors
            args = {}
            args['errors'] = errors
            HttpResponse('Ошибка в заполнение полей')
    else:
        form = AddProjectAttachmentForm()
        args = {}
        args.update(csrf(request))
        args['add_project_attachment_form'] = form
        render_to_response('add_attachement_to_project.html', args)


@login_required
def edit_project(request, project_id):
    me = request.user
    me_id = User.objects.get(username=me).id
    try:
        project = Project.objects.filter(author=me_id).get(project_id=project_id)
    except ObjectDoesNotExist:
        raise Http404('Можно править только свои проекты')

    # skills = project.skill_req.all()
    # performance = project.performers.all()
    if request.method == 'POST':
        form = CreateProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('projects:index'))
        else:
            errors = form.errors
            args = {}
            args['me'] = me
            args['project'] = project
            args['errors'] = errors
            return render_to_response('edit_project.html', args)
    else:
        form = CreateProjectForm(instance=project)
        args = {}
        args.update(csrf(request))
        args['me'] = me
        args['project'] = project
        args['project_edit_form'] = form
        return render_to_response('edit_project.html', args)


@login_required
def make_reply(request, project_id):
    project = Project.objects.get(project_id=project_id)
    me = request.user
    try:
        # If user already replied on this project exception wouldn't raise and you get HttpResponse.
        Reply.objects.filter(project_id=project_id).get(author_id=me)
        return HttpResponse('Вы уже откликались на этот проект')
    except ObjectDoesNotExist:
        if request.method == 'POST':
            tmp_form = PerformersReplyForm(request.POST, request.FILES)
            if tmp_form.is_valid():
                form = tmp_form.save(commit=False)
                form.project = project
                form.author = me
                form.save()
                return HttpResponseRedirect(reverse('projects:getProject', args=[project_id]))
        else:
            args = {}
            args.update(csrf(request))
            args['performers_reply_form'] = PerformersReplyForm()
            args['project'] = project
            return render_to_response('make_reply.html', args)


def reply_details(request, project_id, reply_id):
    try:
        reply = Reply.objects.get(id=reply_id)
    except ObjectDoesNotExist:
        raise Http404('Отклика с таким id не существует')
    args = {}
    args['reply'] = reply
    return render_to_response('reply_details.html', args)


'''
class ProtectedViev(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedViev, self).dispatch(*args, **kwargs)


class ProjectView(ProtectedViev):

    def get(self, request, project_id):
        project = Project.objects.get(project_id=project_id)
        args = {}
        args['project'] = project
        return render_to_response('get_project.html', args)
'''
