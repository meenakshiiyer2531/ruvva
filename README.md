# CareerConnect: AI-Powered Career Counseling Platform 🚀

Welcome to **CareerConnect**, a fully integrated, production-ready career counseling platform. This application leverages a microservices architecture to provide users with AI-driven career assessments, personalized chat-based guidance, and robust user profile management.

## 🖥 Platform Demo

[![Watch the CareerConnect demo](https://img.youtube.com/vi/SRnXmLy0TYM/maxresdefault.jpg)](https://www.youtube.com/watch?v=SRnXmLy0TYM)

## ✨ Features

-   🔐 **Secure Authentication**: User sign-up and login handled via Firebase Authentication with JWT tokens.
-   👤 **User Profile Management**: Full CRUD operations for user profiles, backed up in a local database.
-   🤖 **AI-Powered Chat**: Engage with an AI counselor for career advice, with conversations saved to your profile.
-   📝 **Career Assessments**: Take assessments to discover career paths, with results analyzed by our AI service.
-   🌐 **Resilient Architecture**: Built with fault-tolerant microservices that degrade gracefully.
-   🩺 **Health Monitoring**: Real-time service availability tracking to ensure a seamless user experience.

---

## 🛠️ Tech Stack & Architecture

CareerConnect is built on a distributed microservices architecture, ensuring scalability, fault tolerance, and independent service management.

<img width="511" height="452" alt="image" src="https://github.com/user-attachments/assets/af0b3330-50b1-42c1-9423-a086f2d50fc2" />



-   **Frontend**: React
-   **Backend**: Spring Boot (Java)
-   **AI Service**: Flask (Python)
-   **Database**: Firebase Firestore (Primary) & Local DB (Backup)
-   **Authentication**: Firebase Authentication

---

## 🔥 Getting Started

Follow these instructions to get the CareerConnect platform running on your local machine for development and testing.

### Prerequisites

Make sure you have the following software installed:

-   [Java 17+](https://www.oracle.com/java/technologies/downloads/) & [Maven](https://maven.apache.org/download.cgi)
-   [Python 3.8+](https://www.python.org/downloads/) & [pip](https://pip.pypa.io/en/stable/installation/)
-   [Node.js](https://nodejs.org/) & [npm](https://www.npmjs.com/get-npm)
-   A **Firebase project** with **Firestore Database** and **Authentication** (Email/Password provider) enabled.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/meenakshiiyer2531/ruvva.git](https://github.com/meenakshiiyer2531/ruvva.git))
    cd ruvva
    ```

2.  **Configure Firebase Credentials:**
    -   Go to your Firebase project settings and generate a private key for your service account.
    -   Download the `serviceAccountKey.json` file.
    -   Place the file in the configuration directory of both the **Spring Boot Backend** and the **Python AI Service**.

3.  **Start the Spring Boot Backend:**
    ```bash
    cd backend/backend
    ./mvnw spring-boot:run
    # Backend will be running on http://localhost:8080
    ```

4.  **Start the Python AI Service:**
    ```bash
    cd ../../career-connect-ai
    pip install -r requirements.txt # Or create and activate a virtual environment
    python app.py
    # AI Service will be running on http://localhost:5000
    ```

5.  **Start the React Frontend:**
    ```bash
    cd ../ruvaa-frontend
    npm install
    npm start
    # Frontend will be accessible at http://localhost:3000
    ```

You should now have the full platform running locally! 🎉

---

## 🗃️ Firebase Database Schema

User data is organized in the `users` collection within Firestore, with each user document containing sub-collections for their profile, assessments, and chat history.

/users/{userId}/
├── profile/        # User profile data (name, email, etc.)
├── assessments/    # Career assessment results and AI analysis
└── chatHistory/    # AI chat conversations and messages


---

## 🔒 Security

-   **Authentication Flow**: The frontend communicates with the Spring Boot backend, which validates tokens against Firebase Auth. The Python AI service also integrates with the backend to access user data securely.
-   **CORS**: Cross-Origin Resource Sharing is properly configured across all services to ensure secure communication between the frontend, backend, and AI service.

---

## 🧪 Testing the Integration

To ensure the platform is functioning correctly, perform the following tests:

1.  **Full Stack Test**: Run all services and complete a full user journey: sign up, log in, update profile, take an assessment, and use the AI chat.
2.  **Resilience Test**: Stop the Python AI Service or the Backend and verify that the frontend handles the failure gracefully by showing appropriate messages or using fallback data.
3.  **Database Test**: Verify that user data (profiles, assessments, chat history) is correctly persisted in both Firebase Firestore and the local backup database.
4.  **Authentication Test**: Test login with valid/invalid credentials and ensure that protected routes are inaccessible without a valid JWT token.

---

## 🎯 Production Readiness

The platform is architected for production deployment and is ready for:

-   Deployment to cloud providers like AWS, Google Cloud, or Azure.
-   Horizontal scaling of individual services to handle increased load.
-   Integration with CI/CD pipelines for automated builds and deployments.
-   Integration with monitoring and analytics tools for performance tracking.
