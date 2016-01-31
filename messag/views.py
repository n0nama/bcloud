from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.core.serializers import serialize
from django.core.urlresolvers import reverse
from django.conf import settings
import json

from messag.models import Message, DraftMessage
from messag.forms import ComposeForm
from messag.utils import format_quote, get_user_model, get_username_field

User = get_user_model()


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class Inbox(LoginRequiredMixin, View):
    def get(self, request):
        template = 'messages/inbox.html'
        return render_to_response(template, {'me': request.user, 'current': 'inbox'})

    def post(self, request):
        data = []
        messages_list = Message.objects.inbox_for(request.user).exclude(favorite=request.user)
        for m in messages_list:
            if len(data) > 15:
                break
            data.append({'subject': (lambda a: a[:70]+'..' if(len(a)>70) else a)(m.subject),
                         'avatar': m.sender.profile.avatar.url,
                         'sender': m.sender.profile.f_name+' '+m.sender.profile.l_name,
                         'date': m.sent_at.isoformat(), 'id': m.pk})
        return HttpResponse(json.dumps(data))


class Outbox(LoginRequiredMixin, View):
    def get(self, request):
        template = 'messages/outbox.html'
        return render_to_response(template, {'me': request.user, 'current': 'outbox'})

    def post(self, request):
        data = []
        messages_list = Message.objects.outbox_for(request.user).exclude(favorite=request.user)
        for m in messages_list:
            if len(data) > 15:

                break
            data.append({'subject': (lambda a: a[:70]+'..' if(len(a)>70) else a)(m.subject),
                         'avatar': m.recipient.profile.avatar.url,
                         'sender': m.recipient.profile.f_name+' '+m.sender.profile.l_name,
                         'date': m.sent_at.isoformat(), 'id': m.pk})
        return HttpResponse(json.dumps(data))


class Trash(LoginRequiredMixin, View):
    def get(self, request):
        template = 'messages/trash.html'
        return render_to_response(template, {'me': request.user, 'current': 'trash'})

    def post(self, request):
        data = []
        messages_list = Message.objects.trash_for(request.user)
        for m in messages_list:
            if len(data) > 15:
                break
            data.append({'subject': (lambda a: a[:70]+'..' if(len(a)>70) else a)(m.subject),
                         'avatar': m.sender.profile.avatar.url,
                         'sender': m.sender.profile.f_name+' '+m.sender.profile.l_name,
                         'date': m.sent_at.isoformat(), 'id': m.pk})
        return HttpResponse(json.dumps(data))


class Favorite(LoginRequiredMixin, View):
    def get(self, request):
        template = 'messages/favorite.html'
        return render_to_response(template, {'me': request.user, 'current': 'favorite'})

    def post(self, request):
        data = []
        messages_list = Message.objects.favorite_for(request.user)
        for m in messages_list:
            if len(data) > 15:
                break
            data.append({'subject': (lambda a: a[:70]+'..' if(len(a)>70) else a)(m.subject),
                         'avatar': m.sender.profile.avatar.url,
                         'sender': m.sender.profile.f_name+' '+m.sender.profile.l_name,
                         'date': m.sent_at.isoformat(), 'id': m.pk})
        return HttpResponse(json.dumps(data))


class Draft(LoginRequiredMixin, View):
    def get(self, request):
        template = 'messages/draft.html'
        return render_to_response(template, {'me': request.user, 'current': 'draft'})

    def post(self, request):
        data = []
        messages_list = DraftMessage.objects.draft_for(request.user)
        for m in messages_list:
            if len(data) > 15:
                break
            data.append({'subject': (lambda a: a[:70]+'..' if(len(a)>70) else a)(m.subject),
                         'avatar': m.sender.profile.avatar.url,
                         'sender': m.sender.profile.f_name+' '+m.sender.profile.l_name,
                         'date': m.edited_at.isoformat(), 'id': m.pk})
        return HttpResponse(json.dumps(data))


@login_required
def compose(request, recipient=None, form_class=ComposeForm,
            template_name='messages/compose.html', success_url=None, recipient_filter=None):
    """
    Displays and handles the ``form_class`` form to compose new messages.
    Required Arguments: None
    Optional Arguments:
        ``recipient``: username of a `django.contrib.auth` User, who should
                       receive the message, optionally multiple usernames
                       could be separated by a '+'
        ``form_class``: the form-class to use
        ``template_name``: the template to use
        ``success_url``: where to redirect after successfull submission
    """
    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST, request.FILES, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=sender)
            if 'draft_id' in request.POST:
                draft = DraftMessage.objects.get(id=request.POST['draft_id'])
                if draft.sender == sender:
                    draft.delete()
            messages.info(request, _(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            if 'next' in request.GET:
                success_url = request.GET['next']
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
        if recipient is not None:
            recipients = [u for u in User.objects.filter(
                **{'%s__in' % get_username_field(): [r.strip() for r in recipient.split('+')]})]
            form.fields['recipient'].initial = recipients
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))


@login_required
def compose_draft(request):
    if request.method == "POST":
        if 'id' in request.POST and request.POST['id'] != '':
            draft = DraftMessage.objects.get(id=request.POST['id'])
            if draft.sender != request.user:
                return HttpResponse('Error')
            draft.subject = request.POST['subject']
            draft.body = request.POST['body']
            draft.recipient = request.POST['recipient']
            draft.save()
            return HttpResponse('Draft updated')
        else:
            draft = DraftMessage(
                sender=request.user,
                subject=request.POST['subject'],
                body=request.POST['body'],
                recipient=request.POST['recipient']
            )
            draft.save()
            return HttpResponse(draft.id)

@login_required
def delete_draft(request, draft_id, success_url=None):
    user = request.user
    draft = get_object_or_404(DraftMessage, id=draft_id)
    if success_url is None:
        success_url = reverse('messages_draft')
    if 'next' in request.GET:
        success_url = request.GET['next']
    if draft.sender == user:
        draft.delete()
        return HttpResponseRedirect(success_url)
    else:
        raise Http404

@login_required
def draft_send(request, draft_id, recipient=None, form_class=ComposeForm,
            template_name = 'messages/compose.html', success_url=None, recipient_filter=None):
    draft = DraftMessage.objects.get(id=draft_id)
    if draft.sender != request.user:
        raise 404
    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=sender)
            draft.delete()
            messages.info(request, _(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            if 'next' in request.GET:
                success_url = request.GET['next']
            return HttpResponseRedirect(success_url)
    else:
        form = form_class(initial = {
            'draft_id': draft_id,
            'recipient': draft.recipient,
            'body': draft.body,
            'subject': draft.subject,
        })
    return render_to_response(template_name, {
        'form': form,
        'id': draft.id
    }, context_instance=RequestContext(request))



@login_required
def reply(request, message_id, form_class=ComposeForm,
          template_name='messages/compose.html', success_url=None,
          recipient_filter=None, quote_helper=format_quote,
          subject_template=_(u"Re: %(subject)s"), ):
    """
    Prepares the ``form_class`` form for writing a reply to a given message
    (specified via ``message_id``). Uses the ``format_quote`` helper from
    ``messages.utils`` to pre-format the quote. To change the quote format
    assign a different ``quote_helper`` kwarg in your url-conf.

    """
    parent = get_object_or_404(Message, id=message_id)

    if parent.sender != request.user and parent.recipient != request.user:
        raise Http404

    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=request.user, parent_msg=parent)
            messages.info(request, _(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            return HttpResponseRedirect(success_url)
    else:
        form = form_class(initial={
            'body': quote_helper(parent.sender, parent.body),
            'subject': subject_template % {'subject': parent.subject},
            'recipient': [parent.sender, ]
        })
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))


@login_required
def delete(request, message_id, success_url=None):
    """
    Marks a message as deleted by sender or recipient. The message is not
    really removed from the database, because two users must delete a message
    before it's save to remove it completely.
    A cron-job should prune the database and remove old messages which are
    deleted by both users.
    As a side effect, this makes it easy to implement a trash with undelete.

    You can pass ?next=/foo/bar/ via the url to redirect the user to a different
    page (e.g. `/foo/bar/`) than ``success_url`` after deletion of the message.
    """
    user = request.user
    now = timezone.now()
    message = get_object_or_404(Message, id=message_id)
    deleted = False
    if success_url is None:
        success_url = reverse('messages_inbox')
    if 'next' in request.GET:
        success_url = request.GET['next']
    if message.sender == user:
        message.sender_deleted_at = now
        deleted = True
    if message.recipient == user:
        message.recipient_deleted_at = now
        deleted = True
    if user in message.favorite.all():
        message.favorite.remove(user)
    if deleted:
        message.save()
        messages.info(request, _(u"Message successfully deleted."))
        return HttpResponse('OK')
    raise Http404


@login_required
def add_favorite(request, message_id, success_url=None):
    user = request.user
    message = get_object_or_404(Message, id=message_id)
    if success_url is None:
        success_url = reverse('messages_inbox')
    if 'next' in request.GET:
        success_url = request.GET['next']
    if user not in message.favorite.all() and (message.sender == user or message.recipient == user):
        message.favorite.add(user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        raise Http404


@login_required
def delete_favorite(request, message_id, success_url=None):
    user = request.user
    message = get_object_or_404(Message, id=message_id)
    if success_url is None:
        success_url = reverse('messages_favorite')
    if 'next' in request.GET:
        success_url = request.GET['next']
    if user in message.favorite.all():
        message.favorite.remove(user)
        return HttpResponseRedirect(success_url)
    else:
        raise Http404


@login_required
def undelete(request, message_id, success_url=None):
    """
    Recovers a message from trash. This is achieved by removing the
    ``(sender|recipient)_deleted_at`` from the model.
    """
    user = request.user
    message = get_object_or_404(Message, id=message_id)
    undeleted = False
    if success_url is None:
        success_url = reverse('messages_inbox')
    if 'next' in request.GET:
        success_url = request.GET['next']
    if message.sender == user:
        message.sender_deleted_at = None
        undeleted = True
    if message.recipient == user:
        message.recipient_deleted_at = None
        undeleted = True
    if undeleted:
        message.save()
        messages.info(request, _(u"Message successfully recovered."))
        return HttpResponseRedirect(success_url)
    raise Http404


@login_required
def view(request, message_id, form_class=ComposeForm, quote_helper=format_quote,
         subject_template=_(u"Re: %(subject)s"),
         template_name='messages/view.html'):
    """
    Shows a single message.``message_id`` argument is required.
    The user is only allowed to see the message, if he is either
    the sender or the recipient. If the user is not allowed a 404
    is raised.
    If the user is the recipient and the message is unread
    ``read_at`` is set to the current datetime.
    If the user is the recipient a reply form will be added to the
    tenplate context, otherwise 'reply_form' will be None.
    """
    user = request.user
    now = timezone.now()
    message = get_object_or_404(Message, id=message_id)
    if (message.sender != user) and (message.recipient != user):
        raise Http404
    if message.read_at is None and message.recipient == user:
        message.read_at = now
        message.save()

    context = {'message': message, 'reply_form': None}
    if message.recipient == user:
        form = form_class(initial={
            'body': quote_helper(message.sender, message.body),
            'subject': subject_template % {'subject': message.subject},
            'recipient': [message.sender, ]
        })
        context['reply_form'] = form
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))
