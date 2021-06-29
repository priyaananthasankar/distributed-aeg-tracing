import json
import logging
import os
from datetime import datetime, timedelta
import azure.functions as func
from azure.storage.blob import BlobServiceClient


def main(event: func.EventGridEvent):
    result = json.dumps({
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
    })

    data = event.get_json()
    target_container_name = os.getenv("TO_BLOB_CONTAINER")
    #from_blob_container = data["url"].split('/')[-2]
    blob_name = data["url"].split('/')[-1]

    # Create Blob Service Client
    conn_str = os.getenv("TO_BLOB_CONN_STRING")
    client = BlobServiceClient.from_connection_string(conn_str) 


    # Get the blob client with the source blob
    source_blob = data["url"]
    copied_blob = client.get_blob_client(target_container_name,blob_name)

    # start copy and check copy status
    copy = copied_blob.start_copy_from_url(source_blob)
    props = copied_blob.get_blob_properties()
    logging.info(str(props.copy.status))

    logging.info('Python EventGrid trigger processed an event: %s', result)
