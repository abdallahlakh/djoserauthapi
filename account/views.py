from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

from django.contrib.auth import login

User = get_user_model()

def custom_activation_view(request, uid, token):
    try:
        # decode uid
        uid = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid)

        # check if the token is valid
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            context = {
                'uid': uid,
                'token': token,
                'message': 'User activated successfully',
            }
        else:
            context = {
                'uid': uid,
                'token': token,
                'message': 'Activation link is invalid!',
            }
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        context = {
            'uid': uid,
            'token': token,
            'message': 'User does not exist',
        }

    return render(request, 'active_template.html', context)


def password_rest_view(request, uid, token):
    try:
        # decode uid
        uid = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid)

        # check if the token is valid
        if default_token_generator.check_token(user, token):
            context = {
                'uid': uid,
                'token': token,
                'message': 'Password reset link is valid',
            }
        else:
            context = {
                'uid': uid,
                'token': token,
                'message': 'Password reset link is invalid!',
            }
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        context = {
            'uid': uid,
            'token': token,
            'message': 'User does not exist',
        }

    return render(request, 'password_reset_template.html', context)

def reset_password_confirm_view(request):
    uid = request.GET.get('uid')
    token = request.GET.get('token')
    context = {'uid': uid, 'token': token}
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        re_new_password = request.POST.get('re_new_password')

        if new_password == re_new_password:
            try:
                print(uid)
                user = User.objects.get(pk=context['uid'])
                print(user)
                if default_token_generator.check_token(user, token):
                    user.set_password(new_password)
                    print("this is now",user)
                    user.save()
                    return redirect('http://localhost:3000')  # or wherever you want to redirect after password reset
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                context['message'] = 'User does not exist'

    return render(request, 'reset_password_confirm.html', context)


