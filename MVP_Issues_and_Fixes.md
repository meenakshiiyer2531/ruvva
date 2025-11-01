# MVP Issues and Fixes Tracker

This document outlines the problems encountered during the development of the CareerConnect backend MVP, their resolutions, and a list of remaining issues or refactoring suggestions to ensure the project functions perfectly.

---

## Resolved Issues

Below is a list of problems that have been identified and fixed:

1.  **Firebase Configuration Disabled**
    *   **Problem:** Firebase integration was initially disabled in `application.properties` and `application.yml`.
    *   **Resolution:** Changed `firebase.enabled` to `true` in both `application.properties` and `application.yml` to activate Firebase.

2.  **`run-dev.sh` Line Endings Issue**
    *   **Problem:** The `run-dev.sh` script failed to execute on Linux due to CRLF line endings.
    *   **Resolution:** Converted `run-dev.sh` to use LF line endings using the `sed` command.

3.  **Missing `JAVA_HOME` Environment Variable**
    *   **Problem:** The `mvnw` script failed because the `JAVA_HOME` environment variable was not set.
    *   **Resolution:** This was addressed by the user manually setting the `JAVA_HOME` environment variable.

4.  **`PlaceholderResolutionException` for Environment Variables**
    *   **Problem:** Environment variables like `JWT_SECRET`, `FIREBASE_DATABASE_URL`, and `FIREBASE_PROJECT_ID` were not being resolved, causing application startup failures.
    *   **Resolution:** Modified `run-dev.sh` and `run-dev.bat` to correctly source the `.env` file, loading these environment variables into the shell. `application-dev.yml` was also reverted to use these environment variables.

5.  **`SilentExitException` with Spring Boot DevTools**
    *   **Problem:** The application crashed with a `SilentExitException` due to conflicts with Spring Boot DevTools' automatic restart feature, especially in conjunction with Java 21's module system.
    *   **Resolution:** Removed the `spring-boot-devtools` dependency from `pom.xml` and the `spring.devtools.restart.enabled=false` property from `application-dev.yml`, effectively rolling back DevTools integration.

6.  **`NoSuchBeanDefinitionException` for `WebClient`**
    *   **Problem:** `GeminiAIService` failed to inject `WebClient` when the Gemini API key was not provided, leading to application startup failure.
    *   **Resolution:** Modified `GeminiAIService` to make the `WebClient` dependency optional in its constructor, allowing the application to start even if the Gemini API key is empty (AI features will be disabled gracefully).

7.  **`InaccessibleObjectException` (Java 21 Module System)**
    *   **Problem:** A `java.lang.reflect.InaccessibleObjectException` occurred due to reflective access to internal JDK modules by the Firebase/Firestore SDK, blocked by Java 21's module system.
    *   **Resolution:** Added `--add-opens` JVM arguments to the `spring-boot-maven-plugin` configuration in `pom.xml` to allow the necessary reflective access.

8.  **`Invalid JWT Signature` (Firebase Service Account Key)**
    *   **Problem:** Firebase authentication failed with an "Invalid JWT Signature" error, indicating an issue with the provided service account key.
    *   **Resolution:** Advised the user to replace the content of `src/main/resources/credentials/serviceAccount.json` with a new, valid service account key from their Firebase project settings.

9.  **Incorrect Registration Endpoint Usage**
    *   **Problem:** The user was sending the detailed student registration payload to `POST /api/auth/register`, which is for generic user registration, leading to `null` values for student-specific fields.
    *   **Resolution:** Explained the difference between `POST /api/auth/register` and `POST /api/students/register`, guiding the user to use the correct student-specific endpoint.

10. **`Authentication` Object is `null` (JWT Not Processed)**
    *   **Problem:** The `Authentication` object was `null` in protected endpoints, causing `submitAssessment` to fail, because the JWT authentication filter was not correctly integrated into Spring Security.
    *   **Resolution:** Configured Spring Security in `SecurityConfig.java` to use `JwtAuthenticationFilter` and properly protect endpoints, ensuring the security context is populated.

11. **`PatternParseException` in `SecurityConfig`**
    *   **Problem:** A `PatternParseException` occurred due to an invalid URL matching pattern (`/**/health`) in Spring Security's `requestMatchers`.
    *   **Resolution:** Replaced the problematic pattern with a more explicit list of health endpoint patterns in `SecurityConfig.java`.

12. **`403 Forbidden` for Health Endpoints**
    *   **Problem:** Health check endpoints were still returning `403 Forbidden` even after being explicitly permitted.
    *   **Resolution:** Adjusted `requestMatchers` patterns in `SecurityConfig.java` to exclude the `/api` context path, as Spring Security matches patterns against the URL after the context path removal.

13. **Mock Token Still Generated After Firebase Fix**
    *   **Problem:** Even after Firebase was successfully initialized, the login endpoint was still returning a mock JWT token. This was due to `AuthController.loginWithFirebase` still calling `authService.mockLogin`.
    *   **Resolution:** Modified `AuthController.loginWithFirebase` to correctly call `authService.login` (the real authentication service) to generate valid JWT tokens.

14. **Compilation Error in `AuthController.java` (Syntax)**
    *   **Problem:** A compilation error occurred in `AuthController.java` due to a missing `try` block in the `loginWithFirebase` method, which was inadvertently removed during a previous `replace` operation.
    *   **Resolution:** Restored the `try` block in `loginWithFirebase` in `AuthController.java` to fix the syntax error.

15. **`Failed to find user` During Login**
    *   **Problem:** Login failed with "Failed to find user" because the authentication service was looking for users in the `users` collection, but students were registered and stored in the `students` collection.
    *   **Resolution:** Modified `UserDetailsServiceImpl` to load `Student` objects from `StudentService` for authentication.

16. **Compilation Error in `MockAuthController.java` (`getUsername()` not found)**
    *   **Problem:** After changing `LoginRequest` from `username` to `email`, `MockAuthController.java` failed to compile because it was still calling `request.getUsername()`.
    *   **Resolution:** Updated all instances of `request.getUsername()` to `request.getEmail()` in `MockAuthController.java`.

17. **Circular Dependency Between Beans**
    *   **Problem:** A circular dependency was detected between `jwtAuthenticationFilter`, `userDetailsServiceImpl`, `studentService`, and `securityConfig`.
    *   **Resolution:** Temporarily allowed circular references by setting `spring.main.allow-circular-references=true` in `application-dev.yml` to allow the application to start.

---

## Remaining Issues & Refactoring Suggestions (MVP Focus)

These are areas that should be addressed for a robust and clean MVP, or considered for future improvements.

1.  **Resolve Circular Dependency (High Priority for Clean Code)**
    *   **Issue:** The `spring.main.allow-circular-references=true` is a temporary workaround. The circular dependency between `SecurityConfig` (providing `PasswordEncoder`) and `StudentService` (injecting `PasswordEncoder` via `UserDetailsServiceImpl) needs to be properly broken.
    *   **Suggestion:** Refactor `StudentService` to not directly depend on `PasswordEncoder`. Instead, `PasswordEncoder` could be injected into `AuthService`, and `AuthService` could handle password encoding for `Student` objects before they are passed to `StudentService` for persistence. Alternatively, consider a dedicated `PasswordEncodingService`.

2.  **`User` Entity and `UserDto` Inconsistencies (Medium Priority)**
    *   **Issue:** The `User` entity and `UserDto` still contain `username` fields, which are now inconsistent with the `email`-based login. This can lead to `null` or unexpected values in the `username` field of the `UserDto` returned in the login response.
    *   **Suggestion:** Refactor the `User` entity and `UserDto` to consistently use `email` as the primary identifier. If the `username` field is no longer needed, it should be removed. If it serves a different purpose (e.g., display name), it should be renamed and clearly distinguished from the login identifier.

3.  **`AuthService.register` and `AuthService.mockLogin` (Medium Priority)**
    *   **Issue:** These methods still operate on a generic `User` object, which might be inconsistent with the `Student` registration flow. `AuthService.register` currently saves a `User` to the `users` collection, while `StudentController.registerStudent` saves a `Student` to the `students` collection.
    *   **Suggestion:** Re-evaluate the purpose of `AuthService.register`. If `StudentController.registerStudent` is the primary registration path, `AuthService.register` might be redundant or need to be adapted to create a linked `User` object for authentication purposes. The `AuthService.mockLogin` is only used when Firebase is unavailable, but its logic could be simplified if the `User` entity is refactored.

4.  **`FirebaseAuthService.isFirebaseAuthAvailable()` Simplification (Low Priority)**
    *   **Issue:** The check was simplified to avoid permission issues with `firebaseAuth.listUsers`.
    *   **Suggestion:** While the current simplification works, if the application ever needs to perform operations requiring `listUsers` permissions, ensure the Firebase service account has the necessary roles.

5.  **`commons-logging.jar` Warning (Low Priority)**
    *   **Issue:** A warning about `commons-logging.jar` being on the classpath, potentially causing conflicts with `spring-jcl`.
    *   **Suggestion:** Identify the transitive dependency that brings in `commons-logging.jar` and exclude it in `pom.xml` to clean up the logs.

---

This document will serve as a guide for further development and refinement of the CareerConnect backend.
