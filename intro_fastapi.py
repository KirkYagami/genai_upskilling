"""
FastAPI is a modern Python web framework for building APIs with minimal code. It leverages Python type hints for validation and documentation.
"""


# FastAPI is a class we import from the fastapi module
from fastapi import FastAPI

# Create an app instance
# This app variable is the main point of interaction to create all your API endpoints
app = FastAPI()



@app.get('/')
def index():
    return 'Hello Universe!'

# Handling another path
@app.get('/property')
def property():
    return 'This is the property page'


# Returning JSON instead of a simple string
@app.get('/movies')
def movies():
    return {'movie list': ['movie 1', 'movie 2', 'movie 3']}


@app.get('/')
def index():
    return 'Hello Multiverse!'



"""

## Path Parameters

Path parameters allow you to create dynamic routes in your API, making your endpoints more flexible and reusable. They're essential for RESTful API design and are commonly used to identify specific resources.


### Basic Path Parameters

Path parameters are parts of the URL path that are variable and can be captured as function parameters. They're defined by enclosing the parameter name in curly braces `{}` within the path string.

"""

@app.get('/property/{id}')
def get_property(id:int):
    # query = f"""
    # select * from properties
    # where property_id={id}
    # """
    # res = db.execute(query) 
    # return res.fetchone()


    return f'This is the property page for id: {id}'


"""
### Path Parameters with Type Validation

One of the most powerful features of FastAPI is its automatic validation system. By adding type hints to your path parameters, FastAPI will:

1. Validate the input according to the type
2. Convert the parameter to the specified type
3. Generate OpenAPI documentation that includes the type information
4. Provide better editor support with autocomplete
"""

## NOTE: Order matters!!


@app.get('/products/{product_id}')
def get_product_details(product_id: int):
    # In a real application, you would fetch the product from a database
    product = {
        "id": product_id,
        "name": f"Product {product_id}",
        "price": 29.99,
        "in_stock": True
    }
    return product

"""
### Advanced Path Parameters: Using Enums

For cases where you want to restrict path parameters to a specific set of values, you can use Python's `Enum` class:
"""

from enum import Enum

class CategoryName(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    books = "books"
    home = "home"



@app.get('/categories/{category}')
def get_category(category: CategoryName):
    return {"category": category, "items": f"List of {category.value} items"}


"""
## Query Parameters

Query parameters are used to filter, sort, or provide additional information to an API endpoint without being part of the resource identification. They're especially useful for optional parameters or when you need to include many parameters.

"""


"""

## Query Parameters

Query parameters are used to filter, sort, or provide additional information to an API endpoint without being part of the resource identification. They're especially useful for optional parameters or when you need to include many parameters.

"""



@app.get('/products/')
def list_products( max_price:int, min_price: float=0, sort_by:str='price'):
    return {
        "min_price": min_price,
        "max_price": max_price,
        "sort_by": sort_by,
        "products": f"List of products filtered by price between {min_price} and {max_price}, sorted by {sort_by}"
    }



@app.get('/search/')
def search_items(query: str, category: str = None, page: int = 1, items_per_page: int = 10):
    results = f"Search results for '{query}'"
    if category:
        results += f" in category '{category}'"
    
    results += f" (Page {page}, showing {items_per_page} items per page)"
    
    return {"results": results}



## ----------------

# path, query params, type validation

# request body


"""

In API development, a request body is data sent by the client to your API. Request bodies are crucial when clients need to send larger structured data sets to the server.

The key points to understand:

- A response body is what your API sends back to clients
- A request body is what clients send to your API
- APIs always need to send response bodies, but clients don't always need to send request bodies
- POST requests typically include request bodies for creating or submitting data


"""


@app.post('/adduser')
def adduser():
    return {'user': {'name': 'kirkyagami', 'email': 'kirkyagami99@gmail.com'}}

"""
This example defines a POST endpoint that doesn't yet process any incoming data - it simply returns a hardcoded user object. To actually process client data, we need to implement request body handling.
"""

'''
### Using Pydantic Models for Request Bodies

Pydantic is a data validation library that allows us to define custom data types with validation rules. It's the foundation of FastAPI's request body handling.

'''
from pydantic import BaseModel

class Profile(BaseModel):
    name: str
    email: str
    age: int

@app.post('/profile/')
def createprofile(profile: Profile):
    return profile   


'''
When this code runs:

1. FastAPI will see that the function parameter `profile` is a Pydantic model
2. It will read the request body as JSON
3. It will validate the incoming data against the Profile model requirements
4. If valid, it will create a Profile instance and pass it to your function
5. If invalid, it will return a detailed error message to the client

The beauty of this approach is that validation happens automatically - you don't need to write any validation code yourself.
'''


"""
### Combining Request Bodies with Path Parameters

FastAPI can distinguish between different parameter sources in your function:

"""


class Product(BaseModel):
	name: str
	price: int
	discount: int
	discounted_price: int


@app.post('/addproduct/{product_id}')
def addproduct(product: Product, product_id: int):
    product.discounted_price = product.price - (product.price * product.discount / 100)
    return {'product_id': product_id, 'product': product}



'''
### Adding Query Parameters to the Mix

You can also include query parameters alongside path parameters and request bodies:

'''


@app.post('/addproduct/{product_id}')
def addproduct(product: Product, product_id: int, category: str):
    product.discounted_price = product.price - (product.price * product.discount / 100)
    return {'product_id': product_id, 'product': product, 'category': category}





'''
# Nested Models
## Introduction to Nested Models

When modeling complex data structures, we often need to represent relationships between different entities. Pydantic, a data validation library for Python, provides elegant ways to create nested models that reflect these relationships. This approach allows us to build sophisticated data schemas with proper type validation and clear structure.

## Basic List Fields

Let's start with adding a simple collection field to a model. Consider a `Product` model that needs to store multiple tags:

'''

from pydantic import Field
from typing import List

class Product(BaseModel):
    name: str
    price: int = Field(..., gt=10, title="Price of the item", description="Price must be greater than zero")
    discount: int
    discounted_price: int
    tags: list = []



@app.post('/addproduct/v2/{product_id}')
def addproduct_v2(product: Product, product_id: int, category: str):
    product.discounted_price = product.price - (product.price * product.discount / 100)
    return {'product_id': product_id, 'product': product, 'category': category}

class Image(BaseModel):
    url: str
    name: str


class Product(BaseModel):
    name: str
    price: int = Field(..., gt=0, title="Price of the item", description="Price must be greater than zero")
    discount: int
    discounted_price: int
    tags: List[str] = []
    image: Image


class Product(BaseModel):
    name: str
    price: int = Field(..., gt=0, title="Price of the item", description="Price must be greater than zero")
    discount: int
    discounted_price: int
    tags: List[str] = []
    images: List[Image]  # A list of Image models














'''
1.Code to reverse word 
2 . abstraction 
3.inheritance
4.arguments in function
5.exception

1 SELF INTRO
2 INHERITANCE 
3 ABSTRACTION 
4 METHOD OVERLOAD AND METHOD OVERRIDING 
5 ARGUMENTS
6 EXCEPTIONAL HANDLING EXPLAIN WITH CODE
7 REVERSE WORD
8 Decorators(write ur own decorator)
9 List comprehension tuple comprehension set comprehension which will generate generator


1.self intro
2.about my academic project
3.langchain
4.decorators,generators(create a generator function)
5.word counts in a list
6.prompting
7.reverse a number
8.palindrome
9.find missing numbers in a given range of numbers
10.Langchain memories, etc some scenario based questions in genAI



1. Introduction 
2. What is gen ai 
3. Explain how embedding works
4. What is rag how it works 
Python code:
1 sort the list without using build in methods
2 find the letters occurance in string

'''