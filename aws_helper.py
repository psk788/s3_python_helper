import logging

from botocore.exceptions import ClientError
import boto3
import os

def get_base_directory(path, levels_up=1):
    normalized_path = os.path.normpath(path)
    top_directory = normalized_path
    for _ in range(levels_up):
        top_directory = os.path.dirname(top_directory)
    return top_directory

def replace_filename_with_new(path, new_filename):
    """Replace the filename portion of the path with a new filename,
       and optionally add new folders to the path.

    :param path: The original file path
    :param new_filename: The new filename to replace the old one
    :return: The new file path with the new filename
    """
    dir_name = os.path.dirname(path)
    new_path = os.path.join(dir_name, new_filename)
    return new_path
def upload_file_to_s3(bucket, file_name, s3_prefix='', object_name=None, use_whole_path=False):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param s3_prefix: Prefix in the S3 bucket under which to store the folder's contents
    :param object_name: S3 object name. If not specified, file_name is used
    :param use_whole_path: If true, uses the whole path of the file to create the object name (mirror folder structure
    in s3 relative to execution directory)
    :return: True if file was uploaded, else False
    """
    if object_name is None:
        object_name = str(file_name)
    else:
        object_name = replace_filename_with_new(file_name, object_name)

    if use_whole_path == False:
        object_name = os.path.basename(object_name)


    object_name = os.path.join(s3_prefix, object_name).replace("\\", "/")  # Ensure S3 path uses forward slashes

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(f"Successfully uploaded {file_name} to {os.path.join(bucket,object_name)}")
    except ClientError as e:
        logging.error(e)
        return False
    return True

def upload_folder_to_s3(bucket, folder_name, s3_prefix='', use_whole_path=False):
    """Upload a folder and its contents to an S3 bucket

    :param folder_name: Folder to upload
    :param bucket: Bucket to upload to
    :param s3_prefix: Prefix in the S3 bucket under which to store the folder's contents
    :param use_whole_path: If true, uses the whole path of the file to create the object name (mirror folder structure
     in s3 relative to execution directory), if false it will use the last folder in the folder_name path
    """
    # Path of folder until the last folder
    root_folder_name = get_base_directory(folder_name)

    for root, dirs, files in os.walk(folder_name):
        for file in files:
            file_path = os.path.join(root, file)
            if use_whole_path == False:
                relative_path = file_path.replace(root_folder_name, '').lstrip('/')
            else:
                relative_path = file_path.lstrip('/')

            object_name = os.path.join(s3_prefix, relative_path).replace("\\", "/")  # Ensure S3 path uses forward slashes
            try:
                s3_client.upload_file(file_path, bucket, object_name)
            except ClientError as e:
                logging.error(e)
                return False

    output_path = os.path.join(bucket, s3_prefix) if use_whole_path == False else os.path.join(bucket, s3_prefix, folder_name)
    print(f"Successfully uploaded {folder_name} to {output_path}")

def download_file_from_s3(bucket_name, s3_key, local_path=None, use_s3_path=False, file_name=None):
    """
    Download an object from S3 and save it locally.

    :param bucket_name: Name of the S3 bucket.
    :param s3_key: Key of the object in the S3 bucket.
    :param local_path: Local path where the object should be saved (default is current directory).
    :param use_s3_path: If True, creates the file and any folders in the s3 path.
    :param file_name: If set, replace the s3 object name with this new file name
    """
    if local_path is None:
        if use_s3_path:
            local_path = os.path.join(os.getcwd(), s3_key)
        else:
            local_path = os.path.join(os.getcwd(), os.path.basename(s3_key))
    elif use_s3_path:
        local_path = os.path.join(local_path, s3_key)
    else:
        local_path = os.path.join(local_path, os.path.basename(s3_key))

    if file_name is not None:
        local_path = os.path.join(os.path.dirname(local_path), file_name)

    try:
        # Create local directory if it does not exist
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        # Download the file from S3
        s3_client.download_file(bucket_name, s3_key, local_path)
        print(f"Successfully downloaded {s3_key} from bucket {bucket_name} to {local_path}")
    except Exception as e:
        print(f"Error downloading {s3_key} from bucket {bucket_name}: {e}")


def download_folder_from_s3(bucket_name, s3_prefix, local_dir = ''):
    """
    Download all objects from an S3 bucket with the specified prefix and save them locally.

    :param bucket_name: Name of the S3 bucket.
    :param s3_prefix: Prefix of the objects in the S3 bucket.
    :param local_dir: Local directory where the objects should be saved.
    """
    try:
        # List all objects in the bucket with the specified prefix
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=s3_prefix)

        if 'Contents' not in response:
            print(f"No objects found with prefix '{s3_prefix}' in bucket '{bucket_name}'.")
            return

        for obj in response['Contents']:
            s3_key = obj['Key']
            relative_path = os.path.relpath(s3_key, s3_prefix)
            local_file_path = os.path.join(local_dir, relative_path)

            # Create local directory if it does not exist
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

            # Download the file from S3
            s3_client.download_file(bucket_name, s3_key, local_file_path)
            print(f"Successfully downloaded {s3_key} to {local_file_path}")
    except ClientError as e:
        print(f"Error downloading objects from bucket {bucket_name} with prefix {s3_prefix}: {e}")

def initializeEnvirons(profile_name='default'):
    global s, session, s3_client
    # Create a session using the SSO profile
    session = boto3.Session(profile_name=profile_name)

    # Use the session to interact with AWS services
    s3_client = session.client('s3')
