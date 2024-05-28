# Custom QGIS Expression Engine functions

This repository contains a collection of custom functions for the QGIS Expression Engine. 
The functions are written in Python and can be added to your version of QGIS by following the steps below:

1. Download the repository as a ZIP file or simply the file of the function you want to take.
2. Open QGIS and go to **Settings > User Profiles > Open Active Profile Folder**.
3. In the opened folder, navigate to `python` > `expressions` folder.
4. Copy the downloaded file to the `expressions` folder.
5. Restart QGIS.
6. The new functions should now be available in the Expression Editor, based on their assigned group.

The functions are grouped by their purpose and are listed below:

## Date and Time

- `set_timezone` - Set the timezone of a datetime object.

## Custom (General)

- `wiki_description` - Get the description of a Wikipedia page by it's title.