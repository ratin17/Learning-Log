from django.shortcuts import render, redirect

from .models import Topic, Entry
from .forms import EntryForm, TopicForm


# Create your views here.

def index(request):
 """The home page for Learning Log."""
 return render(request, 'learning_logs/index.html')


def topics(request):
    """Show all topics."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)

    # Make sure the topic belongs to the current user.
    # if topic.owner != request.user:
    #     raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request,topic_id):
    """Add a new topic."""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Display a blank or invalid form.
    context = {'form': form,'topic':topic}
    return render(request, 'learning_logs/new_entry.html', context)




def edit_entry(request,entry_id):
    """Add a new entry."""
    entry = Entry.objects.get(id=entry_id)
    topic=entry.topic

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            entry.save()
            return redirect('learning_logs:topic', topic.id)

    # Display a blank or invalid form.
    context = {'entry':entry,'form': form,'topic':topic}
    return render(request, 'learning_logs/edit_entry.html', context)