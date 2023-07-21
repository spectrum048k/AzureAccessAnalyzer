from azure.azure_api import AzureAPI

def test_is_valid_guid_true():
    az_api = AzureAPI()
    assert az_api.is_valid_guid("12345678-1234-5678-1234-567812345678") == True


def test_is_valid_guid_false():
    az_api = AzureAPI()
    assert az_api.is_valid_guid("12345678-1234-5678-1234-56781234567") == False


def test_is_valid_guid_none():
    az_api = AzureAPI()
    assert az_api.is_valid_guid(None) == False
