prompt = """

TASK: Go to the Amazon website and search for a laptop, filter for laptops with more than 4 stars, select the first and put in in the cart.

1. Go to the website https://www.amazon.com using the 'read_url'.
2. Search for 'laptop' using the 'input_text'.
3. Click on the more than 4 stars filter using the 'click_element'.
3. Click on the first product using the 'click_element'.
4. Add the item to the cart clicking on the 'Add to Cart' button using the 'click_element'.


Write 'TERMINATE' to end the conversation.

"""
