## dropbox-version-diff
Scripts to get revision history for a given file and to diff that file.

## Setup
### Getting Project
```sh
git clone ssh://git@github.com/beeryardtech/dropbox-diff.git
cd dropbox-diff

# Start virtualenv!
source virt.sh

## Get packages
pip install -r requirements.txt

## Do the coding!

## Do a build!
pyb
```

### Initial Project Setup
```sh
# Install and run virtualenv,
# to store local modules
pip install virtualenv

# Save the virtual env off in home directory.
# virtualenv does not play nice with dropbox
virtualenv ~/.virtualenv/dbdiff
source virt.sh

# Use pybuilder to setup build scripts and scaffolding
# Use default options. Include all the plugins.
pip install dropbox configparser argparser pybuilder
pyb --start-project

# XXX - if available run the requirements.txt to get all the packages
pip install -r requirements.txt

## Finally, publish the project
pyb install_dependencies publish
```
