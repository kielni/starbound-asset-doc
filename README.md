# Starbound asset-doc

Generate searchable documentation for a tree Starbound of assets.

### search

Search object and statuseffect names and descriptions

<img src="https://github.com/kielni/starbound-asset-doc/blob/master/screenshots/sb_search.png" width="300">

### object properties

List of all properties in .object files. Each property has a type, list of sample values, and links to objects where it's used

<img src="https://github.com/kielni/starbound-asset-doc/blob/master/screenshots/sb_object_props.png" width="300">

### object

Name, image, description, file path, and JSON contents. Values for `sitStatusEffect` and `statusEffect` are linked to the statuseffect page.

<img src="https://github.com/kielni/starbound-asset-doc/blob/master/screenshots/sb_object.png" width="450">

### statuseffect properties

List of all properties in .statuseffect files. Each property has a type, list of sample values, and links to statuseffects where it's used

<img src="https://github.com/kielni/starbound-asset-doc/blob/master/screenshots/sb_statuseffect_props.png" width="450">

### statuseffect

Name and JSON contents, plus a list of objects where the effect is used.

<img src="https://github.com/kielni/starbound-asset-doc/blob/master/screenshots/sb_statuseffect.png" width="300">

## prerequisites

install <a href="https://www.python.org/downloads/">Python 3.5+</a>

install <a href="https://git-scm.com/downloads">git</a>

<a href="https://starbounder.org/Modding:Basics#Step_1_-_Unpacking_Assets">unpack Starbound assets</a>
from Starbound directory
- Mac: `osx/asset_unpacker assets/packed.pak unpacked`
- Windows: `win32\asset_unpacker.exe assets\packed.pak unpacked`

## setup

in the Starbound directory (ie: Steam/steamapps/common/Starbound)

    git clone https://github.com/kielni/starbound-asset-doc.git
    cd starbound-asset-doc
    pip install -r requirements.txt
    python3 index.py ../unpacked

view docs at http://localhost:8000/asset-doc/index.html

