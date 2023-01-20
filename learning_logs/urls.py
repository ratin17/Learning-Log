"""Defines URL patterns for learning_logs."""

from django.urls import path
from . import views
app_name = 'learning_logs'

urlpatterns = [
# Home page
path('', views.index, name='index'),

#Topic Page
path('topics/', views.topics, name='topics'),

#Individual Topic
path('topics/<int:topic_id>/', views.topic, name='topic'),



]