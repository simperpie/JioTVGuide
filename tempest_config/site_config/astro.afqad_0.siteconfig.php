<?php 
/*     Tempest EPG Generator (made by Kvanc)
https://github.com/K-vanc/Tempest-EPG-Generator.git  */
return array (
  'filename' => 'astro.com',
  'creator_name' => 'Simper',
  'creation_date' => '2024-05-21',
  'rev_no' => 'R0',
  'remarks' => 'Edit Url paths based on your local file locations | Edit Timezone based on your file | Edit culture info based on your files',
  'timezone' => 'UTC',
  'culture' => 'en',
  'max_day' => '7.1',
  'rating_system' => 'MY',
  'episodeOption' => '1',
  'keepindexpage' => 'on',
  'pastdayremover' => 'on',
  'url1' => 'https://github.com/AqFad2811/epg/raw/main/astro.xml',
  'requestOption1' => '1',
  'show' => '(<programme.*?<\\/programme>)||#include#channel="##channel##">',
  'start' => 'start="(\\d+)\\s',
  'start_format' => 'YmdHis',
  'stop' => 'stop="(\\d+)\\s',
  'stop_format' => 'YmdHis',
  'title' => '<title.*?>(.*?)<\\/',
  'desc' => '<desc.*?>(.*?)<\\/',
  'category' => '<category.*?>(.*?)<\\/',
  'showicon' => '<icon src="(.*?)"',
  'season' => '">S(\\d+)',
  'episode' => '">(?:S\\d+\\s)?E(\\d+)',
  'episode_total' => '">(?:S\\d+\\s)?E\\d+\\/(\\d+)',
  'channel_logo' => '||#add###cclogo##',
  'actor' => '<actor.*?>(.*?)<\\/',
  'director' => '<director>(.*?)<\\/',
  'rating' => '<rating.*?<value>(.*?)<\\/',
  'ccurl1' => 'https://github.com/AqFad2811/epg/raw/main/astro.xml',
  'ccrequestOption1' => '1',
  'ccchannel_block' => '<channel id.*?<\\/channel>',
  'ccchannel_id' => 'id="(.*?)"',
  'ccchannel_name' => '<display-name.*?>(.*?)<\\/',
  'ccchannel_logo' => '<icon src="(.*?)"',
);
?>