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
        //dealership specified
        let out = [];
        params.docs.forEach(function(e) {
            if (e.dealership == params.params["dealerId"]) { //review is for requested dealership
                out.push({
                    id: e.id,
                    name: e.name,
                    dealership: e.dealership,
                    review: e.review,
                    purchase: e.purchase,
                    purchase_date: e.purchase_date,
                    car_make: e.car_make,
                    car_model: e.car_model,
                    car_year: e.car_year
                })
            }
        })
        return {entries: out};
    }
    else {
        //no dealership specified
        return {"error": {"status": 404, body: "No dealerId param supplied"}};
    }
}