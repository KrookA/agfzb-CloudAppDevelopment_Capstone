/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
const Cloudant = require('@cloudant/cloudant');

async function main(params) {
    const cloudant = new Cloudant({url: params.url, plugins: {iamauth: {iamApiKey: params.apikey}}})
    const db = cloudant.db.use("dealerships")
    return await readAllDocs(params, db);
}

async function readAllDocs(params, db) {
    let all_docs = await db.list({include_docs: true})
    let documents = all_docs.rows.map((e) => {
        return e.doc
    })
    return {"params": params, docs: documents}
}