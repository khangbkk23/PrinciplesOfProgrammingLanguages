# Base function 
def requires_admin(func):
    def wrapper(user_role, *args, **kwargs):
        if user_role != "admin":
            return "Access denied"
        return func(user_role, *args, **kwargs)
    return wrapper
# Abstract from base function
@requires_admin
def delete_user(user_role, user_id):
    return f"User {user_id} deleted"

print(delete_user("guest", 42))
print(delete_user("admin", 42))

def add_sprinkle(func):
    def wrapper(*args, **kwargs):
        print("*You added sprinkle!*")
        func(*args, **kwargs)
    return wrapper

def add_shit(func):
    def wrapper(*args, **kwargs):
        print("*You added a lot of shit on the top of ice creammm*")
        func(*args, **kwargs)
    return wrapper

@add_sprinkle
@add_shit
def get_ice_cream(flavour):
    print(f"Here is your {flavour} ice-cream")
    
get_ice_cream(flavour='strawberry')
