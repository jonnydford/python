import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from datetime import date
import boto3
import argparse
import CloudFlare
import tempfile

parser = argparse.ArgumentParser(description='Backup your Cloudflare DNS records to S3')
parser.add_argument('--bucketname', help='Your S3 Bucket Name', required=True)
parser.add_argument('--apikey', help='Your Cloudflare API Key',required=True)
parser.add_argument('--email', help='Your Cloudflare Email Address',required=True)
parser.add_argument('--zone', help='Your Cloudflare Zone Identifier', required=True)
args = parser.parse_args()

def main():

    try:
        zone_name = arg.zone
    except IndexError:
        exit('usage: cloudflaredns.py zone (zone is in style example.com)')

    cf = CloudFlare.CloudFlare(email=args.email, token=args.apikey)

    # grab the zone identifier
    try:
        params = {'name': zone_name}
        zones = cf.zones.get(params=params)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones %d %s - api call failed' % (e, e))
    except Exception as e:
        exit('/zones.get - %s - api call failed' % (e))

    if len(zones) == 0:
        exit('/zones.get - %s - zone not found' % (zone_name))

    if len(zones) != 1:
        exit('/zones.get - %s - api call returned %d items' % (zone_name, len(zones)))

    zone_id = zones[0]['id']

    try:
        dns_records = cf.zones.dns_records.export.get(zone_id)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones/dns_records/export %s - %d %s - api call failed' % (dns_name, e, e))

    s3 = boto3.resource('s3')
    bucketName = args.bucketname
    today = date.today()
    filename = 'cloudflaredns%s.txt' % today

    # Uploads the given file using a managed uploader, which will split up large
    # files automatically and upload parts in parallel.
    try:
        s3.Bucket(bucketName).put_object(Key=filename, Body=dns_records) 
        print 'Uploading %s to Amazon S3 bucket %s' % \
        (filename, bucketName)
    except Exception, e:
        print "Couldn't upload to S3"
        sys.exit(3)

if __name__ == '__main__':
    main()

