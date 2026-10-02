from outreach import seller_enquiry, mailto_link, buyer_confirmation

card = {"name": "SAMPLE Weavers Cooperative (demo)"}
subject, body = seller_enquiry(card, "handwoven saree", 500, "Demo Retail Pvt Ltd", "Your Name")
print(subject)
print(body)
print()
print(mailto_link("test@example.com", subject, body)[:100], "...")