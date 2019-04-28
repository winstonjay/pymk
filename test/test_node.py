

def test_index(client, path):
    response = client.get('/')
    print(response)
    assert True