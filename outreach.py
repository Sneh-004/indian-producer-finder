from urllib.parse import quote


def seller_enquiry(card, product, quantity, buyer_company, buyer_name):
    subject = f"Enquiry: {product} supply - {buyer_company}"
    body = f"""Dear {card['name']} team,

I am {buyer_name} from {buyer_company}. We are looking to source {product} (approx. {quantity} units) and found your organisation through our supplier search.

Could you please share:
1. Registration details (cooperative / SHG / society number) and any GI certification
2. Product range and sample photos
3. Price per unit and minimum order quantity
4. Production capacity and delivery time

Thank you for your time. We look forward to hearing from you.

Regards,
{buyer_name}
{buyer_company}"""
    return subject, body


def mailto_link(to_email, subject, body):
    return f"mailto:{to_email}?subject={quote(subject)}&body={quote(body)}"


def buyer_confirmation(card, product, quantity, price, delivery):
    subject = f"Order summary: {product} from {card['name']}"
    body = f"""Hello,

Here is the summary of the order for your approval:

Supplier: {card['name']}
Product: {product}
Quantity: {quantity}
Price per unit: {price}
Delivery time: {delivery}

Please reply CONFIRM to proceed.

Regards,
Procurement assistant"""
    return subject, body