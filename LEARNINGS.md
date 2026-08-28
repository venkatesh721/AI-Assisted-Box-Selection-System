Key Learnings from the Assignment

1. Understanding the Problem:

In this assignment, I learned how to design and develop a Django-based system for selecting a suitable shipping box for an ecommerce order. The system considers the dimensions and weight of products and compares them with the dimensions and maximum weight capacity of available boxes.

I understood that the main challenge is to select a box that can safely contain the products while following the packing requirements. I also learned that the cost of the box is an important factor when selecting the most suitable option.

2. Django Development:

This assignment improved my understanding of Django and REST API development. I learned how to organize a Django project and connect the different components such as models, API logic, URLs, database configuration, and tests.

I also learned how to implement business logic in a backend application instead of handling everything directly inside the API endpoint. This made the project easier to test and maintain.

3. Box Selection and Orientation:

One of the most important things I learned was how to handle product dimensions correctly.

A product does not always have to be placed in only one fixed orientation. Its length, width, and height can be rearranged when checking whether it fits inside a box. Therefore, the system needs to consider possible orientations before deciding that a product cannot fit.

I also learned that checking dimensions alone is not enough. The product or order weight must also be compared with the maximum weight capacity of the selected box.

For multiple products, I learned that the system needs to follow the specified single-row packing rule from the assignment rather than simply checking each product separately.

4. Testing:

Testing was another important part of this assignment. I learned how automated tests can be used to verify the recommendation logic and API behavior.

I tested different situations, including products that fit inside boxes, products that do not fit, different orientations, weight limitations, and multiple-product orders.

The final test suite passed successfully with all 26 tests passing,The tests helped me verify that the implementation worked correctly and also gave me confidence that changes to the code did not break existing functionality.

5. Debugging:

During this assignment, I faced different issues while developing and testing the Django application. I learned that reading the error message carefully helps to identify the actual problem instead of changing the code randomly.

I faced issues related to the Django project configuration, API implementation, and application logic. I checked the error messages, identified the relevant code, made the required changes, and tested the application again.

I also learned that after fixing an issue, it is important to run the test cases again. This helped me make sure that the changes fixed the problem without affecting the existing functionality.

6. AI-Assisted Development:

I used OpenAI Codex during this assignment to understand the requirements, discuss implementation approaches, debug errors, and improve parts of the project.

AI helped me understand some Django and Python concepts and suggested different ways to implement the box selection logic and tests. I did not blindly accept every suggestion. I reviewed the suggested code and changed parts of it when they did not match my project or the assignment requirements.

I also used AI to help identify errors and understand possible solutions. After making changes, I verified the implementation by running the application and executing the test cases.

One important thing I learned from using AI is that generated code can contain mistakes or may not exactly match the requirements. The developer needs to understand the code, review the suggestions, make necessary changes, and test the final implementation.

Using AI helped me work faster, but I learned that testing and verifying the final code is still my responsibility.


7. GitHub and Continuous Integration:

I also learned more about using Git and GitHub as part of a software development workflow.

I learned how to commit changes, push the project to GitHub, and use GitHub Actions to automatically run the test suite.

Having automated tests run through GitHub Actions helped me verify that the project was working correctly in the repository and not only on my local machine.

8. Final Takeaway:

Overall, this assignment gave me practical experience in developing a complete Django backend application from a real-world requirement.

I improved my understanding of Django, REST APIs, database usage, business logic, dimension and weight validation, product orientation, multiple-product handling, automated testing, debugging, Git, GitHub, and CI.

The biggest lesson I learned is that writing code is only one part of developing a project. Understanding the requirements, testing different cases, debugging problems, documenting the implementation, and verifying the final result are equally important.

I also learned how to use AI as a development assistant while still reviewing and verifying the generated suggestions before including them in the final project.
