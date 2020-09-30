# Furnitart

Furnitart is a furniture shop based in Ireland that has developed a business model based on easy-to-assemble furniture that can be shipped all around Europe.
The shop is currently selling online on big platforms. Eventually they develop a base of recurring clients who are enthusiast about their products.
The shop would like to divert those customers, who used to buy their products on big online platforms, to their brand-new website based on this project.
This would definitely allow the company to develop their online presence and to keep transaction fees lower.

## UX

This website is designed for 2 different users : the customer and the seller.

### User stories

- Customer

1. I want to see only products I am interested in. I want to be able to filter and order them so that I can find the product I really need.
2. I want to be given the possibility to choose the payment method.
3. I want to be informed if my items are shipped and I want to receive all relevant information about the shipping.
4. I want to be informed before I buy a product if that is not deliverable to my place.
5. I want to have all my orders and preorders visible at a glance.
6. I want to be updated about any action taken on my order by email .

- Seller

1. I want to have an idea of how business is going and how much available inventory I have at a glance.
2. I want to offer to the user the possibility to pay by PayPal. It is more convenient for me, and I am ready to offer a discount on the grand total.
3. I want to set different delivery rates depending on the delivery destination
4. I want the user to be automatically informed by email when I take any action on an order.

## Features

### Existing Features

- Management: allows sellers to keep track and modify inventory, orders and preorders. Amending orders / preorders allows seller to send automatic emails to customers and keep them updated of order/preorder/shipment status
- Profile: allows users to amend delivery information and keep track of orders and preorders
- Products:allows user to see the products, filter and order them
- Checkout:allows user get a PayPal invoice or to pay directly (Stripe). The Stripe payment is done using the support of a web hooker. This ensures that orders are always correctly registered in the server. In case the payment was processed but order was not processed by mistake , webhooker will create an order.

### Features Left to Implement

- the shipping logic should be more complex providing different rates that adapt to different countries and sizes of the items shipped. The product model already has weight and sizes field. Those along with delivery destination should be used to implement automatic delivery calculation.
- the customer should be able to add the payment code directly in the app
- the app should have the option to change language in order to result more customer friendly
- the bag should be emptied after a certain time of user inactivity
- Registration should be possible also with Facebook

## Technologies Used

- [JQuery](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation.
- [Django3](https://docs.djangoproject.com/)
    - The project uses **Django 3** as framework to achieve rapid development and clean, pragmatic design.
- [Bootstrap4](https://getbootstrap.com/)
    - The project uses **Bootstrap 4** to achieve a responsive, mobile-first site.
- [Python 3](https://www.python.org//)
    - The project uses **Python3** for back-end development.
- [Stripe](https://stripe.com/)
    - The project uses **Stripe** for onnline payment processing.
- [Heroku](https://heroku.com/)
    - The project uses **Heroku** as deployment evoiroment.
- [AWS Simple Cloud Storage (S3)](https://aws.amazon.com/s3/)
    - The project uses **S3** to store media and static files during deployment.
- [PostgreSQL](https://www.postgresql.org/)
    - The project uses **PostgreSQ** as object-relational database system during deployment.
- [Gmail](https://mail.google.com/)
    - The project uses **Gmail** SMTP server to manage email sending during deployment.
- [Git](https://git-scm.com//)
    - The project uses **Git** as version control system.

## Testing

### How project was tested

Most of the project has been automated-tested with Django TestCase (overall coverage 60%).

More in details the modules tested have been Profile, Products, Chekout and Bag.

In all these sections I have run tests for views, forms and models.

The project has also been tested manually. Below some tests.

1. Product Availability decreases after an order:
    1. As superuser creates product "Test" and sets availability to 3.
    2. Add to the bag 3 items of product "Test".
    3. Verify that you can't add more items of this product.
    4. Finalize the order.
    5. Verify that bag is now empty.
    6. Go to "products" and verify that the product is now marked as not avaialable.
2. Orders in profile:
    1. Create a new profile.
    2. Make an order.
    3. Go to profile and verify the order is in the list.
3. Shipment info:
    1. Make an order.
    2. As superuser mark order as shipped and add shipping code in the pop-up menu.
    3. Verify you have received the email with this shipping information and that the info is also available in your Profile.
4. Customer is always informed about shipping problem:
    1. Login and amend delivery country to Germany.
    2. Select a product not deliverable to Eu.
    3. The bag template should already be warning you of a problem with delivery.
    4. Go to checkout. No payment option is available.
    5. Select country Ireland.
    6. Payment options are now avaialable.
5. PayPal payment option applied discount:
    1. Select a product and go to checkout.
    2. Select PayPal payment and process preorder.
    3. Notice discount has been applied on the preorder confirmation.
6. Cancelled preorders disappear from customer profile and availability of products is autoreplenished.
    1. Log in as customer.
    2. Create a preorder.
    3. Check preorder is available.
    4. Log out and log in as seller.
    5. Mark preorder as invalid / expired. 
    6. Check in product list that availability has been replenished.
    7. Log out and log in as customer.
    8. Check preorder is not available anymore in the preorder list.

### How to reproduce tests

- How to reproduce automatic tests

1. Go to GitHub repository.
2. Clone this project.
3. Open the project in GitPod.
4. Execute the following: python3 manage.py test.

- How to reproduce manual tests

To test the project the following accounts should be used:

- customer
USERNAME: ctest
PASSWORD: ctest1234

- seller (superuser)
USERNAME: stest
PASSWORD: stest12345

To test the Stripe payment use the following test cc:

NUMBER: 4242 4242 4242 4242
EXP: 02 /22
CVC: 424

### Layout responsiveness

The project is responsive to different screens. All test concerning responsiveness have been carried out using Chrome Inspector. The minimum screen considered has been 320\*640px

### Bugs and problems

#### Problems solved

- Delivery problems
Some products can only be delivered to Ireland. On top of it, delivery to Ireland is also cheaper compared to EU countries.
Obviously the information about a possible delivery problem and about delivery fees had to be constant during the whole purchasing process.
In order to achieve that I decided to use as a reference the delivery saved in the use profile. In case of anonymous user I have decided to assume he/she is not from Ireland.
This was made possible through the use of session variable and template tagging. At the same time the user had to be given the possibility to change delivery address at checkout.
I had then to create a new session variable that reflected this choice.
User choice had to be considered more relevant than saved delivery address at checkout stage. Although saved delivery address had to be considered more relevant in case of following purchase during the same session.
All the logic that assigned a specific delivery fee or detected a delivery problem takes place inside the context file (bag).

- Payment choice: Stripe and payment by PayPal invoice
The whole checkout page had to be made responsive to the decision of the guest to pay either by PayPal or Stripe.
This was graphically achieved with scripts, whereas different view handles the logic.

- Products and order management: modals
The seller has the possiblity to take action and send automatically an email to customers.
In order to avoid mistakes and to make the management section more user-friendly, modal windows have been addedd.

- Pictures upload
The app is optimized for displaying pictures with the same width and height. 
This was achived with the use of CSS media queries.
Initially it was considered the possiblity to modify the pictures directly before saving them. This approach was eventually not followed as the CSS one was considered more user-friendly,allowing the use to see the access the full original picture.

#### Known bugs

- Areas
On top nav a small area of space around the word 'Areas ^', when clicked, opens the dropdown menu but does not change Chevron icon orientation.
The issue was not addressed due to lack of time and low relevance.

- Availability
The app does register a change in the availability of the product only when the checkout process is completed.
This creates the following issue: during the time between adding to bag and finalizing the checkout the app does not detect possible availability changes.
This can lead to over sale situations.

## Deployment

The project has been developed in Gitpod and deployed on [Heroku](https://heroku.com/).
The deployed project is visible [here ](https://furnitart.herokuapp.com/)
The following steps have been taken to deploy on Heroku:

- install the following Django packages:
    1. Gunicorn (run the application on the server)
    2. Psycopg2-binary (to connect to a PostgreSQL database)
- create requirement.txt file
- create Procfile
- login to Heroku
- create new app in Heroku
- go to settings.py and amend DATABASE settings in order to point to PostgrSQL URI
- make migrations
- add new environment variable in Heroku: DATABASE_URL = PostgrSQL URI
- go to settings.py and amend DATABASE settings. In case DATABASE_URL is present as environment variable, point to that.
- temporary disable collect static
- add new environment variable in Heroku: SECRET_KEY
- In settings edit DEBUG: DEBUG = 'DEVELOPMENT' in os.environ
- add new environment variable in GitPod: DEVELOPMENT
- S3 setup:
    1. Create an AWS account and go to S3
    2. Create a bucket
    3. Change bucket settings
    4. create a group
    5. attach policy to group
    6. create a user and add it to the group
    7. add user to group
    8. download CSV file.

- connect Django to S3:
    1. install boto3
    2. install django-storages
    3. add ‘storages’ to INSTALLED APPS
    4. add keys from CSV file in Heroku: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
    5. remove DISABLE_COLLECTSTATIC
    6. in Django create a file custom_storages.py
    7. in settings.py add static and mediafile environment variables
    8. Add cache control
    9. In AWS create new folder MEDIA
- add Stripe keys to the Heroku config variable
- create a new webhook endpoint for Stripe.

To run the app locally follow these steps:

- Go to GitHub repository
- Clone this project
- Open the project in GitPod
- Execute the following: python3 manage.py runserver

### Content

- The code dealing with Stripe process and consequent webhook handler has been partially taken from the [official Stripe documentation](https://stripe.com/docs)
- I received inspiration for this project from the E-commerce project at the end on my Full-stack Code Institute course

### Media

- The photos used in this site were obtained from [Unsplash](https://unsplash.com/)

### Acknowledgments

- My Mentor for continuous helpful feedback.

- Tutor support at Code Institute for their support.
