@echo off 
setlocal

SET RESOURCE_GROUP=cbbazureautomationrg
SET VM_NAME=myUbuntuVM
SET LOCATION=centralus
SET ADMIN_USERNAME=cbehrens
SET IMAGE=Ubuntu2404
SET VM_SIZE=Standard_D2s_v3
SET SUBNET_ID=/subscriptions/cc06aac4-8c5d-4193-ad34-26129a0aae42/resourceGroups/cbbazureautomationrg/providers/Microsoft.Network/virtualNetworks/myvnet/subnets/mysubnet

:: ensure resource group
call az group create --name %RESOURCE_GROUP% --location %LOCATION%

:: create vnet
call az network vnet create ^
    --resource-group %RESOURCE_GROUP% ^
    --name myvnet ^
    --address-prefix 10.0.0.0/16 ^
    --subnet-name mysubnet ^
    --subnet-prefix 10.0.1.0/24

:: create VM
call az vm create ^
    --resource-group %RESOURCE_GROUP% ^
    --name %VM_NAME% ^
    --location %LOCATION% ^
    --image %IMAGE% ^
    --size %VM_SIZE% ^
    --admin-username %ADMIN_USERNAME% ^
    --generate-ssh-keys ^
    --subnet %SUBNET_ID% ^
    --nsg ""

endlocal