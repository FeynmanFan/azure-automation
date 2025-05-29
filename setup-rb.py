import subprocess
import sys

resource_group = "cbbazureautomationrg"
location = "centralus"
storage_account_name = "cbbdocstorage"
container_name = "doc-container"
automation_account_name = "rbaccount"
subscription_id = "cc06aac4-8c5d-4193-ad34-26129a0aae42"

def run_az_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        sys.exit(1)

# the storage account below will potentially need a new extension installed
run_az_command('az config set extension.dynamic_install_allow_preview=true')

run_az_command(
    f'az storage account create '
    f'--name "{storage_account_name}" '
    f'--resource-group "{resource_group}" '
    f'--location "{location}" '
    f'--sku Standard_LRS '
    f'--kind StorageV2 '
    f'--access-tier Hot'
)
print("Storage account created")

run_az_command(
    f'az storage container create '
    f'--name "{container_name}" '
    f'--account-name "{storage_account_name}" '
    f'--auth-mode login'
)
print("Storage container created")

run_az_command(
    f'az automation account create '
    f'--resource-group "{resource_group}" '
    f'--name "{automation_account_name}" '
    f'--location "{location}"'
)

print("Automation account created")

command = (
    f'az automation account show '
    f'--resource-group "{resource_group}" '
    f'--name "{automation_account_name}" '
    f'--query identity.principalId '
    f'--output tsv'
)

managed_identity_object_id = run_az_command(command).strip()
scope = (
    f'/subscriptions/{subscription_id}/resourceGroups/{resource_group}/'
    f'providers/Microsoft.Storage/storageAccounts/{storage_account_name}'
)
run_az_command(
    f'az role assignment create '
    f'--assignee "{managed_identity_object_id}" '
    f'--role "Storage Blob Data Contributor" '
    f'--scope "{scope}"'
)
print("Automation account granted contributor perms over storage account")
