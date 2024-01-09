from dataclasses import dataclass, field

@dataclass
class Customer:
    id: str
    created_at: str
    updated_at: str
    given_name: str
    family_name: str
    email_address: str
    creation_source: str
    version: int
    preferences: dict = field(default_factory=dict)  # Allow for optional preferences

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'given_name': self.given_name,
            'family_name': self.family_name,
            'email_address': self.email_address,
            'preferences': self.preferences,
            'creation_source': self.creation_source,
            'version': self.version
        }
    
    def __eq__(self, __value: object) -> bool:
        return self.email_address == __value
    
    def __lt__(self, __value: object) -> bool:
        return self.email_address < __value
    
    def __gt__(self, __value: object) -> bool:
        return self.email_address > __value

def from_json(data: dict) -> Customer:
    return Customer(
        id = data['id'],
        created_at = data['created_at'],
        updated_at = data['updated_at'],
        given_name = data['given_name'],
        family_name = data['family_name'],
        email_address = data['email_address'],
        preferences = data['preferences'],
        creation_source = data['creation_source'],
        version = data['version']
    )

@dataclass
class ListCustomer:
    customers: list[Customer]

    def to_json(self) -> dict:
        return {
            'customers': list(map(lambda x : x.to_json(), self.customers))
        }
    
    # Function to find the partition position
    def partition(array, low, high):
    
        # Choose the rightmost element as pivot
        pivot = array[high]
    
        # Pointer for greater element
        i = low - 1
    
        # Traverse through all elements
        # compare each element with pivot
        for j in range(low, high):
            if array[j] <= pivot:
    
                # If element smaller than pivot is found
                # swap it with the greater element pointed by i
                i = i + 1
    
                # Swapping element at i with element at j
                (array[i], array[j]) = (array[j], array[i])
    
        # Swap the pivot element with
        # the greater element specified by i
        (array[i + 1], array[high]) = (array[high], array[i + 1])
    
        # Return the position from where partition is done
        return i + 1
    
    def sort_customers(self, low, high) -> list[Customer]:
        """
        Sorts customers using the quicksort algorithm based on the email field.
        Args:
            low (int): The starting index of the array to be sorted.
            high (int): The ending index of the array to be sorted.
        Returns:
            list[Customer]: The sorted list of customers.
        """
        if low < high:
 
            # Find pivot element such that
            # element smaller than pivot are on the left
            # element greater than pivot are on the right
            pi = self.partition(self.customers, low, high)
 
            # Recursively sort elements before
            # partition and after partition
            self.sort_customers(low, pi - 1)
            self.sort_customers(pi + 1, high)


    
    def search_customer(self, email: str) -> Customer:
        """
        Searches for a customer in the list of customers using binary search algorithm.
    
        Args:
            email (str): The email address of the customer to search for.
            
        Returns:
            Customer: The customer object if found, or None if not found.
        """
        # Sort the list of customers
        self.sort_customers(0, len(self.customers) - 1)

        l = 0
        r = len(self.customers) - 1

        while l <= r:
    
            mid = l + (r - l) // 2
    
            # Check if x is present at mid
            if self.customers[mid] == email:
                return self.customers[mid]
    
            # If x is greater, ignore left half
            elif self.customers[mid] < email:
                l = mid + 1
    
            # If x is smaller, ignore right half
            else:
                r = mid - 1
    
        # If we reach here, then the element
        # was not present
        return False

def from_json_list(data: dict) -> ListCustomer:
    return ListCustomer(
        customers = list(map(lambda x : from_json(x), data['customers']))
    )