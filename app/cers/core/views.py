from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render


@login_required
def set_subsidiary_context(request):
    path = request.POST['path']
    subsidiary_context = int(request.POST['subsidiary_context'])
    user = request.user
    user.settings['company'] = subsidiary_context
    user.save()
    return HttpResponseRedirect(path)
