## dropbox-version-diff
Scripts to get revision history for a given file and to diff that file.

## Setup
### Getting Project
```sh
git clone ssh://git@github.com/beeryardtech/dropbox-diff.git
cd dropbox-diff

# Start virtualenv!
source virt_env/bin/activate

## Do the coding!

## Do a build!
pyb
```

### Initial Project Setup
```sh
# Install and run virtualenv,
# to store local modules
pip install virtualenv
virtualenv virt_env
source virt_env/bin/activate

# Use pybuilder to setup build scripts and scaffolding
# Use default options. Include all the plugins.
pip install pybuilder
pyb --start-project

## Finally, publish the project
pyb install_dependencies publish
```
