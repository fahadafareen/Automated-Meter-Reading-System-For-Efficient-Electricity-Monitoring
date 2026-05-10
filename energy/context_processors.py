from .models import chat

def admin_notifications(request):
    if request.session.get('logint') == 'admin':
        unread_count = chat.objects.filter(receiver='admin', is_read=False).count()
        return {'unread_chats_count': unread_count}
    return {'unread_chats_count': 0}
