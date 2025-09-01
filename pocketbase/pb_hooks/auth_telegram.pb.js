/// <reference path="../pb_data/types.d.ts" />

onBootstrap((e) => {
  e.next()
  console.log("tg_login_mini_app init!")
})


routerAdd("POST", "/api/auth/telegram", async (c) => {
  console.log("checking_token")
  const body = await c.request.json()
  const initData = body.initData
  
  const envRec = await $app.db().findFirstRecordByData("_env", "key", "BOT_TOKEN")
  if(!envRec) return c.json(500, { error: "BOT_TOKEN not set" })
  const botToken = envRec.get("value")

  console.log("token>", botToken)

  const params = new URLSearchParams(initData)
  const hash = params.get("hash")
  params.delete("hash")

  const sorted = Array.from(params.entries())
    .sort((a,b)=> a[0].localeCompare(b[0]))
    .map(([k,v])=> `${k}=${v}`)
    .join("\n")

  // Correct calculation of the secret key as specified by Telegram
  const secret = $security.hmacSha256("WebAppData", botToken) 
  const expectedHash = $security.hmacSha256(sorted, secret)

  if(expectedHash !== hash) return c.json(400, { error:"invalid hash" })

  const tgId = params.get("id")
  const username = params.get("username")

  let record = await $app.dao().findFirstRecordByData("users","telegram_id",tgId)
  if(!record){
    const coll = await $app.dao().findCollectionByNameOrId("users")
    record = new Record(coll)
    record.set("telegram_id", tgId)
    record.set("username", username)
    await $app.dao().saveRecord(record)
  }

  const token = await $app.dao().newRecordAuthToken(record)
  return c.json(200,{token,record})
})