import json
from datetime import datetime
from botbuilder.core import TurnContext, CardFactory
from botbuilder.schema.teams import (
    MessagingExtensionAction,
    MessagingExtensionActionResponse,
    MessagingExtensionResult,
    TaskModuleTaskInfo,
    TaskModuleContinueResponse,
)
from botbuilder.schema.teams import (
    MessagingExtensionQuery,
    MessagingExtensionResponse,
    MessagingExtensionAttachment,
    MessagingExtensionResult,
)
from botbuilder.schema import HeroCard
from northwindDB.supplier import create_supplier
from northwindDB.model import Supplier
from config import Settings
import urllib.parse

# Load configuration settings
CONFIG = Settings()
COMMAND_ID = "addSupplier"

# Function to handle the fetch task for the messaging extension
async def on_teams_messaging_extension_fetch_task(
    self, context: TurnContext, action: MessagingExtensionAction
) -> MessagingExtensionActionResponse:
    try:
        if action.command_id == COMMAND_ID:
            # Initialize initial parameters
            initial_parameters = {}
            print("Action Data:", action.data)
            print("Task Parameters:", action.data.get("taskParameters"))

            # Check if action has task parameters and assign them to initial_parameters
            if action.data and action.data.get("taskParameters"):
                initial_parameters = action.data["taskParameters"]

            # Construct the URL using the parameters and config
            encoded_parameters = urllib.parse.quote(json.dumps(initial_parameters))
            url = f"{CONFIG.BOT_ENDPOINT}/supplier.html?p={encoded_parameters}&appId={CONFIG.TEAMS_APP_ID}"
            print(f"{str(url)}")

            try:
                # Create TaskModuleTaskInfo with URL and properties
                task_info = TaskModuleTaskInfo(
                    title="Add supplier",
                    width=500,
                    height=500,
                    url=url,
                    fallback_url=url,
                )

                # Return TaskModuleResponse with TaskModuleContinueResponse
                return MessagingExtensionActionResponse(
                    task=TaskModuleContinueResponse(value=task_info)
                )
            except Exception as e:
                # Handle any errors that occur during the task continuation
                print(f"Error during task continuation: {str(e)}")

    except Exception as e:
        # Handle outer errors
        print(f"Error in handle_teams_messaging_extension_fetch_task: {str(e)}")

# Function to handle the submit action for the messaging extension
async def on_teams_messaging_extension_submit_action(
    self, context: TurnContext, action: MessagingExtensionAction
) -> MessagingExtensionActionResponse:

    if action.command_id == "addSupplier":
        # Extract initial parameters from the action data
        initial_parameters = (
            action.data.get("taskParameters", {}) if action.data else action.data
        )
        # Create a new Supplier object with the provided data
        supplier = Supplier(
            etag="",
            partition_key="",
            row_key="",
            timestamp=datetime.now(),
            supplier_id="",
            company_name=action.data["companyName"],
            contact_name=action.data["contactName"],
            contact_title=action.data["contactTitle"],
            address=action.data["address"],
            city=action.data["city"],
            region="",
            postal_code="",
            country="",
            phone="",
            fax="",
            home_page="",
        )
        # Save the new supplier to the database
        await create_supplier(self, supplier)

    # Create the Hero Card object
    hero_card = HeroCard(
        title="Supplier added successfully",
        text=action.data["companyName"],
    )
    
    hero_card_attachment = CardFactory.hero_card(hero_card)

    # Define the attachment with the Hero Card content
    attachment = MessagingExtensionAttachment(
        content_type=hero_card_attachment.content_type,
        content=hero_card_attachment.content,
        preview=hero_card_attachment
    )

    # Return the response with the Hero Card attachment
    return MessagingExtensionResponse(
        compose_extension=MessagingExtensionResult(
            type="result",
            attachment_layout="list",
            attachments=[attachment]
        )
    )

