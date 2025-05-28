import subprocess
import json

WEB_APP_NAME = "cbb-MyApplication"
KEY_VAULT_NAME = "cbbaakeyvault"
RESOURCE_GROUP = "cbbazureautomationrg"
LOCATION = "centralus"
SUBSCRIPTION_ID = "cc06aac4-8c5d-4193-ad34-26129a0aae42"

def run(command):
    result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE)
    return result.stdout.strip()

identity_output = run(
    f"az webapp identity assign --name {WEB_APP_NAME} --resource-group {RESOURCE_GROUP} --identities [system]"
)
identity_data = json.loads(identity_output)
principal_id = identity_data["principalId"]

run(
    f"az role assignment create --assignee {principal_id} --role \"Key Vault Secrets User\" "
    f"--scope /subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.KeyVault/vaults/{KEY_VAULT_NAME}"
)