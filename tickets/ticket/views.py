from django.shortcuts import render_to_response
from django.template import RequestContext
from models import NewTicketForm, Ticket, TicketQueue, TicketComment, NewTicketCommentForm
from django.http import HttpResponse, HttpResponseForbidden
from django.core.mail import send_mail
import settings as SETTINGS

def get_user_tickets(user):
	return Ticket.objects.filter(owner=user)

def get_unowned_tickets():
	return Ticket.objects.filter(owner=None)

def get_new_ticket_form(request):
	form = NewTicketForm()
	#print request.user.is_authenticated
	if request.user.is_authenticated() == False:
		# Filter out non-public queues for non-admin users
		#print form.queue
		form.fields['queue'].queryset = TicketQueue.objects.filter(public=True)
	return form
	
def queue(request, queue_name, num=25):
	# Display all the tickets in a queue
	template_data = {}
	queue = TicketQueue.objects.get(title=queue_name.replace('_', ' '))
	template_data['queue'] = queue
	#template_data['tickets'] = Ticket.objects.filter(id=queue.id)[0:int(num)-1]
	template_data['tickets'] = queue.ticket_set.all()
	
	return render_to_response('queue.html',  context_instance=RequestContext(request, template_data,))
	
def ticket_new(request):
	# Add a ticket
	template_data = {}
	template_data['form'] = get_new_ticket_form()
	return render_to_response('new_ticket.html',  context_instance=RequestContext(request, template_data,))
	
def ticket(request, ticket_id):
	ticket = Ticket.objects.get(pk=int(ticket_id))
	if request.method == 'POST':
		form = NewTicketCommentForm(request.POST)
		if form.is_valid():
			ticket =  Ticket.objects.get(pk=int(ticket_id))
			comment = TicketComment(commenter = request.user, ticket=ticket, content=form.cleaned_data['content'])
			if request.POST.has_key('email'):
				subject = '[%s] [Comment] %s' % (SETTINGS.TICKET_APP_NAME, ticket.title)
				message = '%s left a comment on your ticket. \n%s \n<a href="%s/tickets/view/%d/">You can view your ticket here. </a>' % (request.user, form.cleaned_data['content'], SETTINGS.TICKET_DOMAIN, ticket.id) 
				from_email = SETTINGS.TICKET_FROM_EMAIL
				recipient_list = (ticket.submitter_email, )
				send_mail(subject, message, from_email, recipient_list)
			comment.save()
	
	# Display the information about a queue and every comment, POST or not.
	
	#print ticket.title
	# If user is not authenticated, forbidden
	# TODO change this to must be admin
	if request.user.is_authenticated() == False:
		return HttpResponseForbidden
	# IF user is authenticated, but doesn't own the ticket and isn't an admin, forbidden
	if request.user.is_authenticated() and ticket.owner != ticket.owner:
		if requesut.user.is_admin() == False:
			return HttpResponseForbidden
	
	template_data = {}
	# Pass ticket in as non-editable
	template_data['ticket'] = ticket
	
	comments = TicketComment.objects.filter(ticket=ticket)
	#print comments
	template_data['comments'] = comments
	comment_form = NewTicketCommentForm()
	template_data['comment_form'] = comment_form
	return render_to_response('ticket.html',  context_instance=RequestContext(request, template_data,))

def ticket_modify(request):
	template_data = {}
	pass

def ticket_list(request, num=None, ordering=None):
	if num == None:
		num = 25
	template_data = {}
	template_data['tickets'] = Ticket.objects.all()[0:int(num)-1]
	template_data['queues'] = TicketQueue.objects.all()
	template_data['user_tickets'] = get_user_tickets(request.user)
	template_data['unowned_tickets'] = get_unowned_tickets()
	template_data['form'] = get_new_ticket_form(request)
	return render_to_response('ticket_list.html',  context_instance=RequestContext(request, template_data,))