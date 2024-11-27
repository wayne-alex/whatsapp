import random
import string

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string

from Login.forms import SignUpForm
from .models import Token, Account, Conversation, Message


def generate_verification_code(length=6):
    characters = string.digits
    verification_code = '0'  # Initialize with 0 to enter the loop
    while verification_code[0] == '0':
        verification_code = ''.join(random.choice(characters) for _ in range(length))
    return verification_code


# Create your views here.
def landing(request):
    return render(request, 'splash.html')


@login_required
def chats(request):
    # Retrieve conversations for the logged-in user
    # conversations = Conversation.objects.filter(participants=request.user.account)

    # Retrieve the latest message for each conversation
    # for conversation in conversations:
    #     conversation.latest_message = Message.objects.filter(conversation=conversation).order_by('-timestamp').first()
    #
    # context = {
    #     'conversations': conversations,
    #     'account_id': request.user.account.id,
    # }
    return render(request, 'chats.html', )


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully signed in")
            return redirect('chats')
        else:
            messages.error(request, "There was an error while signing in,Username or password incorrect!")
            return redirect('login')
    else:
        return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            # Send Email Address
            email = user.email
            verification_code = generate_verification_code()
            token = Token(user_id=user.id, code=verification_code, email=user.email)
            token.save()

            acc = Account(user=request.user)
            acc.save()

            # Create a dictionary with email data
            email_data = {
                'to': email,
                'name': 'Whatsapp',
                'subject': 'Account Activation',
                'html_message': render_to_string("activationEmail.html",
                                                 {'user_name': user.username, 'verification_code': verification_code}),

            }

            # Make a POST request to your Node.js server
            response = requests.post(settings.NODE_SERVER_URL, json=email_data)

            if response.status_code == 200:
                messages.success(request, "Activation link sent to your Email address.")
                return redirect('verify')
            else:
                messages.error(request, "Failed to send activation email.")
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def forgotpassword(request):
    if request.method == 'POST':
        username = request.user.username
        email = request.user.email
        data = request.POST['data']

        if data in [username, email]:

            obscured_email = email[0] + '*' * (len(email) - 1) + email[-1]
            messages.success(request, f'Email with reset instructions sent to your email address {obscured_email}')
            return redirect('login')
        else:
            messages.success(request, 'No Account found with the above credentials. Kindly recheck and try again')
            return redirect('forgot-password')
    else:
        return render(request, 'forgot_password.html')


@login_required()
def verify(request):
    if request.method == 'POST':
        code = request.POST.get('verification_code', '')
        expected_token = Token.objects.get(user_id=request.user.id, email=request.user.email)
        if expected_token:
            expected_code = str(expected_token.code)
            if code == expected_code:
                acc = Account.objects.get(user_id=request.user.id)
                acc.verified_email = 1
                acc.save()

                messages.success(request, 'You have successfully confirmed your Email. Welcome to MobilPark.')
                return redirect('profile')
            else:
                messages.error(request,
                               'The code you entered is incorrect. Please try again or change your email to a valid '
                               'address.')
                return redirect('verify')
        else:
            messages.success(request, 'No code was found,resend the Email then try Again')
            return redirect('change-email')
    else:
        return render(request, 'verification.html')


def changeEmail(request):
    return render(request, 'changeEmail.html')


@login_required
def profile(request):
    verified_email = Account.objects.get(user=request.user)
    if verified_email.verified_email:
        if request.method == 'POST':
            # Retrieve form data
            fullname = request.POST.get('fullname')
            about = request.POST.get('about')
            profile_picture = request.FILES.get('profile-picture')

            # Update user's profile
            account = Account.objects.get(user=request.user)
            account.full_name = fullname
            account.about = about
            if profile_picture:
                account.profile_picture = profile_picture
            account.save()

            default_account = Account.objects.get(user__username='WhatsApp')
            text = "🎉 Welcome to WhatsApp! 🎉We're thrilled to have you join us. If you have any questions or need " \
                   "assistance, feel free to reach out to our support team. Enjoy exploring our platform! 🚀"
            existing_conversation = Conversation.objects.filter(participants=account).filter(
                participants=default_account)
            if not existing_conversation.exists():
                conversation = Conversation.objects.create()
                conversation.participants.add(account, default_account)
                new_message = Message(conversation=conversation, sender=default_account, text=text)
                new_message.save()

            messages.success(request, 'Profile set successfully! Welcome.')
            return redirect('chats')
        else:
            return render(request, 'profile.html')
    else:
        messages.success(request, 'Kindly verify your email before continuing!')
        return redirect('verify')


@login_required
def chat(request, conversation_id):
    # conversation = get_object_or_404(Conversation, id=conversation_id)

    # for participant in conversation.participants.all():
    #     if participant != request.user.account:
    #         account = participant
    #         break

    # Get all messages associated with the conversation
    msgs = Message.objects.filter(conversation__id=conversation_id)

    return render(request, 'chat.html', {'account': [], 'messages': msgs,'conversation_id': conversation_id})
