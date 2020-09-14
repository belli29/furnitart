# Furnitart

Furnitart is the website of a furniture shop based in Ireland that wants to start selling on the e-market.
The e-store allows shipping all around Europe at different shipping rates. 

 
## UX
 
This website is designed for 2 different users : the customer and the seller.
### Customer
The customer is able to view all different products and order them with using various filters.
He/she can buy prodcuts and finanlly pay for them via Stripe. In this case he/she will recieve an instant notification that the order is being processed.
The seller will send a notification when the order is shipped.

The customer can also decide to request a Paypay invoice that generates an invoice, payable in the following 3 days. Once paid he/she is supposed to contact the seller to upgrade the preorder into an order( then previous flow applies).
This option is suggested to the customer as it does not lead to any processing fee for the seller.

The customer can also register. From the profile page he/she will be able to keep track of all his/ orders on the secion My profile 

- user story1:

User is looking for a new table but has very reduced space in his studio. User searches for table and order results for size (smaller to bigger).

Finally he finds a product that he likes. He verifies the size and decides to purchase it. Intially he would like to pay by Stripe but notices that payment by PayPal invoice has a nice discount.

He makes the preorder, makes a payment on Paypal and emails the payment number to the seller.

After few days he receives an email, confirming payment has been confirmed. After few more days he recieves an email confirming the shipment with a shipping tracking code.


### Seller

After logging in the seller will be able to control orders preorders and the inventory.

The seller will be able to handle the processing of the orders and send info to the customers about the orders.

The seller will also be able to add / delete / modify products and will always have control over the number of items available

- seller story 1:

The seller has 2 units of a product that, due to its size, can only be delivered to Ireland. 
The seller receives a preorder for 1 unit to be shipped to Ireland. The available quantity is now only 1 on the website.
After 3 days, he has not recieved any information about the payment from the customer . He, then, decides to delete the prepayment in order to increase the product availability.

-seller story 2:

The seller has 2 units of a product that, due to its size, can only be delivered to Ireland 
The seller receives a preorder for 1 unit to be shipped to Ireland. The available quantity is now only 1 on the website.
After 2 days, he receives an email from the guest with the payment invoice. The seller confirms through the app that payment has been received.
After 1 day he has shipped the item and can confirm the shipment with a shipping code.

## Features
### Existing Features
- Management : allows sellers to keep track and modify inventory, orders and preorders. Amending orders / preorders allows seller to send automatic emails to customers and keep them updated of order/preorder/shipment status 
- Profile : allows users to anebd delivery information and keep track of orders and preorders
- Products :allows user to see the products, filter and  order them 
- Checkout :allows user get a paypal invoice or to pay directly (Stripe). The Stripe payment is done using the support of a webhooker. This ensures that orderes are always correctly registered in the server. In case the payment was processed but order was not processed by mistake , webhooker will create an order
  
For some/all of your features, you may choose to reference the specific project files that implement them, although this is entirely optional.

In addition, you may also use this section to discuss plans for additional features to be implemented in the future:

### Features Left to Implement
- the shipping logic should be more complex providing different rates that adapt to different countries and sizes of the items shipped
- customer should be able to add the payment code directly in the app 
- the app should have the otpion to change laguage in order to result more customer friendly
- the bag should be emptied after a certain time of user inactivity 
- login possible also with Facebook


## Technologies Used

- [JQuery](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation.
- [Django3](https://docs.djangoproject.com/)
    - The project uses **Django 3** to .
- [Bootstrap4](https://getbootstrap.com/)
    - The project uses **Bootstrap 4** to  .

## Testing

To test the project the following accounts should be used

- customer
USERNAME : ctest
PASSWORD : ctest1234

- seller (superuser)
USERNAME : stest
PASSWORD : stest12345

To test the Stripe payment use the follwong test cc:

NUMBER: 4242 4242 4242 4242
EXP: 02 /22
CVC: 424

Most of the webiste has been automated-tested with Django TestCase

The section tested have been Profile, Products, Chekout and Bag.

In all these sections I have run tests for views, forms and models.

Tu run the tests ? 

The project has also been tested manually.

These tests have been carried on manually adn can be reproduced:

1. Product Availabilioty decreases after an order:
    1. As superuser creates product "Test" and sets availability to 3
    2. Add to the bag 3 items of product "Test"
    3. Verify that you can't add more items of this product
    4. Finalize the order
    5. Verify that bag is now empty
    6. Go to "products" and verify that the product is now marked as not avaialable

The project is responsive to different sceens . All test concerning responsiveness have been carried out using Chrome Inspector. The mimimum screen considered has been 320*640px

### Bugs and problems

- Availability
- Delivery problems
Some products can only be delivered to Ireland . On top of it delivery to Ireland is also chepar compared to EU countries.
Obviously the information about a possible delivery problem and about delivery fees had to be constant during the whole purchasing process.
In order to achieve that I decided to use as a reference the delivery saved in the use profile. In case of anonymous user I have decided to assume he/she is not from Ireland.
This was made possible through the use of session variable and template tagging. At the same time user had to be given the possiblity to change deliver address at checkout.
I had then to create a new session variable that reflected this choice.
ser choice had to be considered more relevant than saved delivery address at checkout stage. Although saved delivery adrres had to be considered more relevant in case of following purchasse during the same session. 
All the logic that assigned a specific delivery fee or detected  a delivery problem takes place inside the context file (bag).

- Payment choice: Stripe and payment by PayPal invoice
The whole checkout page had to be made responsive to the decision of the guest to pay either by Paypal or Stripe.
This was graphically achieved with scripts, whereas different view handles the logic.


## Deployment

The project has been deployed on [Heroku](https://heroku.com/) and on AMS

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:
- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally.


### Content
- The text for section Y was copied from the [Wikipedia article Z](https://en.wikipedia.org/wiki/Z)

### Media
- The photos used in this site were obtained from [Unsplash](https://unsplash.com/)

### Acknowledgements

- I received inspiration for this project from the E-commerce project at the end on my Full-stack Code Institute course
