/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_4132846829")

  // add field
  collection.fields.addAt(21, new Field({
    "hidden": false,
    "id": "number848901969",
    "max": null,
    "min": null,
    "name": "score",
    "onlyInt": false,
    "presentable": false,
    "required": false,
    "system": false,
    "type": "number"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_4132846829")

  // remove field
  collection.fields.removeById("number848901969")

  return app.save(collection)
})
