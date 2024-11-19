from botbuilder.core import TurnContext
from northwindDB.products import (
    update_product,
    get_product_ex,
    get_categories,
    get_suppliers,
)
from adaptive_cards.utils import (
    create_action_error_response,
    create_adaptive_card_invoke_response,
    get_inventory_status
)
from adaptive_cards import cards

# Handle the action to update stock
async def handle_teams_card_action_update_stock(context: TurnContext):
    request = context.activity.value
    data = request["action"]["data"]
    print(f"🎬 Handling update stock action")

    if data["txtStock"] and data["productId"]:
        product = await get_product_ex(data["productId"])
        product["UnitsInStock"] = int(data["txtStock"])
        await update_product(product)
        message = f"Stock updated for  to !"
        edit_card = cards.success_card(product, message)
        return create_adaptive_card_invoke_response(200, edit_card)
    else:
        return create_action_error_response(400, 0, "Invalid request")

# Handle the action to cancel restock
async def handle_teams_card_action_cancel_restock(context: TurnContext):
    request = context.activity.value
    data = request["action"]["data"]
    print(f"🎬 Handling cancel restock action")

    if data["productId"]:
        product = await get_product_ex(data["productId"])
        product["UnitsOnOrder"] = 0
        await update_product(product)
        message = f"Restock cancelled for"
        edit_card = cards.success_card(product, message)
        return create_adaptive_card_invoke_response(200, edit_card)
    else:
        return create_action_error_response(400, 0, "Invalid request")

# Handle the action to restock
async def handle_teams_card_action_restock(context: TurnContext):
    request = context.activity.value
    data = request["action"]["data"]
    print(f"🎬 Handling restock action")

    if data["productId"]:
        product = await get_product_ex(data["productId"])
        product["UnitsOnOrder"] = int(product["UnitsOnOrder"]) + int(data["txtStock"])
        await update_product(product)
        message = f"Restocking units."
        edit_card = cards.success_card(product, message)
        return create_adaptive_card_invoke_response(200, edit_card)
    else:
        return create_action_error_response(400, 0, "Invalid request")

# Handle the action to edit product
async def handle_teams_card_action_edit_product(context: TurnContext):
    request = context.activity.value
    data = request["action"]["data"]
    
    print(f"🎬 Handling product edit")

    if "productId" in data:
        product = await get_product_ex(data["productId"])
        categories = await get_categories()
        cat_array = list(categories.values())
        category_choices = [
            {"title": category["CategoryName"], "value": str(category["CategoryID"])}
            for category in cat_array
        ]

        suppliers = await get_suppliers()
        supp_array = list(suppliers.values())
        supplier_choices = [
            {"title": supplier["CompanyName"], "value": str(supplier["SupplierID"])}
            for supplier in supp_array
        ]

        # Create or retrieve the base card template
        template = cards.edit_product_card(category_choices,supplier_choices,product)
        
        return create_adaptive_card_invoke_response(200, template)

    else:
        return create_action_error_response(400, 0, "Invalid request")

# Handle the action to save product
async def handle_teams_card_action_save_product(context: TurnContext):
    request = context.activity.value
    data = request["action"]["data"]
    print(f"🎬 Handling update save product action")

    if data["ProductID"]:
        # Retrieve and update the product details
        product = await get_product_ex(data["ProductID"])
        product["ProductID"] = data["ProductID"]
        product["ProductName"] = data["productName"]
        product["CategoryID"] = data["category"]
        product["SupplierID"] = data["supplier"]
        product["QuantityPerUnit"] = data["qtyPerUnit"]
        product["UnitPrice"] = data["UnitPrice"]
        product["UnitsInStock"] = data["unitsInStock"]
        product["UnitsOnOrder"] = data["unitsOnOrder"]
        product["ReorderLevel"] = data["reorderLevel"]
        product["Discontinued"] = data["discontinued"]

        # Update the product in the database
        await update_product(product)

        # Populate the success card template
        card_data = {
            "productName": product["ProductName"],
            "unitsInStock": product["UnitsInStock"],
            "productId": product["ProductID"],
            "categoryId": product["CategoryID"],
            "imageUrl": product.get("ImageUrl", ""),  # Use get() to handle optional fields
            "supplierName": product.get("SupplierName", ""),
            "supplierCity": product.get("SupplierCity", ""),
            "categoryName": product["CategoryName"],
            "inventoryStatus": get_inventory_status(product),
            "unitPrice": product["UnitPrice"],
            "quantityPerUnit": product["QuantityPerUnit"],
            "unitsOnOrder": product["UnitsOnOrder"],
            "reorderLevel": product["ReorderLevel"],
            "unitSales": product.get("UnitSales", 0),
            "inventoryValue": (float(product.get("UnitsInStock", "0")) * float(product.get("UnitPrice", "0"))),
            "revenue": product.get("Revenue", 0),
            "averageDiscount": product.get("AverageDiscount", 0),
            "message": f"Product updated for {product['ProductName']}!",
        }
        
        template = cards.success_card(product,card_data["message"])
        
        # Return the adaptive card response
        return create_adaptive_card_invoke_response(200, template)

    else:
        # Handle the error case with an appropriate response
        return create_action_error_response(400, 0, "Invalid request")