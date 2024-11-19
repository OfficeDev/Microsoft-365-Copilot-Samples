import logging
from botbuilder.core import TurnContext, InvokeResponse, CardFactory
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.schema.teams import (
    MessagingExtensionAction,
    MessagingExtensionActionResponse,
    MessagingExtensionQuery,
    MessagingExtensionResponse,
    MessagingExtensionAttachment,
    MessagingExtensionResult,
)
from message_extensions import (
    product_search_command,
    discounted_search_command,
    revenue_search_command,
    add_product_command,
    add_supplier_command,
)
from adaptive_cards import card_handler, utils, cards


class SearchBot(TeamsActivityHandler):
    def __init__(self):
        super().__init__()

    # Handle messaging extension query
    async def on_teams_messaging_extension_query(
        self, context: TurnContext, query: MessagingExtensionQuery
    ):
        query_data = context.activity.value
        command_id = query_data.get("commandId")
        parameters = query_data.get("parameters", [])
        query_options = query_data.get("queryOptions", {})

        # Construct the MessagingExtensionQuery object
        query = MessagingExtensionQuery(
            command_id=command_id, parameters=parameters, query_options=query_options
        )

        response = await self.handle_teams_messaging_extension_query(context, query)
        return response

    # Handle different commands for messaging extension query
    async def handle_teams_messaging_extension_query(
        self, context: TurnContext, query: MessagingExtensionQuery
    ) -> MessagingExtensionResponse:
        if query.command_id == product_search_command.COMMAND_ID:
            return await product_search_command.handle_teams_messaging_extension_query(
                context, query
            )
        elif query.command_id == discounted_search_command.COMMAND_ID:
            return (
                await discounted_search_command.handle_teams_messaging_extension_query(
                    context, query
                )
            )
        elif query.command_id == revenue_search_command.COMMAND_ID:
            return await revenue_search_command.handle_teams_messaging_extension_query(
                context, query
            )
        else:
            return MessagingExtensionResponse(
                compose_extension={"type": "message", "text": "Unknown command"}
            )

    # Handle adaptive card invoke actions
    async def on_adaptive_card_invoke(
        self, context: TurnContext, value
    ) -> InvokeResponse:
        try:
            verb = context.activity.value["action"]["verb"]
            if verb == "ok":
                return await card_handler.handle_teams_card_action_update_stock(context)
            elif verb == "restock":
                return await card_handler.handle_teams_card_action_restock(context)
            elif verb == "cancel":
                return await card_handler.handle_teams_card_action_cancel_restock(
                    context
                )
            elif verb == "edit":
                return await card_handler.handle_teams_card_action_edit_product(context)
            elif verb == "edit-save":
                return await card_handler.handle_teams_card_action_save_product(context)
            else:
                return utils.create_action_error_response(
                    200,
                    0,
                    f"ActionVerbNotSupported: {verb} is not a supported action verb.",
                )
        except Exception as e:
            print(f"Exception occurred: {e}")
            return utils.create_action_error_response(500, 0, str(e))

    # Handle item selection in messaging extension
    async def on_teams_messaging_extension_select_item(
        self, turn_context: TurnContext, query
    ) -> MessagingExtensionResponse:
        edit_card = cards.edit_card(query)
        attachment = MessagingExtensionAttachment(
            content_type=CardFactory.content_types.adaptive_card, content=edit_card
        )

        return MessagingExtensionResponse(
            compose_extension=MessagingExtensionResult(
                type="result", attachment_layout="list", attachments=[attachment]
            )
        )

    # Handle fetch task action in messaging extension
    async def on_teams_messaging_extension_fetch_task(
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionActionResponse:
        if action.command_id == add_product_command.COMMAND_ID:
            return await add_product_command.on_teams_messaging_extension_fetch_task(
                self, turn_context, action
            )
        elif action.command_id == add_supplier_command.COMMAND_ID:
            return await add_supplier_command.on_teams_messaging_extension_fetch_task(
                self, turn_context, action
            )
        else:
            return None

    # Handle submit action in messaging extension
    async def on_teams_messaging_extension_submit_action(
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionResponse:
        try:
            # commandId
            if action.command_id == add_product_command.COMMAND_ID:
                return await add_product_command.on_teams_messaging_extension_submit_action(
                    self, turn_context, action
                )
            elif action.command_id == add_supplier_command.COMMAND_ID:
                return await add_supplier_command.on_teams_messaging_extension_submit_action(
                    self, turn_context, action
                )
            else:
                return None
        except Exception as e:
            print(e)
            return None
