from botbuilder.core import TurnContext, CardFactory
from botbuilder.schema.teams import (
    MessagingExtensionAction,
    MessagingExtensionActionResponse,
    MessagingExtensionResult,
    TaskModuleTaskInfo,
    TaskModuleContinueResponse,
    MessagingExtensionAttachment,
    MessagingExtensionResponse,
)
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.schema import Attachment, HeroCard
from adaptive_cards import cards
from northwindDB.products import create_product
from northwindDB.products import get_categories, get_suppliers, Product

COMMAND_ID = "addProduct"

async def on_teams_messaging_extension_fetch_task(
    self, context: TurnContext,
    action: MessagingExtensionAction,
) -> MessagingExtensionActionResponse:
    try:
        if action.command_id == COMMAND_ID:
            
            # Initialize initial parameters
            initial_parameters = {}
           
            # Check if action has task parameters and assign them to initial_parameters
            if action.data and action.data.get("taskParameters"):
                initial_parameters = action.data["taskParameters"]
            
            # Get categories  
            categories = await get_categories()
            
            # Assuming categories is a dictionary
            cat_array = list(categories.values())
            category_choices = [
                {
                    "title": category["CategoryName"],
                    "value": str(category["CategoryID"]),
                }
                for category in cat_array
            ]

            # Get suppliers    
            suppliers = await get_suppliers()
            
            # Assuming supplier is a dictionary
            sup_array = list(suppliers.values())

            supplier_choices = [
                {"title": supplier["CompanyName"], "value": str(supplier["SupplierID"])}
                for supplier in sup_array
            ]

            card = cards.add_products_cards(category_choices, supplier_choices,initial_parameters.get("name", ""))
            
            task_info = TaskModuleTaskInfo(
                card=card, height=500, title="Add a product", width=500
            )

            continue_response = TaskModuleContinueResponse(value=task_info)
            return MessagingExtensionActionResponse(task=continue_response)

    except Exception as e:
        # Handle outer errors
        print(f"Error in on_teams_messaging_extension_fetch_task: {str(e)}")


async def on_teams_messaging_extension_submit_action(
    self, turn_context: TurnContext, action: MessagingExtensionAction
) -> MessagingExtensionActionResponse:
    try:
        if action.data:
            data = action.data

            # For Copilot action
            initial_parameters = action.data.get("taskParameters", {}) or action.data

            # Handle action cases
        if data.get("action") == "submit":
            # Define product dictionary based on initial parameters
            product = Product(
                etag="",
                partition_key="",
                row_key="",
                timestamp="",
                product_id="",
                product_name=initial_parameters.get("productName", ""),
                supplier_id=initial_parameters.get("SupplierID", ""),
                category_id=initial_parameters.get("categoryID", ""),
                quantity_per_unit=initial_parameters.get("qtyPerUnit", "0"),
                unit_price=initial_parameters.get("unitPrice", "0"),
                units_in_stock=initial_parameters.get("unitsInStock", "0"),
                units_on_order=initial_parameters.get("unitsOnOrder", "0"),
                reorder_level=initial_parameters.get("reorderLevel", "0"),
                discontinued=initial_parameters.get("discontinued", False),
                image_url="https://picsum.photos/seed/1/200/300",
            )

            # Create the product
            await create_product(self, product)

            # Create hero card for response
            hero_card = HeroCard(
                title="Product added successfully",
                text=initial_parameters.get("productName", ""),
            )

            hero_card_attachment = CardFactory.hero_card(hero_card)

            # Define the attachment with the Hero Card content
            attachment = MessagingExtensionAttachment(
                content_type=hero_card_attachment.content_type,
                content=hero_card_attachment.content,
                preview=hero_card_attachment,
            )

            # Return MessagingExtensionActionResponse
            return MessagingExtensionResponse(
                compose_extension=MessagingExtensionResult(
                    type="result",
                    attachment_layout="list",
                    attachments=[attachment],
                )
            )

        elif data.get("action") == "cancel":
            # Handle cancel action if needed
            print(f"cancelled")

    except Exception as e:
        print(f"Error: {e}")
