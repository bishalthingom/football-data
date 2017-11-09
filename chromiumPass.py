import secretstorage

bus = secretstorage.dbus_init()
collection = secretstorage.get_default_collection(bus)
for item in collection.get_all_items():
    if item.get_label() == 'Chrome Safe Storage':
        MY_PASS = item.get_secret()
        break
else:
    raise Exception('Chrome password not found!')

print MY_PASS