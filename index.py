import argparse
import copy
import glob
import http.server
import json
import os
import re
import shutil
import socketserver
import traceback

from jinja2 import Template

parser = argparse.ArgumentParser(description='Generate mod docs')
parser.add_argument('path', help='path to root of unpacked assets tree')
parser.add_argument('--port', dest='port', type=int, default=8000, help='port for server')
args = parser.parse_args()


def read_json(fn, prefix):
    with open(fn) as f:
        # // and /* */ comments aren't valid JSON
        data = re.sub(r'//.*', '', f.read())
        data = re.sub(r'/\*.*?\*/', '', data, flags=re.DOTALL)
        try:
            obj = json.loads(data)
            # relative path
            path = re.sub(prefix, '', fn).replace('\\', '/')
            obj['full_path'] = path
            parts = path.split('/')
            obj['path'] = '/'.join(parts[:-1])
            return obj
        except json.decoder.JSONDecodeError as e:
            print('error parsing %s' % (fn))
            traceback.print_exc()
            return None


def collect_keys(props, obj):
    for k in obj.keys():
        data_type = re.match(r".*?'(.*?)'>", str(type(obj[k]))).group(1)
        props.setdefault(k, {
            'name': k,
            'type': data_type,
            'objects': set(),
            'values': set(),
        })
        name = obj.get('objectName', obj.get('name'))
        props[k]['objects'].add(name)
        if data_type == 'dict':
            continue
        if data_type == 'list':
            for val in obj[k]:
                try:
                    props[k]['values'].add(str(val))
                except TypeError:
                    props[k]['values'].add('dict')
        else:
            props[k]['values'].add(str(obj[k]))


# find object files
def read_objects(prefix):
    path = '%s/objects' % prefix
    object_files = glob.glob('%s/**/*.object' % path, recursive=True)
    print('%s objects in %s' % (len(object_files), path))
    objects = {}
    props = {}
    effects = {}
    idx = 0
    for fn in object_files:
        obj = read_json(fn, prefix)
        idx += 1
        if not idx % 100:
            print('%s/%s' % (idx, len(object_files)))
        obj['img'] = '%s/%s.png' % (obj['path'], obj['objectName'])
        objects[obj['objectName']] = obj
        collect_keys(props, obj)
        for eff_key in ['sitStatusEffects', 'statusEffects']:
            for effect in obj.get(eff_key, []):
                effects.setdefault(effect, [])
                effects[effect].append(obj['objectName'])
    return {
        'objects': objects,
        'props': props,
        'effects': effects
    }


def read_status_effects(prefix):
    path = '%s/stats/effects' % prefix
    effect_files = glob.glob('%s/**/*.statuseffect' % path, recursive=True)
    print('%s effects in %s' % (len(effect_files), path))
    effects = {}
    props = {}
    idx = 0
    for fn in effect_files:
        obj = read_json(fn, prefix)
        idx += 1
        if not idx % 100:
            print('%s/%s' % (idx, len(effect_files)))
        name = obj['full_path'].split('/')[-1].replace('.statuseffect', '')
        effects[name] = obj
        collect_keys(props, obj)
    return {
        'effects': effects,
        'props': props
    }


def read_template(fn):
    with open('templates/%s.jinja2' % fn) as f:
        return Template(f.read())


def write_file(out_fn, templates, context):
    with open(out_fn, 'w') as f:
        for template in templates:
            f.write(template.render(context))
    #print('wrote %s' % out_fn)


def exclude_meta(src_obj):
    obj = copy.copy(src_obj)
    for key in ['path', 'img', 'full_path', 'objects']:
        if key in obj:
            del obj[key]
    return obj


def write_props(key, props, out_path, header, footer):
    body = read_template(key)
    props_copy = exclude_meta(props)
    for p in props_copy:
        vals = list(props[p]['values'])
        vals.sort()
        props[p]['values'] = vals[:10]
        props[p]['value_count'] = len(vals)
    context = {
        'active': key,
        'props': props_copy
    }
    write_file('%s/%s.html' % (out_path, key), [header, body, footer], context)


def write_objects(obj_type, objects, out_path, header, footer):
    body = read_template(obj_type)
    for key in objects:
        obj = exclude_meta(objects[key])

        json_data = json.dumps(obj, indent=4)
        # fix up links in statusEffects and sitStatusEffects
        # "<a href=\"/asset-doc/statuseffect/bed1.html\">bed1</a>"
        json_data = re.sub(r'<a href=\\"(.*?)\\">', r'<a href="\g<1>">', json_data)
        json_data = re.sub(r'<(\w+)>', r'&lt;\g<1>&gt;', json_data)
        context = {
            'active': obj_type,
            'path': objects[key].get('path'),
            'img': objects[key].get('img'),
            'json': json_data,
            'objects': objects[key].get('objects'),
        }
        context.update(obj)
        out_fn = '%s/%s/%s.html' % (out_path, obj_type, obj.get('objectName', obj.get('name')))
        write_file(out_fn, [header, body, footer], context)


def link_effects(objects, effects):
    for obj_name in objects:
        obj = objects[obj_name]
        for eff_key in ['sitStatusEffects', 'statusEffects']:
            if not eff_key in obj:
                continue
            links = []
            for effect in obj[eff_key]:
                key = effect.replace('"', '')
                if key in effects:
                    links.append('<a href="/asset-doc/statuseffect/%s.html">%s</a>' % (key, effect))
                else:
                    links.append(effect)
            obj[eff_key] = links


def write_json(objects, effects, out_path):
    # json data for search
    out_fn = '%s/objects.json' % (out_path)
    obj_list = []
    for key in objects:
        obj = objects[key]
        name = obj.get('objectName', obj.get('name'))
        obj_list.append({
            'name': name,
            'path': obj['path'],
            'filename': '/asset-doc/object/%s.html' % (name),
            'img': obj['img'],
            'description': obj.get('shortdescription', '')
        })
    for key in effects:
        obj = effects[key]
        name = obj.get('name')
        obj_list.append({
            'name': obj.get('name'),
            'filename': '/asset-doc/statuseffect/%s.html' % (name),
            'img': obj.get('icon'),
            'description': obj.get('label', '')
        })
    with open(out_fn, 'w') as f:
        f.write(json.dumps(obj_list))
    print('wrote %s' % out_fn)


def main():
    obj = read_objects(args.path)
    effects = read_status_effects(args.path)
    link_effects(obj['objects'], effects['effects'])
    header = read_template('header')
    footer = read_template('footer')
    out_path = '%s/asset-doc' % args.path
    # objects
    if not os.path.exists('%s/object' % out_path):
        os.makedirs('%s/object' % out_path)
    write_props('object-props', obj['props'], out_path, header, footer)
    write_objects('object', obj['objects'], out_path, header, footer)
    # status effects
    if not os.path.exists('%s/statuseffect' % out_path):
        os.makedirs('%s/statuseffect' % out_path)
    for effect in obj['effects']:
        if effect not in effects['effects']:
            continue
        effects['effects'][effect]['objects'] = obj['effects'][effect]
    write_props('statuseffect-props', effects['props'], out_path, header, footer)
    write_objects('statuseffect', effects['effects'], out_path, header, footer)
    # search
    write_json(obj['objects'], effects['effects'], out_path)
    shutil.copy('templates/style.css', '%s/style.css' % out_path)
    shutil.copy('templates/app.js', '%s/app.js' % out_path)

    os.chdir(args.path)
    with socketserver.TCPServer(('', args.port), http.server.SimpleHTTPRequestHandler) as httpd:
        print('load http://localhost:%s/index.html in a browser' % args.port)
        httpd.serve_forever()

if __name__== "__main__":
    main()
