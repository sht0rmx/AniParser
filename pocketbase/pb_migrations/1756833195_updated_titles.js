/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_4132846829")

  // remove field
  collection.fields.removeById("date1629928600")

  // add field
  collection.fields.addAt(19, new Field({
    "hidden": false,
    "id": "number1016612640",
    "max": null,
    "min": null,
    "name": "publishDay",
    "onlyInt": false,
    "presentable": false,
    "required": false,
    "system": false,
    "type": "number"
  }))

  // add field
  collection.fields.addAt(20, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text819208175",
    "max": 0,
    "min": 0,
    "name": "pubDayDesc",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_4132846829")

  // add field
  collection.fields.addAt(17, new Field({
    "hidden": false,
    "id": "date1629928600",
    "max": "",
    "min": "",
    "name": "publishDate",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "date"
  }))

  // remove field
  collection.fields.removeById("number1016612640")

  // remove field
  collection.fields.removeById("text819208175")

  return app.save(collection)
})
