from google.cloud import storage
from os import environ as env
import json
import enc


class GoogleStorage:
    def __init__(self):

        self.storage_client  = self.creds()

        pass

    def creds(self):


        cred_dict = json.loads(enc.decrypt(env.get('gstorage')))


        creds = storage.Client.from_service_account_info(
            info=cred_dict)

        return creds

    def check(self):

        buckets=self.storage_client.list_buckets()
        for bucket in buckets:
            print(bucket.name)

        return

    def upload_to_gcs(self, file):
        # Initialize Google Cloud Storage client
        storage_client = self.storage_client

        # Get bucket
        bucket_name = "dvbr_images"  # Replace with your bucket name
        bucket = storage_client.bucket(bucket_name)

        # Create a blob and upload the file
        blob = bucket.blob(file.filename)
        blob.upload_from_string(
            file.read(),
            content_type=file.content_type
        )

        # Return the public URL
        return blob.public_url



    def upload_to_bucket(self, blob_name, path_to_file, bucket_name):
        """ Upload data to a bucket"""

        # Explicitly use service account credentials by specifying the private key
        # file.
        storage_client = self.storage_client

        # print(buckets = list(storage_client.list_buckets())

        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(path_to_file)

        # returns a public url
        return blob.public_url

    def allowed_file(self, filename):
        # Define allowed file extensions
        print(filename)

    def list_files_in_bucket(self):
        try:
            # Initialize Google Cloud Storage client
            storage_client = self.storage_client

            # Get bucket
            bucket_name = "dvbr_images"  # Replace with your bucket name
            bucket = storage_client.bucket(bucket_name)

            # List all blobs/files in the bucket
            blobs = bucket.list_blobs()

            # Create list of file names and URLs
            files = []
            for blob in blobs:
                files.append({
                    'name': blob.name,
                    'url': blob.public_url,
                    'size': blob.size,
                    'updated': blob.updated
                })

            return files

        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

if __name__ == '__main__':
    th = GoogleStorage()
    th.check()