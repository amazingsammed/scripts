$jsonStr = '{
    "items": [
        {"id": 1, "name": "item 1"},
        {"id": 2, "name": "item 2"},
        {"id": 3, "name": "item 3"},
        {"id": 4, "name": "item 4"},
        {"id": 5, "name": "item 5"}
    ]
}';

$startIndex = 2; // Start from index 2 (item with id 3)

$data = json_decode($jsonStr, true);
$items = array_slice($data['items'], $startIndex);

$newData = ['items' => $items];
$newJsonStr = json_encode($newData);

echo $newJsonStr;
