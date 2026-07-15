from langchain_core.tools import tool

# This dictionary works like a temporary order database
MOCK_ORDERS = {
    "ORD-1001": "Shipped",
    "ORD-1002": "Processing",
    "ORD-1003": "Delivered",
    "ORD-1004": "Cancelled",
    "ORD-1005": "Out for Delivery",
}


@tool
def get_order_status(order_id: str) -> str:
    """Looks up the current status of a customer's order using the order ID."""
    status = MOCK_ORDERS.get(order_id)
    if status is None:
        return f"Sorry, I could not find any order with the ID {order_id}."
    return f"Order {order_id} is currently: {status}"


@tool
def calculate_discount(price: float, discount_percent: float) -> str:
    """Calculates the final price after applying a discount percentage to the original price."""
    if price < 0:
        return "Price cannot be negative. Please provide a valid price."
    if discount_percent < 0 or discount_percent > 100:
        return "Discount percent must be between 0 and 100."

    final_price = price * (1 - discount_percent / 100)
    return f"The final price after {discount_percent}% discount is ₹{final_price:.2f}"


@tool
def calculate_delivery_charge(order_value: float, customer_type: str) -> str:
    """Calculates the delivery charge based on the order value and whether the customer is Premium or Standard."""
    if customer_type not in ("Premium", "Standard"):
        return "Unsupported customer type. Please use 'Premium' or 'Standard'."

    if customer_type == "Premium":
        charge = 0
    elif order_value >= 2000:
        charge = 0
    else:
        charge = 100

    return f"The delivery charge for this order is ₹{charge}"


@tool
def get_estimated_delivery_days(shipping_type: str) -> str:
    """Gives the estimated delivery time based on the shipping type: Standard, Express, or Same Day."""
    delivery_times = {
        "Standard": "3-5 business days",
        "Express": "1-2 business days",
        "Same Day": "Same day",
    }

    if shipping_type not in delivery_times:
        return "Unsupported shipping type. Please choose Standard, Express, or Same Day."

    return f"Estimated delivery time for {shipping_type} shipping: {delivery_times[shipping_type]}"

