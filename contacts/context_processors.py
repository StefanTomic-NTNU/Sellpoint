from contacts.models import Contact

def notifications(request):
    if not request.user.is_authenticated:
        return {'unread_messages': 0}
    unread_messages = Contact.objects.filter(
        recipient=request.user,
        message_read=False).count()
    return {'unread_messages': unread_messages}