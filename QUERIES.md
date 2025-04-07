# Sample queries for testing the AppSync SAM application

Go to the "**Queries**" section of your AppSync API in the AWS console to test the queries.

The JSON input for these queries must be formatted using an escape sequence, as demonstrated in the example below.

- findOne:
```
query MyQuery {
  findOne(
    input: "{\"filter\":{\"name\":{\"$regex\":\"Joshua\"}},\"projection\":{\"_id\":0,\"name\":1,\"age\":1,\"likes\":1}}"
  )
}
```

- find:
```
query MyQuery {
 find(
    input: "{   \"filter\": {\"name\": {\"$regex\": \"Joshua\"}},   \"projection\": {\"_id\": 0, \"name\": 1, \"age\": 1, \"likes\": 1} }"
  )
}
```

- aggregate:
```
query MyQuery {
  aggregate(
    input: "{\"pipeline\":[{\"$match\":{\"runtime\":{\"$gte\":50},\"year\":{\"$lte\":2000}}},{\"$project\":{\"title\":1,\"plot\":1,\"fullplot\":1,\"languages\":1,\"cast\":1,\"directors\":1,\"year\":1}},{\"$group\":{\"_id\":\"$year\",\"no_of_movies\":{\"$sum\":1}}},{\"$sort\":{\"no_of_movies\":-1}},{\"$limit\":10}]}"
  )
}
```

- insertOne:
```
mutation MyMutation {
  insertOne(
    input: "{\"document\":{\"name\":\"Diogo Dalot\",\"age\":28,\"likes\":[\"LB\",\"RB\",\"wings\"]}}"
  )
}
```

- insertMany:
```
mutation MyMutation {
  insertMany(
    input: "{\"documents\":[{\"name\":\"Alejandro Garnacho\",\"age\":22,\"likes\":[\"LW\",\"wing\"]},{\"name\":\"Christian Eriksen\",\"age\":32,\"likes\":[\"MD\",\"CDM\"]}]}"
  )
}
```

- updateOne:
```
mutation MyMutation {
  updateOne(
    input: "{\"filter\":{\"_id\":\"67f364e4193e70832a6dedcb\"},\"update\":{\"$set\":{\"name\":\"Eriksen Jr.\"}}}"
  )
}
```

- updateMany:
```
mutation MyMutation {
  updateMany(
    input: "{\"filter\":{\"likes\":\"attack\"},\"update\":{\"$push\":{\"likes\":\"Goal Machine\"}}}"
  )
}
```

- deleteOne:
```
mutation MyMutation {
  deleteOne(input: "{\"filter\":{\"_id\":\"67ebbbc8dba24ffc12ca0022\"}}")
}
```

- deleteMany:
```
mutation MyMutation {
  deleteMany(input: "{\"filter\":{\"name\":\"BrunoFernandes\"}}")
}
```

