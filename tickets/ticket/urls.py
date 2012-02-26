from django.conf.urls.defaults import *

urlpatterns = patterns('ticket.views',
	#('^$', 'home'),
	('queue/(?P<queue_name>\w+)/$', 'queue'),
	('new/$', 'ticket_new'),
	('ticket/(?P<ticket_id>\w+)/$', 'ticket'),
	#('/$', 'ticket_list'),
	('list/', 'ticket_list'),
	('list/(?P<num>\d+)/$', 'ticket_list'),
	('list/(?P<num>\d+)/(?P<ordering>\d+)/$', 'ticket_list'),
	#('tickets/(?
)


    