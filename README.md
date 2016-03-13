## dropbox-version-diff
Scripts to get revision history for a given file and to diff that file.

## Setup
### Getting Project
```sh
# For Mac to install pip
sudo easy_install pip

# Clone the repo
git clone ssh://git@github.com/beeryardtech/dbdiff.py.git
cd dbdiff.py

# Start virtualenv!
source virt.sh

## Get packages
pip install -r requirements.txt

## Do the coding!

## Do a build!
pyb
```

### Setting up Dropbox
Login to htts://developer.dropbox.com and create a new "Dropbox API" app. Choose "Full Dropbox" access type and give it a name. Name has to be unique, so something like "{username}dbdiff". 

Now go to the newly created app's settings page, make a copy of `dbdiff.example.ini` and name it `dbdiff.ini`, and update its auth section. 

- app_key --> App Key
- app_secret --> App Secret
- app_token --> Generate an access token or leave blank and execute any of the commands

### Commands

The following are (or will be supported):

- check - Verify API by running through a list of API calls and tests them.
- get - Get a file at a specific revision
- put - Put a given file in Dropbox. By default, this is a forced update.
- revs - Get revision list of a given file

### Initial Project Setup
```sh
# Install and run virtualenv,
# to store local modules
sudo pip install virtualenv

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
