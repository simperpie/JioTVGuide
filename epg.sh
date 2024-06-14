#!/bin/bash

# Run the PHP commands
php tempest.php --epg config=tempest.config.xml invgz

# Remove the specified XML files
rm tempest_config/epg/simper_epg_original.xml
rm tempest_config/epg/simper_epg.xml

# Optional: print a message indicating the script has finished
echo "Script execution completed and specified files have been removed."