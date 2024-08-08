markdown
Copy code
# S3 File Handler

This Python script provides a function to download files from an S3 bucket and save them locally with various configuration options.
Currently uses boto3 to interact with AWS S3 using inherited sso credentials.

## Requirements

- boto3

Install the required package using pip:
```bash
pip install boto3
```

## Usage
    
    ```python
   aws_helper.initializeEnvirons()

    # download file to current directory with the same name
    aws_helper.download_file_from_s3('my-bucket-name', 'prefix/file_path.txt')

    # download file to current directory using s3 pathing to create or add to subfolders
    aws_helper.download_file_from_s3('my-bucket-name', 'prefix/file_path.txt', use_s3_path=True)

    # download file to folder 'downloaded_data' with default name
    aws_helper.download_file_from_s3('my-bucket-name', 'prefix/file_path.txt', 'downloaded_data')

    # download file to current directory using s3 pathing to create or add to subfolders starting at directory 'data'
    aws_helper.download_file_from_s3('my-bucket-name', 'prefix/file_path.txt', 'data', use_s3_path=True)

    # download file to current directory using s3 pathing to create or add to subfolders starting at directory 'data' with new name
    aws_helper.download_file_from_s3('my-bucket-name', 'prefix/file_path.txt', 'data', file_name='test.txt')

    # download folder and contents to current directory
    aws_helper.download_folder_from_s3('my-bucket-name', 'prefix/folder1/folder2/folder3/')

    # download folder and contents to local directory 'downloaded_data'
    aws_helper.download_folder_from_s3('my-bucket-name', 'prefix/folder1/folder2/folder3//', 'downloaded_data')

    # upload folder and contents to s3 with prefix 'uploadTest'
    aws_helper.upload_folder_to_s3('my-bucket-name', 'data/folder_to_upload', 'uploadTest')

    # upload folder and contents to s3 with prefix 'uploadTest' including provide path
    aws_helper.upload_folder_to_s3('my-bucket-name', 'data/folder_to_upload', 'uploadTest', use_whole_path=True)

    # upload folder and contents to s3 with prefix 'uploadTest' entire folder path
    aws_helper.upload_folder_to_s3('my-bucket-name', '/Users/myname/data/folder_to_upload', 'uploadTest2')

    # upload folder and contents to s3 with prefix 'uploadTest' entire folder path
    aws_helper.upload_folder_to_s3('my-bucket-name', '/Users/myname/data/folder_to_upload', 'uploadTest2', use_whole_path=True)



