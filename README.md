# 🔗 Shawty - A Modern URL Shortener

![Shorty Application Screenshot](https://user-images.githubusercontent.com/your-username/your-repo/your-screenshot.png) <!-- 📸 Replace with a link to your own screenshot -->

**Shorty** is a full-featured, secure, and stylish URL shortening web application built with Python and Flask. It allows users to transform long, cumbersome URLs into short, memorable links. The application features user authentication, a personalized history of shortened links, and the ability to create custom-named short URLs.

**🚀 Live Demo:** [SHAWTY](https://shawtyurl.onrender.com) <!-- 🔗 Replace with your live deployment URL -->

---

## ✨ Features

-   **⚡ Fast & Simple URL Shortening:** Quickly generate a short URL for any valid web address.
-   **✏️ Custom Short Links:** Signed-in users can create custom, human-readable short links (e.g., `your-site.com/my-event`).
-   **🔐 User Authentication:** Secure user registration and login system to manage links.
-   **📜 Personal Link History:** Logged-in users have access to a history of all the links they have shortened.
-   **🛠️ Manage Links:** Users can easily copy or delete links from their history with a single click.
-   **🎨 Stylish UI:** A modern, responsive, and attractive user interface with a dynamic dark theme.
-   **✅ Custom Modals:** Polished, theme-matching confirmation dialogs for a better user experience.

---

## 🛠️ Tech Stack

This project was built using a modern web development stack:

-   **Backend:**
    -  Python Flask
-   **Database:**
    -  MongoDB Atlas
-   **Frontend:**
    -  HTML
    -  CSS
    -  JAVASCRIPT

---

## 🚀 Getting Started

To run this project locally, follow these steps:

### Prerequisites

-   Python 3.8 or higher
-   Pip (Python package installer)
-   Git
-   A free [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account

### ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment:**
    ```
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required packages:**
    ```
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    You need to create environment variables for your database connection string and a secret key.
    
    *   **`MONGO_URI`**: Your connection string from MongoDB Atlas.
    *   **`SECRET_KEY`**: A long, random string. You can generate one in a Python shell with:
        ```
        import secrets
        secrets.token_hex(32)
        ```
    
    Set these variables in your terminal before running the app.

5.  **Configure MongoDB Atlas Network Access:**
    -   Log in to your MongoDB Atlas account.
    -   Navigate to **Network Access** under the "Security" section.
    -   Click **"Add IP Address"** and then **"Allow Access From Anywhere"** (`0.0.0.0/0`).

6.  **Run the application:**
    ```
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

---

## ☁️ Deployment

This application is ready for deployment on services like Render, Heroku, or PythonAnywhere.

1.  Ensure you have a `requirements.txt` and a `Procfile` in your repository.
2.  Push your code to a GitHub repository.
3.  Connect your repository to a new "Web Service" on your hosting provider.
4.  Set the environment variables (`MONGO_URI` and `SECRET_KEY`) in your hosting service's dashboard.
5.  Deploy!

---

## 🙏 Acknowledgements

-   Inspired by modern URL shorteners like Bitly and Dub.co.
-   Icons provided by [Font Awesome](https://fontawesome.com/).
-   Guidance and templates from the open-source community.
