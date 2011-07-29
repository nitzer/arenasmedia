# -*- coding:utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import create_update
from user_profile.models import UserProfile
from user_profile.forms import UserProfileForm
from django.template import RequestContext


def profile(request, username):
    extra_context = {}
    profile = get_object_or_404(UserProfile, user__username__iexact=username)
    extra_context.update({'profile': profile})
    if request.user == profile.user:
        form = UserProfileForm(instance=profile)
        extra_context.update({'form': form})
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('user_profile', profile)

    return render_to_response('user_profile/profile.html', context_instance=RequestContext(request, extra_context))
