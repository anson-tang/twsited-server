#!/usr/bin/env python
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Don Li <donne.cn@gmail.com>
# License: Copyright(c) 2012 Don.Li
# Summary: 

import time
import Queue

from twisted.internet import reactor, defer 
from datetime import datetime
from db import POOL
from log import log
from constant import *
from table_fields import TABLE_FIELDS, TABLE_HAD_DELETED, TABLE_NO_AI



TABLE_PREFIX = 'tb_'

@defer.inlineCallbacks
def sync_dirty_attributes(queue, loop=True):
    qsize = queue.qsize()
    if qsize > 0:
        log.info("sync data to db. dirty attrib length:%s." % qsize)
        if loop:
            sync_cnt = min(qsize, MAX_SYNC_CNT_PER_LOOP)
        else:
            sync_cnt = qsize

        i = 0
        while i < sync_cnt:
            i += 1

            try:
                attrib = queue.get_nowait()
                yield attrib.syncdb()
            except Queue.Empty:
                break
            except:
                pass
    if loop:
        reactor.callLater(SYNC_DB_INTERVAL, sync_dirty_attributes, queue)
    else:
        log.debug('End sync db, dirty attributes length {0}, loop:{1}'.format(
            queue.qsize(), loop))


try:
    DIRTY_ATTRIBUTES
except NameError:
    DIRTY_ATTRIBUTES = Queue.Queue()
    reactor.callLater(SYNC_DB_INTERVAL, sync_dirty_attributes, DIRTY_ATTRIBUTES)
    reactor.addSystemEventTrigger('before', 'shutdown', sync_dirty_attributes, DIRTY_ATTRIBUTES, False)


class AttributeError(Exception):pass

class Attribute(object): #Present one row in db
    def __init__(self, name):
        self.__name = name
        self.__attrib_id = 0
        self.__new = False
        self.__del = False
        self.__dirty = False

        self.__dirty_fields = []
        
        self.__fields = TABLE_FIELDS[self.__name][0] if name in TABLE_NO_AI \
            else [ v for v in TABLE_FIELDS[self.__name][0] if v != 'id'] 
        self.__time_fields = TABLE_FIELDS[self.__name][1]
 
    @property
    def table(self):
        return TABLE_PREFIX + self.__name

    @property
    def value(self):
        dv = {'id': self.__attrib_id}
        for k, v in self.__dict__.iteritems():
            if not k.startswith('_'):
                if isinstance(v, datetime):
                    v = int(time.mktime(v.timetuple()))
                dv[k] = v

        return dv

    def new_value(self):
        new_value = [self.__attrib_id]
        for field in self.__fields:
            v = self.__dict__[field]
            if isinstance(v, datetime):
                v = int(time.mktime(v.timetuple()))
            new_value.append(v)

        return new_value

    def __str__(self):
        return str(self.value)
    __repr__ = __str__

    @property
    def attrib_id(self):
        return self.__attrib_id

    @defer.inlineCallbacks
    def new(self, **kwargs):
        _dirty_fields = []
        _values = []

        for k, v in kwargs.iteritems():
            _dirty_fields.append(k)
            if k in self.__time_fields:
                _v = datetime.now() if v is None else v
                if not isinstance(v, datetime):
                    v = datetime.fromtimestamp( v )
            _values.append(v)
        # init __time_fields
        for k in self.__time_fields:
            if kwargs.has_key(k):
                continue
            _dirty_fields.append(k)
            v = int(time.time())
            kwargs[k] = v
            v = datetime.fromtimestamp(v)
            _values.append(v)
        # init deleted
        if self.__name in TABLE_HAD_DELETED:
            kwargs['deleted'] = 0
            _dirty_fields.append('deleted')
            _values.append(0)

        self.__dict__.update(kwargs)
        _sql = 'INSERT INTO %s (' % self.table  + ','.join(_dirty_fields) + ') VALUES ('  + ','.join(['%s'] * len(_values)) + ')'
 
        if self.__name in TABLE_NO_AI:
            yield POOL.insert(_sql, _values)
            self.__attrib_id = kwargs['id']
        else:
            self.__attrib_id = yield POOL.insert(_sql, _values)
        raise defer.returnValue(self.__attrib_id)

    @staticmethod
    @defer.inlineCallbacks
    def load(name, where=None, multirow=False):
        fields = TABLE_FIELDS[name][0]
        where = dict() if where is None else where

        if name in TABLE_HAD_DELETED:
            where['deleted'] = 0

        _sql = 'SELECT {0} FROM {1} WHERE {2};'.format(','.join(fields), TABLE_PREFIX + name, \
            '1 AND' + ' AND '.join([' %s=%s' % (k, "'%s'" % v if isinstance(v, (str, unicode)) else v ) for k, v in where.iteritems()]))
        _dataset = yield POOL.query(_sql)

        attribs  = {}
        if not _dataset:
            raise defer.returnValue(attribs if multirow else None)

        if multirow is False:
            _attr = Attribute(name)
            _attr.update(False, **dict(zip(fields, _dataset[0])))
            raise defer.returnValue(_attr)

        for row in _dataset:
            _attr = Attribute(name)
            _attr.update(False, **dict(zip(fields, row)))
            attribs[_attr.attrib_id] = _attr

        raise defer.returnValue(attribs)

    def update(self, _dirty=False, **kwargs):
        if 'id' in kwargs:
            self.__attrib_id = kwargs.pop('id')
        for k in self.__time_fields:
            v = kwargs[k]
            kwargs[k] = int(time.mktime(v.timetuple())) if isinstance(v, datetime) else v
        self.__dict__.update(kwargs)

        if _dirty:
            for k in kwargs.keys():
                if not k.startswith('_'):
                    self.dirty(k)

    def delete(self):
        if self.__attrib_id > 0:
            self.__del = True
            self.dirty()

    def __setattr__(self, attr_name, attr_value):
        self.__dict__[attr_name] = attr_value
        if not attr_name.startswith('_'):
            self.dirty(attr_name)

    def dirty(self, k=None):
        if not self.__dirty:
            DIRTY_ATTRIBUTES.put(self)
            self.__dirty = True

        if k and k not in self.__dirty_fields:
            self.__dirty_fields.append(k)

    def clean(self):
        self.__dirty = False
        del self.__dirty_fields[:]

    def __gen_update_value(self, fields):
        _sql = "UPDATE %s SET {0} WHERE id='%s'" % (self.table, self.__attrib_id)
        values = []
        fields_str = ''

        field_num = 1
        for field in fields:
            v = getattr(self, field)
            if field in self.__time_fields and not isinstance(v, datetime):
                v = datetime.fromtimestamp(v)
            values.append(v)

            if field_num < len(fields):
                fields_str += '{0}=%s,'.format(field)
            else:
                fields_str += '{0}=%s'.format(field)
            field_num += 1

        _sql = _sql.format(fields_str)

        return _sql, values

    @defer.inlineCallbacks
    def syncdb(self):
        if self.__dirty:
            _dirty_fields = self.__dirty_fields[:]

            if len(_dirty_fields) == 0 and False == self.__del:
                log.info('no dirty_fields! table name:{0}, attrib_id:{1}.'.format( self.table, self.__attrib_id ))
                raise defer.returnValue(None)

            _sql = ''

            try:
                if self.__del:
                    yield db.execute('DELETE FROM {0} WHERE id={1};'.format(self.table, self.__attrib_id))
                else:
                    _sql, _v = self.__gen_update_value(_dirty_fields)
                    if _v:
                        yield POOL.execute(_sql, _v)
                    else:
                        log.warn('Update error. table: {0}, cid: {1}, sql: {2}, dirty: {3}.'.format(\
                            self.table, self.__attrib_id, _sql, self.__dirty_fields))
            except:
                log.exception('[ SQLERROR ]table:{0}, id:{1}, dirty:{2}, new:{3}, dirty_fields:{4}, sql:{5}'.format(
                    self.table, self.__attrib_id, self.__dirty, self.__new, self.__dirty_fields, _sql))
            else:
                self.clean()
