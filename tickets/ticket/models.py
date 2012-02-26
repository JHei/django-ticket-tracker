from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, Form
from django import forms

STATUS_CODES = (
	(1, 'New'),
    (2, 'Open'),
    (3, 'Stalled'), 
    (4, 'Resolved'),
    (5, 'Rejected'),
    (6, 'Deleted'),
    )

class TicketQueueManager(models.Manager):
	def new_count(self):
		return self.filter(status=1)
	def open_count(self):
		return self.filter(status=2)
	def stalled_count(self):
		return self.filter(status=3)
	
class TicketQueue(models.Model):
	title = models.CharField(max_length=100)
	owner = models.ForeignKey(User)
	# Choose whether clients can put their ticket in this queue
	public = models.BooleanField()
	class Admin:
		search_fields = ('title', 'owner')
		ordering = ('title')
	def url(self):
		return self.title.replace(' ', '_')
	def __str__(self):
		return self.title
	objects = TicketQueueManager()
		
class Ticket(models.Model):
	"""Trouble tickets"""
	title = models.CharField(max_length=100)
	queue = models.ForeignKey(TicketQueue)
	submitted_date = models.DateField(auto_now_add=True)
	modified_date = models.DateField(auto_now=True)
	due_date = models.DateField()
	submitter = models.ForeignKey(User, related_name="submitter")
	submitter_email = models.EmailField()
	owner = models.ForeignKey(User, blank=True, null=True)
	description = models.TextField(blank=True)
	status = models.IntegerField(default=1, choices=STATUS_CODES)
	priority = models.IntegerField(default=1,)

	
	class Admin:
		list_display = ('title', 'priority', 'status', 'submitted_date', 'submitter', 
			'submitted_date', 'modified_date')
		search_fields = ('title', 'description',)

	class Meta:
		ordering = ('priority', 'modified_date', 'title')

	def __str__(self):
		return self.title
	def status_pretty(self):
		return STATUS_CODES[self.status][1]
		
class TicketComment(models.Model):
	"""Comment on a Ticket"""
	commenter = models.ForeignKey(User, related_name="commenter")
	content = models.TextField()
	ticket = models.ForeignKey(Ticket)
	
	class Admin:
		list_display = ('ticket', 'commenter', 'content')
		search_fields = ('content')
	def __str__(self):
		return "%s: (%s) %s" % (self.ticket.title, self.commenter, self.content[:30])
	
# New Ticket For 
class NewTicketForm(ModelForm):
	
	class Meta:
		model = Ticket
		exclude = ('submitted_date', 'modified_date', 'due_date', 'submitter', 'submitter_email', 'assigned_to', 'status', 'priority')
	def save(self, commit=True, force_insert=False, force_update=False):
		pass
class NewTicketCommentForm(Form):
	content = forms.CharField(max_length=1000, widget=forms.Textarea)
	#def save(self, commit=True, force_insert=False, force_update=False):
		
class UpdateTicketForm():
	class Meta:
		model = Ticket
	def save(self, commit=True, force_insert=False, force_update=False):
		pass