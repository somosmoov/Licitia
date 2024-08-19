import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

keyVaultName = "KeyVaultAvaliacao"
KVUri = f"https://KeyVaultAvaliacao.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

secretName = "SECRET_NAME"
secretValue = "SECRET_VALUE"

print(f"Creating a secret in KeyVaultAvaliacao called '{secretName}' with the value '{secretValue}' ...")

client.set_secret(secretName, secretValue)

print(" done.")

print(f"Retrieving your secret from KeyVaultAvaliacao.")

retrieved_secret = client.get_secret(secretName)

print(f"Your secret is '{retrieved_secret.value}'.")
print(f"Deleting your secret from KeyVaultAvaliacao ...")

poller = client.begin_delete_secret(secretName)
deleted_secret = poller.result()

print(" done.")
