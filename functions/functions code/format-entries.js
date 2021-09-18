/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
function main(params) {
    if (false) {
        return params.params;
    }

    if (params.params["dealerId"]) {
        //dealer id spefified
        let out = []
        params.docs.forEach(function(e) {
            if (e.id == params.params["dealerId"]) { //include state
                out.push({
                    id: e.id,
                    city: e.city,
                    state: e.state,
                    st: e.st,
                    address: e.address,
                    zip: e.zip,
                    lat: e.lat,
                    long: e.long,
                    short_name: e.short_name,
                    full_name: e.full_name
                })
                return;
            }
        })
        return {entries: out};
    }
    else if (params.params["state"]) {
        //state specified
        let out = [];
        params.docs.forEach(function(e) {
            if (e.st === params.params["state"].toUpperCase()) { //include state
                out.push({
                    id: e.id,
                    city: e.city,
                    state: e.state,
                    st: e.st,
                    address: e.address,
                    zip: e.zip,
                    lat: e.lat,
                    long: e.long,
                    short_name: e.short_name,
                    full_name: e.full_name
                })
            }
        })
        return {entries: out};
    }
    else {
        //no state specified
        return {
            entries: params.docs.map((row) => {
                return {
                    id: row.id,
                    city: row.city,
                    state: row.state,
                    st: row.st,
                    address: row.address,
                    zip: row.zip,
                    lat: row.lat,
                    long: row.long,
                    short_name: row.short_name,
                    full_name: row.full_name
                }
            })
        }
    }
}
