from abc import ABC, abstractmethod
from functools import wraps


class AppConfig: #Creation of single instance for singleton design principle
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.app_name = "CabsForYou"
            cls._instance.currency = "₹"
        return cls._instance


# Using separate classes and abstract methods to apply Single responsiblity principle

#Logic for calculating fare based on type of trip.
class pricingStrategy(ABC):
    @abstractmethod
    def calculate_fare(self, distance: float):
        pass


class normalPricing(pricingStrategy):
    def calculate_fare(self, distance: float):
        return distance * 10


class surgePricing(pricingStrategy):
    def calculate_fare(self, distance: float):
        return distance * 25


#Logic for presenting method of payment
class paymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass


class upiPayment(paymentStrategy):
    def pay(self, amount: float):
        print(f"Paid ₹{amount} via UPI")


class cardPayment(paymentStrategy):
    def pay(self, amount: float):
        print(f"Paid ₹{amount} via Card")


class walletPayment(paymentStrategy):
    def pay(self, amount: float):
        print(f"Paid ₹{amount} via Wallet")




#Object selection using Factory Design
class pricingFactory:
    _pricing_map = {
        "NORMAL": normalPricing,
        "SURGE": surgePricing
    }

    @classmethod
    def get_pricing(cls, pricing_type: str):
        try:
            return cls._pricing_map[pricing_type.upper()]()
        except KeyError:
            raise ValueError("Invalid pricing type")


class rideBookingService:
    def __init__(self, pricing: pricingStrategy, payment: paymentStrategy):
        self.pricing = pricing
        self.payment = payment

    def book_ride(self, distance: float):
        fare = self.pricing.calculate_fare(distance)
        self.payment.pay(fare)


#Decorators to wrap ridebookingservice with logging and authentication
def loggingDecorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("[LOG] Ride booking started")
        result = func(*args, **kwargs)
        print("[LOG] Ride booking completed")
        return result
    return wrapper



def authenticationDecorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("[AUTH] User authenticated")
        return func(*args, **kwargs)
    return wrapper




rideBookingService.book_ride = authenticationDecorator(
    loggingDecorator(rideBookingService.book_ride)
)




if __name__ == "__main__":
    config = AppConfig()
    print(f"{config.app_name} App Started ({config.currency})")

    pricing = pricingFactory.get_pricing("SURGE")  
    payment = cardPayment()                      

    booking_service = rideBookingService(pricing, payment)
    booking_service.book_ride(10)
