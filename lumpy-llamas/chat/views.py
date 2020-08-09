import logging
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from core.helpers import jsonbody
from chat.models import _model_field_limits, User, ChatRoom, ChatRoomUser


logger = logging.getLogger(__name__)


@login_required
def chat_lobby(request):
    return JsonResponse(dict())


@login_required
def chat_room(request, room_name):
    return JsonResponse({'room_name': room_name})


@login_required
def chat_users(request):
    current_user = request.user
    users = [{'user': user.username} for user in User.objects.filter(~Q(username=current_user)).order_by('username')]
    return JsonResponse({'users': users})


CHAT_ROOM_SCHEMA = {
    'type': 'object',
    'required': ['roomName', 'private', 'users'],
    'properties': {
        'roomName': {
            'type': 'string',
            'maxLength': _model_field_limits['ChatRoom__name__max_length'],
            'minLength': 1,
        },
        'private': {
            'type': 'boolean',
        },
        'users': {
            'type': 'array',
            'items': {
                'type': ['string']
            }
        }
    },
}


@login_required
@jsonbody(CHAT_ROOM_SCHEMA)
def go_to_chat_room(request, data):
    requesting_user = request.user.username
    room_name = data.get('roomName')
    is_private = data.get('private')
    permitted_users = data.get('users', [])
    permitted_users.append(requesting_user)

    print(requesting_user, room_name, is_private)
    try:
        if not room_name.isalnum():
            message = 'Invalid chat room name. Names must be alphanumeric.'
            is_valid = False
        else:
            message = 'Ok'
            is_valid = True

            room = ChatRoom.objects.filter(name=room_name)

            if room.exists():
                # Entering an existing room
                room = ChatRoom.objects.filter(name=room_name).first()

                if room.is_private:
                    requesting_user_record = User.objects.get(username=requesting_user)
                    permitted = ChatRoomUser.objects.filter(
                            chat_room_id=room.pk, user_id=requesting_user_record.pk
                        ).exists()

                    if not permitted:
                        is_valid = False
                        message = 'This room is private and you are not on the permitted users list.'
            else:
                # Creating a new room and entering
                if is_private:
                    if len(permitted_users) < 2:
                        message = 'You need at least one other permitted user.'
                        is_valid = False
                    else:
                        with transaction.atomic():
                            room = ChatRoom(name=room_name, is_private=True)
                            room.save()

                            user_records = User.objects.filter(username__in=permitted_users)
                            records = [ChatRoomUser(chat_room_id=room, user_id=user) for user in user_records]
                            ChatRoomUser.objects.bulk_create(records)
                else:
                    room = ChatRoom(name=room_name, is_private=True)
                    room.save()

    except Exception:
        logger.exception('Error occurred in validating chat room name')
        message = 'An error occurred in going to the chat room, please contact an administrator'
        is_valid = False

    return JsonResponse({'valid': is_valid, 'message': message})
