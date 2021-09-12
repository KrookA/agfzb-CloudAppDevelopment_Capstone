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
	let review = params.review;
	if (!(review.id && review.name && review.dealership && review.review && review.purchase && review.purchase_date && review.car_make && review.car_model && review.car_year)) {
	    //not all fields provided
	    return Promise.reject({error: "Not all required fields submitted to POST"});
	}
	
	return {
	    doc: {
	        id: review.id,
	        name: review.name,
	        dealership: review.dealership,
	        review: review.review,
	        purchase: review.purchase,
	        purchase_date: review.purchase_date,
	        car_make: review.car_make,
	        car_model: review.car_model,
	        car_year: review.car_year
	    }
	}
}
