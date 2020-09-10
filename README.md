# Furnitart

Furnitart is the website of a furniture shop based in Ireland that wants to start selling on the e-market.
The e-store is allows shipping all around Europe at different shipping rates. 

 
## UX
 
This website is thought for 2 different users : the customer and the seller.
### Customer
The customer is able to view all different products and order them with using various filters.

The customer can buy various items and finanlly pay for them (Stripe). In this case he/she will recieve a notification that the order is being processed.
The seller will send a noftification when the order is shipped  

The customer can also decide to request a Paypay invoice that generates an invoice, payable in the following 3 days. Once paid he/she is supposed to contact the seller in order to upgrade the preorder into an order( then previous flow applies).
This option is suggested to the customer as it does not lead to any processing fee for the seller.

The customer can also register. As a plus he will be able to take track of all his/ orders on the secion My profile 

-user story1:

User is looking for a new table with a very reduced size for his studio. User searches for table and order results for size (smaller to bigger).

Finally he finds a product that he likes. He is tempted to pay by Stripe but notices that payment by PayPal invoice has a nice discount.

He makes the preorder, makes a payment on Paypal and emails the payment number to the seller.

After few days he is informed that the the payment was confirmed. After foew more days he recieved an email confirming the shipment with a shipping tracking code.


### Seller

After logging in the seller will be able to control orders preorders and the inventory.

The seller will be able to handle the processing of the orders and send info to the customers about the orders.

The seller will also be able to add / delete / modify products and will always have control over the number of items available

-seller story 1:

The seller has 2 units of a product that, due to its size, can only be delivered to Ireland 
The seller receives a preorder for 1 unit to be shipped to Ireland. The available quantity is now only 1 on the website.
After 3 days, he has not recieved any information about the payment from the customer . He, then, decides to delete the prepayment in order to increase the product availability.

-seller story 2:

The seller has 2 units of a product that, due to its size, can only be delivered to Ireland 
The seller receives a preorder for 1 unit to be shipped to Ireland. The available quantity is now only 1 on the website.
After 2 days, he receives an email from the guest with the payment invoice. The seller conforms through the app that payment has been received.
After 1 day he has shipped the item and can confirm the shipment with a shipping code.



In particular, as part of this section we recommend that you provide a list of User Stories, with the following general structure:
- As a user type, I want to perform an action, so that I can achieve a goal.

This section is also where you would share links to any wireframes, mockups, diagrams etc. that you created as part of the design process. These files should themselves either be included as a pdf file in the project itself (in an separate directory), or just hosted elsewhere online and can be in any format that is viewable inside the browser.

## Features

In this section, you should go over the different parts of your project, and describe each in a sentence or so.
 

### Existing Features
- Management : allows sellers to keep track of the full inventory. allows sellers to keep track of orders and preorders
- Profile : allows users to keep track of orders and preorders
- Prducts :allowa user to filter products or order them 


For some/all of your features, you may choose to reference the specific project files that implement them, although this is entirely optional.

In addition, you may also use this section to discuss plans for additional features to be implemented in the future:

### Features Left to Implement
- Another feature idea

## Technologies Used

In this section, you should mention all of the languages, frameworks, libraries, and any other tools that you have used to construct this project. For each, provide its name, a link to its official site and a short sentence of why it was used.

- [JQuery](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation.


## Testing

In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:

1. Contact form:
    1. Go to the "Contact Us" page
    2. Try to submit the empty form and verify that an error message about the required fields appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that a success message appears.

In addition, you should mention in this section how your project looks and works on different browsers and screen sizes.

You should also mention in this section any interesting bugs or problems you discovered during your testing, even if you haven't addressed them yet.

If this section grows too long, you may want to split it off into a separate file and link to it from here.

## Deployment

This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:
- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally.


## Credits

### Content
- The text for section Y was copied from the [Wikipedia article Z](https://en.wikipedia.org/wiki/Z)

### Media
- The photos used in this site were obtained from ...

### Acknowledgements

- I received inspiration for this project from X
