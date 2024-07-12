from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CreateNewPresetForm
from .models import Preset
from markers.models import Marker


def create_preset(request):
    context = {}
    if request.method == 'POST':
        form = CreateNewPresetForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            comment = form.cleaned_data['comment']
            time_of_the_event = form.cleaned_data['time_of_the_event']
            price = form.cleaned_data['price']
            creator = request.user
            markers = form.cleaned_data['markers']
            preset = Preset(title=title,
                            comment=comment,
                            time_of_the_event=time_of_the_event,
                            creator=creator, price=price,
                            )
            preset.save()
            for marker in markers:
                preset.markers.add(marker)
            print(markers)
            return HttpResponse(status=200)
    # markers = request.user.markers.all()
    # print('markers', markers)
    form = CreateNewPresetForm(user=request.user)
    context.update(form=form)
    return render(request, 'create_preset.html', context)
