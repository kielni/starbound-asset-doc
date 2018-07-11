# Starbound asset-doc

Generate searchable documentation for a tree of Starbound assets.

The easiest way to get started making mods for Starbound is to start with the
stock Starbound assets. What goes into an object file? What status effects can you
use? Unpacking the stock Starbound assets results in a directory tree with
thousands of files, and no easy way to navigate through them. This project reads
object and status effect files, generates documentation files, and runs
a web server for browsing the content.

### search

Just start typing to search over 3,000 object and status effect names and descriptions.
Results display an image, name, and description; click to go to the detail page for the
object or status effect.

<img src="https://github.com/kielni/starbound-asset-doc/blob/master/screenshots/sb_search.png" width="300">

### object properties

Displays a list of all properties used in `.object` files.
Each property has a type, list of sample values, and links to objects that use the property.

<img src="https://github.com/kielni/starbound-asset-doc/blob/master/screenshots/sb_object_props.png" width="450">

### object

Displays the name, image, description, file path, and syntax-highlighted JSON contents of each `.object` file.
Values for `sitStatusEffect` and `statusEffect` are linked to the corresponding status effect page.

<img src="https://github.com/kielni/starbound-asset-doc/blob/master/screenshots/sb_object.png" width="450">

### statuseffect properties

Displays a list of all properties used in `.statuseffect` files.
Each property has a type, list of sample values, and links to status effects that use the property.

<img src="https://github.com/kielni/starbound-asset-doc/blob/master/screenshots/sb_statuseffect_props.png" width="450">

### statuseffect

Displays the name and and syntax-highlighted JSON contents of each `.statuseffect` file.
It also displays a list of linked objects that use the effect.

<img src="https://github.com/kielni/starbound-asset-doc/blob/master/screenshots/sb_statuseffect.png" width="300">

## prerequisites

<a href="https://www.python.org/downloads/">Python 3.5+</a>

<a href="https://git-scm.com/downloads">git</a>

a tree of <a href="https://starbounder.org/Modding:Basics#Step_1_-_Unpacking_Assets">unpacked Starbound assets</a>

from `Starbound` directory
- Mac: `osx/asset_unpacker assets/packed.pak unpacked`
- Windows: `win32\asset_unpacker.exe assets\packed.pak unpacked`

## setup

- get the location of your unpacked Starbound assets (here: `unpacked/` under the Starbound directory)

- in a terminal in the Starbound directory (ie: `Steam/steamapps/common/Starbound`)

```
git clone https://github.com/kielni/starbound-asset-doc.git
cd starbound-asset-doc
pip install -r requirements.txt
```

- index the content and start the server

```
python3 index.py ../unpacked
```

- go to http://localhost:8000/asset-doc/index.html to browse the generated docs

