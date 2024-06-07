#!/bin/bash

# Run the PHP commands
php tempest.php --epg config=jiotv.config.xml invgz
php tempest.php --epg config=tataplay.config.xml invgz
php tempest.php --epg config=simper.config.xml invgz
php tempest.php --epg config=youtube.config.xml invgz
php tempest.php --xmlmerge xml=jiotv xml=tataplay out=merged gz

# Remove the specified XML files
rm tempest_config/epg/jiotv_original.xml
rm tempest_config/epg/jiotv.xml
rm tempest_config/epg/tataplay_original.xml
rm tempest_config/epg/tataplay.xml
rm tempest_config/epg/simper_epg_original.xml
rm tempest_config/epg/simper_epg.xml
rm tempest_config/epg/youtube_original.xml
rm tempest_config/epg/youtube.xml
rm tempest_config/epg/merged.xml

# Optional: print a message indicating the script has finished
echo "Script execution completed and specified files have been removed."
