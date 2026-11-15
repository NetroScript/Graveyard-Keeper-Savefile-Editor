import os

own_dir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(own_dir, 'data')
html_dir = os.path.join(data_dir, 'html')

version = os.path.join(data_dir, 'version')
item_version = os.path.join(data_dir, 'itemversion')
hashes = os.path.join(data_dir, 'hashes')
settings = os.path.join(data_dir, 'settings')
locals_json = os.path.join(data_dir, 'locals.json')
data_json = os.path.join(data_dir, 'data.json')
new_item_data_json = os.path.join(data_dir, 'new_item_data.json')

dump_skeleton_html = os.path.join(html_dir, 'dumpskeleton.html')
items_json = os.path.join(html_dir, 'items.json')
