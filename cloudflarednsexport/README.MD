# Cloudflare DNS Exporter

----
## What is Cloudflare DNS Exporter?
Cloudflare DNS Exporter is a tool to backup your DNS Zone file using the Cloudflare API.  
Run as a cron-job or scheduled task to periodically back up your DNS settings from Cloudflare. 

----
## Usage
python cloudflarednsexport.py \
--bucketname bucketnamehere \
--apikey CloudflareAPIKey \
--email CloudflareAccountEmail \
--zone YourCloudflareZone (like example.com)

----
## Why
Posterity.  
If you've ever lost, corrupted or accidentally changed your DNS having a backup of what it used to be can be a great help. 
