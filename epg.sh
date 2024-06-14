#!/bin/bash

# Run the PHP commands
php tempest.php --epg config=tempest.config.xml invgz
php tempest.php --epg config=jiotv.config.xml invgz
php tempest.php --epg config=tataplay.config.xml invgz

# Remove the specified XML files
rm tempest_config/epg/simper_original.xml
rm tempest_config/epg/simper.xml
rm tempest_config/epg/jiotv_original.xml
rm tempest_config/epg/jiotv.xml
rm tempest_config/epg/tataplay_original.xml
rm tempest_config/epg/tataplay.xml

# Optional: print a message indicating the script has finished
echo "Script execution completed and specified files have been removed."
