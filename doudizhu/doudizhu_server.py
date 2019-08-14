import doudizhu

room_pool = {}

def join_room(roomId, uid):
    if roomId not in room_pool:
        return None
    return room_pool[roomId].player_join(uid)
    


def leave_room(roomId, uid):
    if roomId not in room_pool:
        return None
    return room_pool[roomId].player_leave(uid)

def get_room_players(roomId):
    if roomId not in room_pool:
        return None
    return room_pool[roomId].get_players()


def be_ready_in_room(roomId, uid):
    pass

def cancel_ready_in_room(roomId, uid):
    pass

def get_ready_list_in_room(roomId):
    pass

def act_in_room(roomId, uid, action):
    if roomId not in room_pool:
        return None
    return room_pool[roomId].act(uid, action)