## Paraview Cinema Plugin

This plugin is intended to expose Paraview Cinema data via a restful interface.

To run this, the best thing to do is have nginx do the static serving and proxy
back to Girder. The `nginx.conf` does this on my system and the
`index-girder.html` refers to the API call created by the plugin.

The script at `scripts/pvcinema_import.py` creates a folder-item hierarch based
on a folder containing several cinema output folders (containing `info.json`
files).
