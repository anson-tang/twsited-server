#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: all table fields
# about deleted: when 1-invalid 0-normal

TABLE_HAD_DELETED = ('ongoing', 'building', 'adventure', 'item', 'quest', 'mail', 'wild', 'soldier')
TABLE_NO_AI = ('character', )


TABLE_FIELDS = {
    'character': (('id', 'openid', 'nickname', 'gem', 'golds', 'burg_num', 'item_capacity', \
        'quest_over', 'vip_end_time', 'create_time'),
        ('vip_end_time', 'create_time')),
    'burg': (('id', 'uid', 'burg_id', 'is_current', 'name', 'food', 'wood', 'stone', 'steel', 'building_queue', \
        'soldier_queue', 'storage_max', 'protect_max', 'vehicle_max', 'wild_max', 'soldier_max', 'food_per_hour', \
        'wood_per_hour', 'stone_per_hour', 'steel_per_hour', 'level', 'exp', 'strength', \
        'might', 'attack_percent', 'hp_percent', 'resource_add', 'might_add', 'rate', \
        'status', 'total_point', 'death_time', 'last_strength_time', 'last_adventure_time', \
        'last_resource_time', 'create_time', 'px', 'py'), 
        ('death_time', 'last_strength_time', 'last_adventure_time', 'last_resource_time', 'create_time', )),
}

