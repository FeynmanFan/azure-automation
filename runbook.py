from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import datetime
import automationassets

storage_account_name =  automationassets.get_automation_variable("STORAGE_ACCOUNT_NAME")
container_name = automationassets.get_automation_variable("CONTAINER_NAME")

credential = DefaultAzureCredential()
blob_service_client = BlobServiceClient(
    account_url=f"https://{storage_account_name}.blob.core.windows.net",
    credential=credential
)

container_client = blob_service_client.get_container_client(container_name)

current_time = datetime.datetime.now(datetime.timezone.utc)
cutoff = current_time - datetime.timedelta(minutes=6)

blobs = container_client.list_blobs()

for blob in blobs:
    if blob.last_modified < cutoff:
        try:
            blob_client = container_client.get_blob_client(blob.name)
            blob_client.set_standard_blob_tier("Archive")
            print(f"Set blob {blob.name} to Archive tier.")
        except Exception as e:
            print(f"Error setting tier for blob {blob.name}: {str(e)}")
    else:
        print(f"Blob {blob.name} is not older than the cutff, skipping.")