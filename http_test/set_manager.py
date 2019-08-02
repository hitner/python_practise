import os
import re
import json
import time
import threading
import tornado.locks
from tornado.ioloop import IOLoop
from tornado.log import gen_log

location = '.'


class Status:
    last_index = 0
    index_file_map = {}


_status = Status()


def file_name(index, name):
    return "%s/%d_%s.json" % (location, index, name)


def init():
    _status.last_index = 0
    _status.index_file_map.clear()
    regular = re.compile(r"([0-9]+_)(.+)(\.json)")
    for entry in os.scandir(location):
        if entry.is_file():
            m = regular.match(entry.name)
            if m:
                stat_result = entry.stat()
                index = int(m.group(1)[0:-1])
                _status.index_file_map[index] = {
                    'index': index,
                    'name': m.group(2),
                    'size': stat_result.st_size,
                    'mtime': stat_result.st_mtime
                }
                if index > _status.last_index:
                    _status.last_index = index


def get_set_list():
    keys = _status.index_file_map.keys()
    sordedkeys = sorted(keys)
    result = []
    for key in sordedkeys:
        result.append(_status.index_file_map[key])
    return result


def add_set(content):
    name = content.get('name')
    if name:
        _status.last_index += 1
        filename = file_name(_status.last_index, name)
        fp = open(filename, 'w')
        string = json.dumps(content, indent=4, ensure_ascii=False)
        fp.write(string)
        fp.close()

        _status.index_file_map[_status.last_index] = {
            'index': _status.last_index,
            'name': name,
            'size': len(string),
            'mtime': time.time()
        }
        return _status.index_file_map[_status.last_index]


def get_set_content(set_index):
    fs = _status.index_file_map.get(set_index)
    if fs:
        with open(file_name(set_index, fs['name']), 'r') as fp:
            try:
                result = json.load(fp)
                return result
            except json.JSONDecodeError:
                return None


def delete_set(set_index):
    fs = _status.index_file_map.get(set_index)
    if fs:
        os.remove(file_name(set_index, fs['name']))
        del _status.index_file_map[set_index]
        return True


def patch_set(set_index, content):
    fs = _status.index_file_map.get(set_index)
    if fs:
        with open(file_name(set_index, fs['name']), "r+") as fp:
            try:
                data = fp.read()
                origin = json.loads(data)
                origin.update(content)
                final_string = json.dumps(origin, ensure_ascii=False, indent=4)
                new_name = content.get('name')
                if new_name and new_name != fs['name']:
                    with open(file_name(set_index, new_name), "w") as newfp:
                        newfp.write(final_string)
                    os.remove(file_name(set_index, fs['name']))
                    fs['name'] = new_name
                else:
                    fp.seek(0)
                    fp.write(final_string)
                    fp.truncate()
                fs['mtime'] = time.time()
                fs['size'] = len(final_string)
                return True
            except json.JSONDecodeError:
                return None


def post_interface(set_index, content):
    fs = _status.index_file_map.get(set_index)
    if fs:
        with open(file_name(set_index, fs['name']), "r+") as fp:
            try:
                data = fp.read()
                origin = json.loads(data)
                if 'interface' not in origin:
                    origin['interface'] = []
                origin['interface'].append(content)
                final_string = json.dumps(origin, ensure_ascii=False, indent=4)
                fp.seek(0)
                fp.write(final_string)
                fp.truncate()
                fs['mtime'] = time.time()
                fs['size'] = len(final_string)
                return True
            except json.JSONDecodeError:
                return None


def put_or_delete_interface(set_index, interface_index, content, delete_flag=0):
    fs = _status.index_file_map.get(set_index)
    if fs:
        with open(file_name(set_index, fs['name']), "r+") as fp:
            try:
                data = fp.read()
                origin = json.loads(data)
                interfaces = origin.get('interface')
                if interfaces:
                    if len(interfaces) > interface_index:
                        if delete_flag:
                            del interfaces[interface_index]
                        else:
                            interfaces[interface_index] = content
                        final_string = json.dumps(origin, ensure_ascii=False, indent=4)
                        fp.seek(0)
                        fp.write(final_string)
                        fp.truncate()
                        fs['mtime'] = time.time()
                        fs['size'] = len(final_string)
                        return True
            except json.JSONDecodeError:
                return None
