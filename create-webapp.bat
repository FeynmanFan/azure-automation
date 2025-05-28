call az provider register --namespace Microsoft.Web
call az appservice plan create --name LinuxWA --resource-group cbbazureautomationrg --location centralus --sku B1 --is-linux
az webapp create --resource-group "cbbazureautomationrg" --plan LinuxWA --name cbb-MyApplication --runtime "DOTNETCORE:9.0"