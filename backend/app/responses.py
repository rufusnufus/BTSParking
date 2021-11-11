from fastapi import status

create_car_responses = {
    status.HTTP_200_OK: {
        "description": "Car created successfully",
        "content": {
            "application/json": {
                "examples": {
                    "touareg": {
                        "summary": "Volkswagen Touareg",
                        "value": {"id": 1, "model": "Volkswagen Touareg", "license_number": "A000AA"}
                    },
                }
            }
        }
    },
}

get_cars_responses = {
    status.HTTP_200_OK: {
        "description": "Listing of all added cars of a user",
        "content": {
            "application/json": {
                "examples": {
                    "cars": {
                        "summary": "cars",
                        "value": [{"id": 1, "model": "Volkswagen Touareg", "license_number": "A000AA"}]
                    },
                }
            }
        }
    },
}

delete_car_responses = {
    status.HTTP_204_NO_CONTENT: {
        "description": "Car deleted successfully",
    },
    status.HTTP_403_FORBIDDEN: {
        "description": "This car isn't owned by this user",
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "This car doesn't exist",
    },
}
