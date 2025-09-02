/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_2569223347")

  // update collection data
  unmarshal({
    "name": "env"
  }, collection)

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_2569223347")

  // update collection data
  unmarshal({
    "name": "_env"
  }, collection)

  return app.save(collection)
})
