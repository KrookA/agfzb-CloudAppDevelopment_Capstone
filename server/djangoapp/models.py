from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    MODELS = (
        ("FIREBIRD", "Firebird"),
        ("A6", "A6"),
        ("MX-5", "MX-5"),
        ("SEDAN", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "WAGON")
    )

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealerId = models.IntegerField()
    name = models.CharField(max_length=20)
    model_type = models.CharField(choices=MODELS, max_length=20)
    year = models.DateField()

    def __str__(self):
        return self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, obj):
        self.address = obj["address"]
        self.city = obj["city"]
        self.full_name = obj["full_name"]
        self.id = obj["id"]
        self.lat = obj["lat"]
        self.long = obj["long"]
        self.short_name = obj["short_name"]
        self.st = obj["st"]
        self.state = obj["state"]
        self.zip = obj["zip"]

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, obj):
        self.id = obj["id"]
        self.dealership = obj["dealership"]
        self.name = obj["name"]
        self.purchase = obj["purchase"]
        self.review = obj["review"]
        if "purchase_date" in obj:
            self.purchase_date = obj["purchase_date"]
        if "car_make" in obj:
            self.car_make = obj["car_make"]
        if "car_model" in obj:
            self.car_model = obj["car_model"]
        if "car_year" in obj:
            self.car_year = obj["car_year"]
        if "sentiment" in obj:
            self.sentiment = obj["sentiment"]
    
    def __str__(self):
        return "Review: " + self.review