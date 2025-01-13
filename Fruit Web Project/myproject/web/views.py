from django.shortcuts import render, redirect
from .forms import ProfileModelForm, FruitModelForm
from .models import Profile, Fruit


def index_page(request):
    profile = Profile.objects.first()

    context = {
        "profile": profile
    }
    return render(request, "web/index.html")


def dashboard_page(request):
    return render(request, "web/dashboard.html")


def fruit_create_page(request):
    profile = Profile.objects.first()
    form = FruitModelForm(request.POST or None)

    if form.is_valid():
        fruit = form.save(commit=False)
        fruit.profile = profile
        fruit.save()
        return redirect('home page', kwargs={id: fruit.id})

    context = {
        "profile": profile,
        "add_form": form
    }
    return render(request, "web/create-fruit.html", context)


def fruit_detail_page(request, id):
    profile = Profile.objects.first()
    context = {
        "profile": profile,
        "fruit": Fruit.objects.get(id=id),
    }

    return render(request, "web/details-fruit.html", context)


def fruit_edit_page(request, id):
    profile = Profile.objects.first()
    fruit = Fruit.objects.get(id=id)
    form = FruitModelForm(instance=fruit)

    context = {
        'edit_form': form,
        'profile': profile,
        'fruit': fruit
    }

    if request.method == 'POST':
        form = FruitModelForm(request.POST, instance=fruit)
        if form.is_valid():
            form.save()
            return redirect('dashboard page')

    return render(request, "web/edit-fruit.html", context)


def fruit_delete_page(request, id):
    profile = Profile.objects.first()
    fruit = Fruit.objects.get(id=id)
    form = FruitModelForm(instance=fruit)

    if request.method == 'POST':
        form = FruitModelForm(request.POST, instance=fruit)
        if form.is_valid():
            fruit.delete()
            return redirect('home page')

    context = {
        'delete_form': form,
        'profile': profile,
        'fruit': fruit
    }

    return render(request, "web/delete-fruit.html", context)


def profile_create_page(request):
    profile = Profile.objects.first()
    form = ProfileModelForm()

    if request.method == 'POST':
        form = ProfileModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard page')

    context = {
        "profile": profile,
        "add_form": form
    }

    return render(request, "web/create-profile.html", context)


def profile_details_page(request):
    profile = Profile.objects.get(id=id)
    context = {
        "profile": profile,
        "fruit": Fruit.objects.get(id=id),
    }

    return render(request, "web/details-profile.html", context)


def profile_edit_page(request):
    profile = Profile.objects.first()
    form = ProfileModelForm(instance=profile)

    context = {
        'edit_form': form,
        'profile': profile,
    }

    if request.method == 'POST':
        form = Profile(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard page')

    return render(request, "web/edit-profile.html", context)


def profile_delete_page(request):
    profile = Profile.objects.first()
    fruits = Fruit.objects.all()
    form = ProfileModelForm()
    if request.method == 'POST':
        fruits.delete()
        profile.delete()
        return redirect('index_page')
    context = {
        'delete_form': form,
        'profile': profile,
    }
    return render(request, "web/delete-profile.html", context)
