from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')
    # return HttpResponse("The landing page for Learning Log")

@login_required
def topics(request):
    """List topics view (seems more like controller)"""
    # return HttpResponse("Here is the list of all topics")
    topics = Topic.objects.filter(owner=request.user)
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """List entries for a topic"""
    # entries = Entry.objects.filter(topic=topic_id).order_by("date_added")
    topic = Topic.objects.get(pk=topic_id)
    check_topic_owner(topic, request)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Controller to create a new learning topic (or is it sub-topic - bleh, mixed)"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add something you learned for a given topic."""
    topic = Topic.objects.get(pk=topic_id)
    check_topic_owner(topic, request)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # because EntryForm is different object then Entry
            # and we need to create a row in the Entry nu table
            # form.save() will also do the same (= create new Entry), and will return the Entry object
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id)
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Update your scratch note"""
    entry = Entry.objects.get(pk=entry_id)
    check_topic_owner(entry.topic, request)
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', entry.topic.id)
    # return HttpResponse(output)
    context = {'entry': entry, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    """Delete an entry. Isn't the name self-explanatory?"""
    entry = Entry.objects.get(pk=entry_id)
    check_topic_owner(entry.topic, request)
    entry.delete()
    return redirect('learning_logs:topic', entry.topic.id)

def check_topic_owner(topic, request):
    if topic.owner != request.user:
        raise Http404
