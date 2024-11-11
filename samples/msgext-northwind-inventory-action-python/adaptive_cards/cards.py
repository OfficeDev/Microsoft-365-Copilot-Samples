# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import CardFactory
from botbuilder.schema import Attachment


def edit_card(query):
    return {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.5",
        "refresh": {
            "userIds": [],
            "action": {
                "type": "Action.Execute",
                "verb": "refresh",
                "title": "Refresh",
                "data": {"productId": f"{query.get('ProductID')}"},
            },
        },
        "body": [
            {
                "type": "Container",
                "separator": "True",
                "items": [
                    {
                        "type": "ColumnSet",
                        "columns": [
                            {
                                "type": "Column",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "size": "large",
                                        "weight": "bolder",
                                        "text": f"📦 {query.get('ProductName')}",
                                        "wrap": "True",
                                        "style": "heading",
                                    }
                                ],
                                "width": "60",
                            },
                            {
                                "type": "Column",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": f"{query.get('InventoryStatus')}",
                                        "wrap": "True",
                                        "horizontalAlignment": "Right",
                                        "isSubtle": "True",
                                        "color": (
                                            "good"
                                            if query.get("InventoryStatus")
                                            == "In stock"
                                            else (
                                                "warning"
                                                if query.get("InventoryStatus")
                                                == "low stock"
                                                else "attention"
                                            )
                                        ),
                                    }
                                ],
                                "width": "40",
                            },
                        ],
                    }
                ],
                "bleed": "True",
            },
            {
                "type": "Container",
                "style": "emphasis",
                "items": [
                    {
                        "type": "TextBlock",
                        "weight": "Bolder",
                        "text": "**📍Supplier information**",
                        "wrap": "True",
                        "size": "Medium",
                        "isSubtle": "False",
                    },
                    {
                        "type": "ColumnSet",
                        "separator": "True",
                        "columns": [
                            {
                                "type": "Column",
                                "width": "stretch",
                                "items": [
                                    {
                                        "type": "FactSet",
                                        "spacing": "Large",
                                        "facts": [
                                            {
                                                "title": "Name",
                                                "value": f"{query.get('SupplierName')}",
                                            },
                                            {
                                                "title": "City",
                                                "value": f"{query.get('SupplierCity')}",
                                            },
                                        ],
                                        "separator": "True",
                                    }
                                ],
                            }
                        ],
                    },
                    {
                        "type": "TextBlock",
                        "weight": "Bolder",
                        "text": "**🛒 Stock information**",
                        "wrap": "True",
                        "size": "Medium",
                        "isSubtle": "False",
                    },
                    {
                        "type": "ColumnSet",
                        "separator": "True",
                        "columns": [
                            {
                                "type": "Column",
                                "width": "stretch",
                                "items": [
                                    {
                                        "type": "FactSet",
                                        "spacing": "Large",
                                        "facts": [
                                            {
                                                "title": "Category",
                                                "value": f"{query.get('CategoryName')}",
                                            },
                                            {
                                                "title": "Unit price",
                                                "value": f"{query.get('UnitPrice')} USD",
                                            },
                                            {
                                                "title": "Avg discount",
                                                "value": f"{query.get('AverageDiscount')} %",
                                            },
                                            {
                                                "title": "Inventory valuation",
                                                "value": f"{query.get('InventoryValue')} USD",
                                            },
                                        ],
                                        "separator": "True",
                                    }
                                ],
                            },
                            {
                                "type": "Column",
                                "width": "stretch",
                                "items": [
                                    {
                                        "type": "FactSet",
                                        "spacing": "Large",
                                        "facts": [
                                            {
                                                "title": "Units in stock",
                                                "value": f"{query.get('UnitsInStock')}",
                                            },
                                            {
                                                "title": "Units on order",
                                                "value": f"{query.get('UnitsOnOrder')}",
                                            },
                                            {
                                                "title": "Reorder Level",
                                                "value": f"{query.get('ReorderLevel')}",
                                            },
                                            {
                                                "title": "Revenue this period",
                                                "value": f"{query.get('Revenue')} USD",
                                            },
                                        ],
                                        "separator": "True",
                                    }
                                ],
                            },
                        ],
                    },
                ],
            },
            {
                "type": "Container",
                "items": [
                    {
                        "type": "ActionSet",
                        "actions": [
                            {
                                "type": "Action.ShowCard",
                                "title": "Take action",
                                "card": {
                                    "type": "AdaptiveCard",
                                    "body": [
                                        {
                                            "type": "Input.Text",
                                            "id": "txtStock",
                                            "label": "Quantity",
                                            "min": 0,
                                            "max": 9999,
                                            "errorMessage": "Invalid input, use whole positive number",
                                            "style": "Tel",
                                        }
                                    ],
                                    "actions": [
                                        {
                                            "type": "Action.Execute",
                                            "title": "Update stock ✅",
                                            "verb": "ok",
                                            "data": {
                                                "productId": f"{query.get('ProductID')}"
                                            },
                                        },
                                        {
                                            "type": "Action.Execute",
                                            "title": "Restock 📦",
                                            "verb": "restock",
                                            "data": {
                                                "productId": f"{query.get('ProductID')}"
                                            },
                                        },
                                        {
                                            "type": "Action.Execute",
                                            "title": "Cancel restock ❌",
                                            "verb": "cancel",
                                            "data": {
                                                "productId": f"{query.get('ProductID')}"
                                            },
                                        },
                                    ],
                                },
                            },
                            {
                                "type": "Action.Execute",
                                "title": "Edit product",
                                "verb": "edit",
                                "data": {"productId": f"{query.get('ProductID')}"},
                            },
                        ],
                    }
                ],
            },
        ],
    }

def success_card(query, message):
    return {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.5",
        "refresh": {
            "userIds": [],
            "action": {
                "type": "Action.Execute",
                "verb": "refresh",
                "title": "Refresh",
                "data": {"productId": f"{query.get('ProductID')}"},
            },
        },
        "body": [
            {
                "type": "Container",
                "style": "good",
                "separator": "True",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": f"{message}",
                        "weight": "Bolder",
                        "size": "Medium",
                        "color": "Good",
                    }
                ],
            },
            {
                "type": "Container",
                "separator": "True",
                "items": [
                    {
                        "type": "ColumnSet",
                        "columns": [
                            {
                                "type": "Column",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "size": "large",
                                        "weight": "bolder",
                                        "text": f"📦 {query.get('ProductName')}",
                                        "wrap": "True",
                                        "style": "heading",
                                    }
                                ],
                                "width": "60",
                            },
                            {
                                "type": "Column",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": f"{query.get('InventoryStatus')}",
                                        "wrap": "True",
                                        "horizontalAlignment": "Right",
                                        "isSubtle": "True",
                                        "color": (
                                            "good"
                                            if query.get("InventoryStatus")
                                            == "In stock"
                                            else (
                                                "warning"
                                                if query.get("InventoryStatus")
                                                == "low stock"
                                                else "attention"
                                            )
                                        ),
                                    }
                                ],
                                "width": "40",
                            },
                        ],
                    }
                ],
                "bleed": "True",
            },
            {
                "type": "Container",
                "style": "emphasis",
                "items": [
                    {
                        "type": "TextBlock",
                        "weight": "Bolder",
                        "text": "**📍Supplier information**",
                        "wrap": "True",
                        "size": "Medium",
                        "isSubtle": "False",
                    },
                    {
                        "type": "ColumnSet",
                        "separator": "True",
                        "columns": [
                            {
                                "type": "Column",
                                "width": "stretch",
                                "items": [
                                    {
                                        "type": "FactSet",
                                        "spacing": "Large",
                                        "facts": [
                                            {
                                                "title": "Name",
                                                "value": f"{query.get('SupplierName')}",
                                            },
                                            {
                                                "title": "City",
                                                "value": f"{query.get('SupplierCity')}",
                                            },
                                        ],
                                        "separator": "True",
                                    }
                                ],
                            }
                        ],
                    },
                    {
                        "type": "TextBlock",
                        "weight": "Bolder",
                        "text": "**🛒 Stock information**",
                        "wrap": "True",
                        "size": "Medium",
                        "isSubtle": "False",
                    },
                    {
                        "type": "ColumnSet",
                        "separator": "True",
                        "columns": [
                            {
                                "type": "Column",
                                "width": "stretch",
                                "items": [
                                    {
                                        "type": "FactSet",
                                        "spacing": "Large",
                                        "facts": [
                                            {
                                                "title": "Category",
                                                "value": f"{query.get('CategoryName')}",
                                            },
                                            {
                                                "title": "Unit price",
                                                "value": f"{query.get('UnitPrice')} USD",
                                            },
                                            {
                                                "title": "Avg discount",
                                                "value": f"{query.get('AverageDiscount')} %",
                                            },
                                            {
                                                "title": "Inventory valuation",
                                                "value": f"{query.get('InventoryValue')} USD",
                                            },
                                        ],
                                        "separator": "True",
                                    }
                                ],
                            },
                            {
                                "type": "Column",
                                "width": "stretch",
                                "items": [
                                    {
                                        "type": "FactSet",
                                        "spacing": "Large",
                                        "facts": [
                                            {
                                                "title": "Units in stock",
                                                "value": f"{query.get('UnitsInStock')}",
                                            },
                                            {
                                                "title": "Units on order",
                                                "value": f"{query.get('UnitsOnOrder')}",
                                            },
                                            {
                                                "title": "Reorder Level",
                                                "value": f"{query.get('ReorderLevel')}",
                                            },
                                            {
                                                "title": "Revenue this period",
                                                "value": f"{query.get('Revenue')} USD",
                                            },
                                        ],
                                        "separator": "True",
                                    }
                                ],
                            },
                        ],
                    },
                ],
            },
            {
                "type": "Container",
                "items": [
                    {
                        "type": "ActionSet",
                        "actions": [
                            {
                                "type": "Action.ShowCard",
                                "title": "Take action",
                                "card": {
                                    "type": "AdaptiveCard",
                                    "body": [
                                        {
                                            "type": "Input.Text",
                                            "id": "txtStock",
                                            "label": "Quantity",
                                            "min": 0,
                                            "max": 9999,
                                            "errorMessage": "Invalid input, use whole positive number",
                                            "style": "Tel",
                                        }
                                    ],
                                    "actions": [
                                        {
                                            "type": "Action.Execute",
                                            "title": "Update stock ✅",
                                            "verb": "ok",
                                            "data": {
                                                "productId": f"{query.get('ProductID')}"
                                            },
                                        },
                                        {
                                            "type": "Action.Execute",
                                            "title": "Restock 📦",
                                            "verb": "restock",
                                            "data": {
                                                "productId": f"{query.get('ProductID')}"
                                            },
                                        },
                                        {
                                            "type": "Action.Execute",
                                            "title": "Cancel restock ❌",
                                            "verb": "cancel",
                                            "data": {
                                                "productId": f"{query.get('ProductID')}"
                                            },
                                        },
                                    ],
                                },
                            },
                            {
                                "type": "Action.Execute",
                                "title": "Edit product",
                                "verb": "edit",
                                "data": {"productId": f"{query.get('ProductID')}"},
                            },
                        ],
                    }
                ],
            },
        ],
    }

def add_products_cards(
    category_choices: str,
    supplier_choices: str,
    product_Name:str,
) -> Attachment:
    return CardFactory.adaptive_card(
        {
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Enter Product Details",
                    "weight": "bolder",
                    "size": "medium",
                },
                {
                    "type": "Input.Text",
                    "id": "productName",
                    "placeholder": "Product Name",
                    "value": product_Name,
                },
                {
                    "type": "Input.ChoiceSet",
                    "label": "Category",
                    "id": "categoryID",
                    "value": "",
                    "isRequired": True,
                    "errorMessage": "Category is required",
                    "choices": category_choices,
                },
                {
                    "type": "Input.ChoiceSet",
                    "label": "Supplier",
                    "id": "SupplierID",
                    "value": "",
                    "isRequired": True,
                    "errorMessage": "Supplier is required",
                    "choices": supplier_choices,
                },
                {
                    "type": "Input.Number",
                    "id": "unitPrice",
                    "label": "Unit Price",
                    "min": 0,
                    "value": "",
                },
                {
                    "type": "Input.Text",
                    "id": "qtyPerUnit",
                    "label": "Quantity per unit",
                    "value": "",
                },
                {
                    "type": "Input.Number",
                    "id": "unitsInStock",
                    "label": "Units in stock",
                    "min": 0,
                    "value": "",
                },
                {
                    "type": "Input.Number",
                    "id": "unitsOnOrder",
                    "label": "Units on order",
                    "min": 0,
                    "value": "",
                },
                {
                    "type": "Input.Number",
                    "id": "reorderLevel",
                    "label": "Reorder level",
                    "min": 0,
                    "value": "",
                },
                {
                    "type": "Input.Toggle",
                    "valueOn": "true",
                    "valueOff": "false",
                    "id": "discontinued",
                    "title": "Discontinued",
                    "value": "false",
                },
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Submit",
                    "data": {"action": "submit"},
                },
                {
                    "type": "Action.Submit",
                    "title": "Cancel",
                    "data": {"action": "cancel"},
                },
            ],
            "type": "AdaptiveCard",
            "version": "1.0",
        }
    )

def edit_product_card(category_choices, supplier_choices, Product):
    return {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.5",
        "body": [
            {
                "type": "TextBlock",
                "text": "Enter Product Details",
                "weight": "bolder",
                "size": "medium",
            },
            {
                "type": "Input.Text",
                "id": "productName",
                "placeholder": "Product Name",
                "value": Product.get("ProductName", ""),
            },
            {
                "type": "Input.ChoiceSet",
                "label": "Category",
                "id": "category",
                "value":Product.get("CategoryID", ""),
                "isRequired": True,
                "errorMessage": "Category is required",
                "choices": category_choices,  # Directly pass the list of choices
            },
            {
                "type": "Input.ChoiceSet",
                "label": "Supplier",
                "id": "supplier",
                "value":Product.get("SupplierID", ""),
                "isRequired": True,
                "errorMessage": "Supplier is required",
                "choices": supplier_choices,  # Directly pass the list of choices
            },
            {
                "type": "Input.Number",
                "id": "UnitPrice",
                "label": "Unit Price",
                "min": 0,
                "value": Product.get("UnitPrice", 0),
            },
            {
                "type": "Input.Text",
                "id": "qtyPerUnit",
                "label": "Quantity per unit",
                "value": Product.get("QuantityPerUnit", ""),
            },
            {
                "type": "Input.Number",
                "id": "unitsInStock",
                "label": "Units in stock",
                "min": 0,
                "value": Product.get("UnitsInStock", 0),
            },
            {
                "type": "Input.Number",
                "id": "unitsOnOrder",
                "label": "Units on order",
                "min": 0,
                "value": Product.get("UnitsOnOrder", 0),
            },
            {
                "type": "Input.Number",
                "id": "reorderLevel",
                "label": "Reorder level",
                "min": 0,
                "value": Product.get("ReorderLevel", 0),
            },
            {
                "type": "Input.Toggle",
                "valueOn": "true",
                "valueOff": "false",
                "id": "discontinued",
                "title": "Discontinued",
                "value": str(Product.get("Discontinued", "false")).lower(),
            },
        ],
        "actions": [
            {
                "type": "Action.Execute",
                "title": "Submit",
                "verb": "edit-save",
                "data": {"ProductID": Product.get("ProductID", "")},
            }
        ],
    }
