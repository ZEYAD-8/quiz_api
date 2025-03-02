# Quiz API

This project was created as the final project of the year at [`ALX`](https://tech.alxafrica.com/) SE program.

## Project Overview
The Quiz API is a robust and scalable solution for creating and managing quizzes and user attempts. It allows users to:

- Create and categorize quizzes.
- Attempt quizzes with different question types.
- View their attempt history and scores.
- Manage authentication and user access.

The API is hosted on Railway and available at the base URL:
**`https://quizapi.up.railway.app/v1`**.

This API supports a variety of question types, including:
- Multiple Choice
- True/False
- Matching Pairs
- Ordering Items

## Endpoints Overview

### Authentication
- **`POST /users/register/`**: Register a new user.
- **`POST /users/login/`**: Authenticate a user and retrieve a token.
- **`POST /users/change_password/`**: Changes the password.
- **`POST /users/change_role/`**: Changes the role of the user to the requested role.
- **`POST /users/profile/`**: Display user information and related details.
- **`GET /users/creations/`**: Returns the questions and quizzes created by this user (creator only).

### Quizzes
- **`GET /quizzes/`**: Retrieve a list of quizzes with optional filters.
  - Doesn't require authentication.
  - supports query parameters.
  - returns 1 random quiz by default.
- **`POST /quizzes/create/`**: Create a new quiz (creator only).
- **`GET /quizzes/{id}/`**: Retrieve details of a specific quiz.
- **`PUT /quizzes/{id}/`**: Update a quiz (creator only).
- **`DELETE /quizzes/{id}/`**: Delete a quiz (creator only).

### Questions
- **`GET /questions/`**: Retrieve a list of questions with optional filters.
  - Doesn't require authentication.
  - supports query parameters.
  - returns 5 random questions by default.
- **`POST /questions/create/`**: Create a new question (creator only).
- **`GET /questions/{id}/`**: Retrieve details of a specific question.
- **`PUT /questions/{id}/`**: Update a question (creator only).
- **`DELETE /questions/{id}/`**: Delete a question (creator only).

### Categories
- **`GET /categories/`**: Retrieve a list of available categories.
- **`POST /categories/create/`**: Create a new category (admin only).
- **`GET /categories/{str:identifier}/`**: Retrieve details of a specific category (the identifier can be the id or the slug).
- **`PUT /categories/{str:identifier}/`**: Update a category (admin only).
- **`DELETE /categories/{str:identifier}/`**: Delete a category (admin only).

### Quiz Attempts
- **`GET /attempts/`**: Retrieve user's quiz attempts.
  - supports one query parameters (quiz_id) to only get the attempts for a specific quiz.
- **`GET /attempts/{quiz_id}/`**: Get an *Answerless* view of the quiz to solve.
- **`POST /attempts/{quiz_id}/submit/`**: Submit a new attempt for a quiz and have it graded.
  - For the specific format to how to format each question type, view the postman documentation.
- **`GET /attempts/{quiz_id}/others/`**: Retrieve other users' attempts for a specific quiz (creator only).

## Documentation
For detailed API documentation, including request and response examples, authentication requirements, and more, refer to the Postman collection:
**[Postman Collection Link](https://documenter.getpostman.com/view/40691710/2sAYJAexhn#intro)**
There is also a [video](https://youtu.be/Cpncp9K9ShU?si=WNVP2Q39462nNvWv) that explains how to use the collection, endpoints and adds clarifications.

The Postman collection contains all the necessary details for testing and integrating with this API.

---

For any questions or support or if you want to integrate this API, feel free to reach out.

---

### 📞 Contact Me

| ![📧](https://img.shields.io/badge/Email-blue)     | [zeyadosama15@gmail.com](mailto:your_email@example.com) |
|----------------------------------------------------|---------------------------------------------------------|
| ![💼](https://img.shields.io/badge/LinkedIn-blue)  | [linkedin.com/in/zeyad-elnaggar](https://linkedin.com/in/yourprofile) |

---

