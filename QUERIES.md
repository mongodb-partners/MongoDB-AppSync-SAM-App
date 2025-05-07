# Sample queries for testing the AppSync SAM application

Go to the "**Queries**" section of your AppSync API in the AWS console to test the queries.

You can find a sample of 20 documents [here](/sample_documents.json) that you can insert in your DB and perform the below operations for a POC/POV of this solution.

The JSON input for these queries must be formatted using an escape sequence, as demonstrated in the example below.

- findOne:
```
query MyQuery {
  findOne(
    input: "{\"database\":\"inventory\",\"collection\":\"products\",\"filter\":{\"name\":\"Television Set\"},\"projection\":{\"name\":1,\"price\":1,\"available_qty\":1}}"
  )
}
```

- find:
```
query MyQuery {
  find(
    input: "{\"database\":\"inventory\",\"collection\":\"products\",\"filter\":{\"category\":\"electronics\"},\"projection\":{\"name\":1,\"price\":1,\"available_qty\":1}}"
  )
}
```

- aggregate:
```
query MyQuery {
  aggregate(
    input: "{\"database\":\"inventory\",\"collection\":\"products\",\"pipeline\":[{\"$group\":{\"_id\":\"$category\",\"total_price\":{\"$sum\":\"$price\"},\"total_qty\":{\"$sum\":\"$available_qty\"}}}]}"
  )
}
```

- insertOne:
```
mutation MyMutation {
  insertOne(
    input: "{\"database\":\"inventory\",\"collection\":\"products\",\"document\":{\"name\":\"Home Theatre\",\"price\":1000,\"available_qty\":20,\"category\":\"electronics\"}}"
  )
}
```

- insertMany:
```
mutation MyMutation {
  insertMany(
    input: "{\"database\":\"inventory\",\"collection\":\"products\",\"documents\":[{\"name\":\"Study Table\",\"price\":800,\"available_qty\":50,\"category\":\"home\"},{\"name\":\"Laptop\",\"price\":1200,\"available_qty\":30,\"category\":\"electronics\"}]}"
  )
}
```

- updateOne:
```
mutation MyMutation {
  updateOne(
    input: "{\"database\":\"inventory\",\"collection\":\"products\",\"filter\":{\"name\":\"Television Set\"},\"update\":{\"$set\":{\"price\":450,\"available_qty\":45}}}"
  )
}
```

- updateMany:
```
mutation MyMutation {
  updateMany(
    input: "{\"database\":\"inventory\",\"collection\":\"products\",\"filter\":{\"category\":\"electronics\"},\"update\":{\"$inc\":{\"available_qty\":30}}}"
  )
}
```

- deleteOne:
```
mutation MyMutation {
  deleteOne(
    input: "{\"database\":\"inventory\",\"collection\":\"products\",\"filter\":{\"name\":\"Television Set\"}}"
  )
}
```

- deleteMany:
```
mutation MyMutation {
  deleteMany(
    input: "{\"database\":\"inventory\",\"collection\":\"products\",\"filter\":{\"category\":\"home\"}}"
  )
}
```

