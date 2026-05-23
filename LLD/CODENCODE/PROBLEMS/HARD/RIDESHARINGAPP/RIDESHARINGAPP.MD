Uber Story Version — Entities Aligned With Real Flow

Imagine this like a real Uber trip happening step by step.

STEP 1 — Rider Opens Uber App
Entity Used: Rider
Rider = Customer who wants to travel
Responsibility
Enters source location
Enters destination
Chooses ride type
Books ride
Story
Ravi opens Uber app to go home.

So:

Ravi = Rider
STEP 2 — Rider Enters Pickup & Destination
Entity Used: Location
Location = Coordinates (latitude, longitude)
Responsibility
Stores source location
Stores destination location
Calculates distance
Story
Pickup  -> Office
Drop    -> Home

Uber internally stores:

Office = Location
Home   = Location

Then calculates:

distance(source, destination)

Because fare depends on distance.

STEP 3 — Uber Shows Ride Types
Entity Used: Product / Vehicle
Product = UberGo / UberX / UberAuto
Responsibility

Each product defines:

Base Fare
Per KM Rate
Vehicle Type
Story

Uber shows Ravi:

UberGo   -> Cheap
UberX    -> Premium
UberAuto -> Auto Rickshaw

Example:

Product	Base Fare	Per KM
UberGo	50	10
UberX	100	20

So product decides pricing behavior.

STEP 4 — Uber Calculates Fare
Entity Used: Fare
Fare = Temporary estimated price
Responsibility
Stores calculated amount
Stores expiry time (TTL)
Prevents outdated booking
Story

Uber says:

UberGo = ₹150
UberX  = ₹300

But this price is temporary.

After 5 seconds or 2 minutes:

Fare expires

because:

traffic changes
surge pricing changes
STEP 5 — Fare Calculation Logic
Strategy Entity Used: PricingStrategy
PricingStrategy = Rule to calculate price
Why Strategy Pattern?

Tomorrow Uber may introduce:

Night pricing
Rain pricing
Festival pricing
Surge pricing

We should add new logic WITHOUT changing old code.

Story Mapping
Morning
NormalPricing

Formula:

baseFare + distance * perKm
Night Time
NightPricing

Formula:

normalFare * 1.5
Rainy Day

Future:

RainPricing

Easy to add because of Strategy Pattern.

STEP 6 — Uber Finds Nearby Drivers
Entity Used: Driver
Driver = Person who accepts ride
Responsibility
Current location
Availability
Rating
Assigned vehicle
Story

Nearby drivers:

Amit
Rahul
John

Each driver has:

- location
- rating
- available/not available
STEP 7 — Driver Matching Logic
Strategy Entity Used: DriverMatchingStrategy
DriverMatchingStrategy = Rule to choose driver
Why Strategy Pattern?

Because company may ask:

Today -> nearest driver
Tomorrow -> highest rated driver
Later -> eco-friendly driver

We should support future algorithms easily.

Story Mapping
Strategy 1 — Nearest Driver
Choose driver closest to rider

Example:

Driver	Distance
Amit	1 km
Rahul	3 km

Result:

Amit selected
Strategy 2 — Highest Rated Driver
Driver	Rating
Amit	4.5
Rahul	4.9

Result:

Rahul selected
STEP 8 — Ride Gets Created
Entity Used: Ride
Ride = Actual confirmed booking
Responsibility

Stores:

Rider
Driver
Product
Source
Destination
Ride Status
Story

Once driver accepts:

Ride Created

Now Uber stores:

Ravi booked UberGo with Amit

That becomes:

Ride Object
STEP 9 — Prevent Double Booking
Important Entity: Driver Mutex Lock
Problem

Two riders:

Ravi
Kiran

try booking SAME driver.

Without locking:

Both get same driver ❌
Solution

Before assigning driver:

lock(driverMutex)

Now only ONE rider gets driver.

STEP 10 — Repositories (Mini Database)

Repositories store data in memory.

DriverRepository
Stores all drivers
Story

Uber checks:

Which drivers are nearby?

It asks:

DriverRepository
FareRepository
Stores temporary fares
Story

When Ravi clicks:

UberGo ₹150

That fare gets saved temporarily.

RideRepository
Stores confirmed rides
Story

After booking:

Ride stored permanently
STEP 11 — Services (Brains of System)

Services contain business logic.

FareEstimationService
Calculates fare
Story

Ravi enters:

Office -> Home

Service calculates:

distance
+ product price
+ pricing strategy

and returns:

₹150
DriverMatchingService
Finds best driver
Story

Uber asks:

Who should pick Ravi?

This service uses:

NearestDriverStrategy
OR
HighestRatedStrategy
RideService
Creates actual ride
Story

Once Ravi clicks:

CONFIRM RIDE

RideService:

validates fare
finds driver
locks driver
creates ride
marks driver unavailable
Full Story Flow (Best Interview Explanation)
1. Rider opens app
2. Rider enters source & destination
3. FareEstimationService calculates fare
4. Product decides base pricing
5. PricingStrategy applies pricing logic
6. Rider selects product
7. RideService starts booking
8. DriverMatchingService finds driver
9. DriverMatchingStrategy selects best driver
10. Driver locked to avoid double booking
11. Ride object created
12. Ride stored in RideRepository
One Easy Memory Trick

Remember this sentence:

Rider chooses Product,
PricingStrategy calculates Fare,
DriverMatchingStrategy finds Driver,
RideService creates Ride safely.