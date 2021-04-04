from contacts.models import Contact

def notifications(request):
    unread_messages = Contact.objects.filter(
        recipient=request.user,
        message_read=False).count()
    return {'unread_messages': unread_messages}