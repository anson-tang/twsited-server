#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: all table fields
# about deleted: when 1-invalid 0-normal

TABLE_HAD_DELETED = ('pvp_room', )
TABLE_NO_AI = ('character', )


TABLE_FIELDS = {
    'character': (('id', 'machine_code', 'nickname', 'exp', 'coin', 'create_time'),
        ('create_time',)),
    'pvp_room': (('id', 'uid', 'room_id', 'rank', 'scores', 'join_time', 'leave_time', 'deleted'),
        ('join_time', 'leave_time')),
}

