import re
import uuid

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from utils import gen_random_code
from .models import User, Member, Room, Message
from .forms import SignUpForm, LoginForm, SendMessageForm


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'home/index.html')

    return redirect("home:home_page")


@method_decorator(login_required, name='dispatch')
class HomePage(ListView):
    template_name = "home/home.html"
    context_object_name = "rooms"

    def get_queryset(self):
        return [member.room for member in Member.objects.filter(user=self.request.user, left=False).select_related('room')]


def room(is_ajax: bool):
    @login_required
    def view(request, invite_link):
        try:
            r = Room.objects.get(invite_link=invite_link)
        except (Room.DoesNotExist, KeyError):
            messages.error(request, "There is no room with the Invite Link you provided. You can create one here.")
            return redirect("home:create")

        user_rooms = [member.room for member in Member.objects.filter(user=request.user)]
        m = Member(
            user=request.user,
            room=r,
            join_date=timezone.now(),
            is_admin=False,
            left=False
        )
        if r not in user_rooms:
            m.save()
        elif r in user_rooms and (m := Member.objects.get(room=r, user=request.user)).left:
            m.left = False
            m.save()
        preview_rooms = [member.room for member in Member.objects.filter(user=request.user) if not member.left]

        context = {
            'room': r,
            'user': m,
            'recent_messages': r.message_set.all()[:200],
            'rooms': preview_rooms,
        }
        return render(request, 'home/chats-ajax.html' if is_ajax else 'home/chats.html', context=context)

    return view


@login_required
def leave(request):
    if not request.POST:
        return Http404()

    try:
        m = Member.objects.get(user=request.user, room__id=request.POST["room-id"])
        m.left = True
        m.save()
        messages.success(request, f"Left room {m.room.name}.")
        return redirect("home:index")
    except (KeyError, Member.DoesNotExist):
        return Http404("This room doesn't exist or you aren't joined.")


@login_required
def create(request):
    if name := request.POST.get('name', None):
        invite_link = str(uuid.uuid4())
        r = Room(
            name=name,
            invite_link=invite_link,
            date_created=timezone.now(),
            creator=request.user
        )
        m = Member(
            user=request.user,
            room=r,
            join_date=timezone.now(),
            is_admin=True
        )
        r.save()
        m.save()
        messages.success(request, f"Created room {r.name}.")
        return redirect('home:room', invite_link=invite_link)

    context = {
        'is_creating': True,
        'rooms': [member.room for member in Member.objects.filter(user=request.user)]
    }
    return render(request, 'home/create.html', context=context)


@login_required
def kick_user(request):
    if not request.POST or not Member.objects.filter(id=request.POST['member-id']):
        return Http404()

    m = Member.objects.get(id=request.POST['member-id'])
    user_membership = Member.objects.get(user=request.user, room=m.room)

    if m.room.creator != request.user and not user_membership.is_admin:
        return Http404()

    m.left = True
    m.save()
    messages.success(request, f"Kicked out user {m.user.username} from room {m.room.name}.")

    return redirect('home:room', invite_link=m.room.invite_link)


@login_required
def set_room_administration(request, status):
    if not request.POST or (m := Member.objects.get(id=request.POST['member-id'])).room.creator != request.user:
        return Http404()

    if status == "admin":
        m.is_admin = True
    elif status == "noadmin":
        m.is_admin = False
    else:
        return Http404("Invalid administration status")

    m.save()
    messages.success(request, f"User {m.user.username} is {'' if m.is_admin else 'not'} an admin now.")
    return redirect("home:room", invite_link=m.room.invite_link)


@login_required
def delete_room(request):
    if not request.POST or (r := Room.objects.get(id=request.POST['room-id'])).creator != request.user:
        return Http404()

    if r.creator != request.user:
        return Http404("You are not the creator of this room.")

    r.delete()
    messages.success(request, f"Deleted room {r.name}.")
    return redirect("home:index")


@login_required
def send(request):
    form = SendMessageForm(request.POST)
    if form.is_valid():
        r = Room.objects.get(invite_link=form.cleaned_data['room'])
        sender = Member.objects.get(user=request.user, room=r)
        text = form.cleaned_data["message"]

        if reply_id := form.cleaned_data.get("reply_id", ""):
            reply = Message.objects.get(id=reply_id)
        else:
            reply = None

        message = Message(sender=sender, text=text, room=r, date=timezone.now(), replied_message=reply)
        message.save()

        return redirect('home:room', invite_link=r.invite_link)


def sign_up(request):
    if 'code' not in request.POST:
        form = SignUpForm(request.POST)
        if not form.is_valid():
            if not re.findall('^[a-zA-Z][a-zA-Z0-9_]{4,30}$', form.cleaned_data['username']):
                messages.error(request, "Username must only have letters, numbers and underline. It must start with a letter and have at least 5 characters.")
                return redirect("home:index")

            else:
                messages.error(request, "Something went wrong. Try again.")
                return redirect("home:index")

        if User.objects.filter(username=form.cleaned_data['username'], passed_login_code=True) or User.objects.filter(email=form.cleaned_data['email'], passed_login_code=True):
            messages.error(request, "A user with this username or email already exists.")
            return redirect("home:index")

        try:
            code = gen_random_code()
            send_mail(
                'Your ChatRoom login code',
                f'<h1>Hello, welcome to ChatRoom.</h1> use this code to create your account. <code>{code}</code> If this is not requested by you, you can ignore this message.',
                'info@chatroom.ncpanel.pro',
                [form.cleaned_data['email']],
                fail_silently=False
            )

            signer, created = User.objects.get_or_create(email=form.cleaned_data['email'], username=form.cleaned_data['username'], defaults=dict(passed_login_code=False))
            signer.login_code = code
            signer.set_password(form.cleaned_data['password'])
            signer.save()

            messages.info(request, "An email with the login code has been sent to you.")
            return redirect('home:code', email=signer.email, username=signer.username)
        except Exception as e:
            messages.error(request, str(e))
            return redirect("home:index")

    else:
        form = SignUpForm(request.POST)
        if form.is_valid():
            signer = User.objects.get(username=form.cleaned_data['username'])
            if signer.passed_login_code:
                return redirect("home:index")
            if signer.login_code != form.cleaned_data['code']:
                messages.error(request, 'The code is wrong. Try again.')
                return redirect('home:code', email=signer.email, username=signer.username)
            else:
                signer.passed_login_code = True
                signer.save()
                messages.success(request, 'Created account! Now login with your username and password.')
                return redirect('home:home_page')


def code(request, email, username):
    return render(request, 'home/index.html', context={'email': email, 'username': username})


def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        print(user)
        if user and (user.passed_login_code or user.is_staff or user.is_superuser):
            login(request, user)
            return redirect('home:home_page')
        else:
            messages.error(request, "You entered a wrong username or password.")
            return redirect("home:index")


@login_required
def logout_view(request):
    logout(request)
    return redirect("home:index")
