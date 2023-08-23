# Wushu Server 🥋
A comprehensive backend for the Cornell Wushu Team, designed to handle authentication, member management, images, list serves, and performance details.

## Features
- Authentication: Secure JWT based authentication system.
- Member Management: CRUD operations for team members.
- Images: Upload and manage image assets.
- List Serves: Manage mailing lists.
- Performances: Keep track of all performances and related data.

## Getting Started
### Prerequisites
- Flask
- Flask-JWT-Extended
- Flask-CORS

### Installation
- Clone the repository
  ```bash
  git clone https://github.com/pratyush1712/wushu-server.git
  ```
- Navigate to the project directory:
  ```bash
  cd wushu-server
  ```
- Install the required packages
  ```bash
  pip install -r requirements.txt
  ```
- Run the server:
  ```bash
  python main.py
  ```

## Endpoints
- /auth/token - Token generation for authentication.
- /auth/logout - Log out and clear tokens.
- /auth/auth-check - Check if a user is authenticated.
- /list_serv - CRUD for list serves.
- /images - Image management.
- /members - CRUD operations for members.
- /performances - CRUD operations for performances.

## Contributing
If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.
