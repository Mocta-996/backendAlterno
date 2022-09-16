import glob
import os
import boto3
from botocore.client import Config
buckeetName="collectionsemi1"

def list_files(bucket):
    """
    Funcion para listar todo el contenido del bucket
    """
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)
        print("*** ",item)

    return contents


def upload_file(file_name, bucket):
    """
    Función para subir un archivo a un bucket S3 y crear su URL
    """
    response=''
    try:
        object_name = os.path.basename(file_name) 
        s3_client = boto3.client('s3')
        response = s3_client.upload_file(file_name, bucket, object_name)
        if response==None:
            response ='https://{}.s3.amazonaws.com/{}'.format(buckeetName,object_name)
            return response
    except Exception as e:
        print(e)
        return 0

    

def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3')
    output = f"downloads/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)

    return output

#list_files(buckeetName)
# respuesta = upload_file('C:\\Users\\marcs\\Documents\\USAC\\Seminario\\Laboratorio\\Proyecto1\\ServerPython\docs\\img2.jpg',buckeetName)
# print(respuesta)
# list_files(buckeetName)