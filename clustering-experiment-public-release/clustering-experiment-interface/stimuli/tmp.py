import json

with open('stimuli_info.json') as f:
    info = json.load(f)

lookup = {}

for item in info.values():
    lookup[item['base_uuid']] = item['unique_uuid']

for idx, item in enumerate(['fccbc907-4526-43e2-8ded-142b804b471a',
                            'e0b28b0d-8194-475b-98a6-6931d1ff1004',
                            'b3697dbc-04ee-4762-a98d-5773cf0c7e84',
                            '37ecaaa0-dbb1-4b98-ad55-ce73229d5866',
                            '6b397277-e2cf-4165-9f1a-32aeef65ebbc',
                            'be66f0f4-0431-458a-8aa4-16bc76354c9f',
                            '339f68e4-98bf-4d4a-81c7-06fa958f307e',
                            '3c4d6c38-877b-41d2-b2b5-d2f74ef0970b',
                            '2f452eee-c0bb-437c-bd4e-f35ee9fe9ff6',
                            '8ced8977-7d84-444f-9648-a0c4b65e45ce',
                            '9960e442-6168-430d-b694-abfb5f4339fa',
                            'e9bc8099-ff66-4017-abd4-33cd8dbcc2d6',
                            '4fbeab87-3c1b-44f6-91c7-47cb4e50c315',
                            '839dbbc1-445d-4298-95c3-38299943cfb6',
                            '2bb1495b-1ef6-4943-bb48-662371f50b30',
                            'f54baffc-bc26-4c4d-b940-824d08daf230',
                            '79a56e1c-89e6-41ff-a3c6-0f4126d8f6a3',
                            '6da3f9dc-e910-4c46-822b-eebee4448324',
                            '51196345-76b0-41da-9c00-5ecb1a87b408',
                            'c91f4a09-8df1-4eb3-859a-8dc243343b26',
                            'fa83ff0a-5066-4c01-bdf6-909bc3dda074',
                            'fdb55140-d76a-43e5-b66a-8883dc677b94',
                            'd62793d4-4219-4f10-b2aa-86d40192d723',
                            '0f18f0ad-f23d-4fc9-a761-3920c107550b',
                            '56c594b9-620f-49b9-8302-684c969061da',
                            '3808a1ab-27ce-451f-bbd1-525f0e658c07',
                            '98dd5bec-729c-46ed-9714-b1e26e817196',
                            'e8770f4c-e648-4512-9529-b68de18f7703']):
    print(f"{idx + 1}: {item} -> {lookup[item]}")
