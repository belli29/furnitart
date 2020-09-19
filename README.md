# Furnitart

Furnitart is the website of a furniture shop based in Ireland that wants to start selling on the e-market.
The e-store allows shipping all around Europe at different shipping rates.

## UX

This website is designed for 2 different users : the customer and the seller.

### User stories

- Customer

1. I want to see only products I am interested in. I want to be able to filter and order them so that I can find the produt I really need
2. I want to be given the possiblity to choose the payment method and to get a small discount in case the purchase is not immediate (PayPal)
3. I want to be informed if my items is shipped and I want to received shipping code in order to track it
4. I want to be informed before i buy a product if that is not delivarable to my place
5. I want to have all my orders and preorders visible at a glance
6. I want to have info about shipment / "preorder upgrading to order" / preorder cancelled avaialable on the web but I also want to receive an email everytime something changes

- Seller

1. I want to have an idea of how business is going and how much avaialable inventory I have at a glance
2. I want to offer to the user the possiblity to pay by Paypal. It is more convenient for me and I am ready to offer a discount on the grand total
3. I want to set different delivery rates depending on the delivery destination
4. I want user to be automatically informed by email when I take any action on an order

## Features

### Existing Features

- Management : allows sellers to keep track and modify inventory, orders and preorders. Amending orders / preorders allows seller to send automatic emails to customers and keep them updated of order/preorder/shipment status
- Profile : allows users to anebd delivery information and keep track of orders and preorders
- Products :allows user to see the products, filter and order them
- Checkout :allows user get a paypal invoice or to pay directly (Stripe). The Stripe payment is done using the support of a webhooker. This ensures that orderes are always correctly registered in the server. In case the payment was processed but order was not processed by mistake , webhooker will create an order

For some/all of your features, you may choose to reference the specific project files that implement them, although this is entirely optional.

In addition, you may also use this section to discuss plans for additional features to be implemented in the future:

### Features Left to Implement

- the shipping logic should be more complex providing different rates that adapt to different countries and sizes of the items shipped. The product model already has weight and sizes field. Those along with delivery destination should be used to implement automatic delivery calculation.
- customer should be able to add the payment code directly in the app
- the app should have the option to change laguage in order to result more customer friendly
- the bag should be emptied after a certain time of user inactivity
- rRegistration should be possible also with Facebook

## Technologies Used

- [JQuery](https://jquery.com)
  - The project uses **JQuery** to simplify DOM manipulation.
- [Django3](https://docs.djangoproject.com/)
  - The project uses **Django 3** as framework to achieve rapid development and clean, pragmatic design.
- [Bootstrap4](https://getbootstrap.com/)
  - The project uses **Bootstrap 4** to achieve a responsive, mobile-first site.

## Testing

### How to test the project

### How project was tested

Most of the project has been automated-tested with Django TestCase (overall coverage 55%).

More in details the modules tested have been Profile, Products, Chekout and Bag.

In all these sections I have run tests for views, forms and models.

The project has also been tested manually. Below some of the tests.

1. Product Availability decreases after an order:

   1. As superuser creates product "Test" and sets availability to 3
   2. Add to the bag 3 items of product "Test"
   3. Verify that you can't add more items of this product
   4. Finalize the order
   5. Verify that bag is now empty
   6. Go to "products" and verify that the product is now marked as not avaialable

2. Orders in profile

   1. Create a new profile
   2. Make an order
   3. Go to Profiel and verify the order is in the list

3. Shipment info:

   1. Make an order
   2. As superuser mark order as shipped and add shipping code in the pop-up menu
   3. Verifya you have recieved the email with this shipping information and that the ifo is also avaialable in your Profile

4. Customer is alsways informed about shipping problem:

   1. Login and amend delivery country to Germany
   2. Select a product not delivarable to Eu
   3. The bag template should already be warning you of a problem with delivery
   4. Go to checkout. No payment option is avaialable
   5. Select country Ireland
   6. Payment options are now avaialable

5. Paypal payment option applied discount:
   1. Select a product and go to checkout
   2. Select Paypal payment and process preorder
   3. Notice discount has been applied on the preorder confirmation

### How to reproduce tests

- How to reproduce automatic tests

1. Go to GitHub repository
2. Clone this project
3. Open the project in GitPod
4. Execute the folloowing : python3 manage.py test

- How to reproduce manual tests

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

### Layout responsiveness

The project is responsive to different screens . All test concerning responsiveness have been carried out using Chrome Inspector. The mimimum screen considered has been 320\*640px

### Bugs and problems

#### Problems solved

- Delivery problems
  Some products can only be delivered to Ireland . On top of it, delivery to Ireland is also cheaper compared to EU countries.
  Obviously the information about a possible delivery problem and about delivery fees had to be constant during the whole purchasing process.
  In order to achieve that I decided to use as a reference the delivery saved in the use profile. In case of anonymous user I have decided to assume he/she is not from Ireland.
  This was made possible through the use of session variable and template tagging. At the same time user had to be given the possiblity to change delivery address at checkout.
  I had then to create a new session variable that reflected this choice.
  User choice had to be considered more relevant than saved delivery address at checkout stage. Although saved delivery address had to be considered more relevant in case of following purchasse during the same session.
  All the logic that assigned a specific delivery fee or detected a delivery problem takes place inside the context file (bag).

- Payment choice: Stripe and payment by PayPal invoice
  The whole checkout page had to be made responsive to the decision of the guest to pay either by Paypal or Stripe.
  This was graphically achieved with scripts, whereas different view handles the logic.

#### Known bugs

- Areas
  On top nav a small area of space around the word 'Areas ^' , when clicked, opens the dropdown menu but does not change Chevron icon orientation.
  The issue was not adressed due to lack of time and low relevance.

- Availability
  The app does register a change in the avaialbility of the product only when the checkout process is completed.
  This creates the following issue: during the time between adding to bag and finalizing the checkout the app does not detect possible avaialbility changes.
  This can lead to oversale situations.

## Deployment

The project has been developed in Gitpod and deployed on [Heroku](https://heroku.com/).

The following actions have been taken to deploy on Heroku:

- A different database is used (postgres). The url is specified in Heroku environment variables
- Static / media files stored in AWS S3 service . Cache control has also been added to improve performance
- On Deploymnet sending emails has been done using on Gmail SMTP server

The app settings file recognizes if we are in development / deployment environment based on Global variables set in Heroku /Gitpod

More in details In Heroku (deployment), we have the following environment variables, not present on local (Gitpod):

USE_AWS = True;
AWS_ACCESS_KEY_ID;
AWS_SECRET_ACCESS_KEY;
EMAIL_HOST_USER;
EMAIL_HOST_PASS;
DATABASE_URL ;

The deployed project is visible [here ](https://furnitart.herokuapp.com/)

To run the app locally follow these steps:

- Go to GitHub repository
- Clone this project
- Open the project in GitPod
- Execute the folloowing : python3 manage.py runserver

### Content

- The code dealing with Stripe process and consequest webhook hadler has been partially taken from the [official Stripe documentation](https://stripe.com/docs)
- I received inspiration for this project from the E-commerce project at the end on my Full-stack Code Institute course

### Media

- The photos used in this site were obtained from [Unsplash](https://unsplash.com/)

### Acknowledgements

- My Mentor for continuous helpful feedback.

- Tutor support at Code Institute for their support.
