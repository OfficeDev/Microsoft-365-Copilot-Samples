import logging
from botbuilder.core import TurnContext, CardFactory
from botbuilder.schema import HeroCard, CardImage, CardAction
from botbuilder.schema.teams import (
    MessagingExtensionQuery,
    MessagingExtensionResponse,
    MessagingExtensionAttachment,
    MessagingExtensionResult,
)
from northwindDB.products import get_products_by_revenue_range
from adaptive_cards import cards

COMMAND_ID = "revenueSearch"
query_count = 0


async def handle_teams_messaging_extension_query(
    context: TurnContext, query: MessagingExtensionQuery
) -> MessagingExtensionResponse:
    global query_count
    query_count += 1

    # Seek the parameter by name, don't assume it's in element 0 of the array
    revenue_range = cleanup_param(
        next(
            (
                param.get("value")
                for param in query.parameters
                if param.get("name") == "revenueRange"
            ),
            None,
        )
    )

    logging.info(
        f"💰 Revenue query #{query_count}: Products with revenue in range={revenue_range}"
    )

    products = await get_products_by_revenue_range(revenue_range)

    logging.info(f"Found {len(products)} products in the Northwind database")

    attachments = []
    for product in products:
        hero_card = HeroCard(
            title=product["ProductName"],
            tap=CardAction(type="invoke", value=product),
            text=f'Revenue/period {product["Revenue"]}%<br />Revenue by {product["SupplierName"]} of {product["SupplierCity"]}',
            images=[CardImage(url=product["ImageUrl"])],
        )

        attachment = MessagingExtensionAttachment(
            content_type=CardFactory.content_types.adaptive_card,
            content=cards.edit_card(product),
            preview=CardFactory.hero_card(hero_card),
        )
        attachments.append(attachment)
    return MessagingExtensionResponse(
        compose_extension=MessagingExtensionResult(
            type="result", attachment_layout="list", attachments=attachments
        )
    )


def cleanup_param(value: str) -> str:
    if not value:
        return ""
    result = value.strip()
    result = result.split(",")[0]  # Remove extra data
    result = result.replace("*", "")  # Remove wildcard characters
    return result
