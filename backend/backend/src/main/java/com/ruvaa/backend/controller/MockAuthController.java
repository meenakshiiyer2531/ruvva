package com.ruvaa.backend.controller;

import com.ruvaa.backend.dto.LoginRequest;
import com.ruvaa.backend.dto.LoginResponse;
import com.ruvaa.backend.dto.UserDto;
import lombok.RequiredArgsConstructor;
import com.ruvaa.backend.mock.MockDataStore;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import java.time.LocalDateTime;
import java.util.Map;

/**
 * Mock Authentication Controller for testing without Firebase
 * Only active when Firebase is disabled
 */
@Slf4j
@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "false", matchIfMissing = true)
public class MockAuthController {

    private final MockDataStore store;
    private static final String SUCCESS_KEY = "success";
    private static final String MESSAGE_KEY = "message";
    // Simple in-memory token registry (token -> email) for mock mode
    private static final java.util.Map<String,String> TOKEN_REGISTRY = new java.util.concurrent.ConcurrentHashMap<>();

    /**
     * Register a new user (mock implementation)
     */
    @PostMapping("/register")
    public ResponseEntity<?> register(@Valid @RequestBody RegisterRequest request) {
        try {
            log.info("Mock registration request for email: {}", request.getEmail());

            // Check if user already exists
            if (store.getAuthUsers().containsKey(request.getEmail())) {
                return ResponseEntity.badRequest().body(Map.of(
                    SUCCESS_KEY, false,
                    MESSAGE_KEY, "User already exists with email: " + request.getEmail()
                ));
            }

            // Create mock user
            MockDataStore.MockUserAuth user = new MockDataStore.MockUserAuth(
                String.valueOf(System.currentTimeMillis()),
                request.getEmail(),
                request.getPassword(), // In real app, this would be hashed
                request.getName(),
                LocalDateTime.now()
            );
            store.getAuthUsers().put(request.getEmail(), user);

            UserDto userDto = UserDto.builder()
                .id(user.getId())
                .email(user.getEmail())
                .name(user.getName())
                .build();

            log.info("Mock user registered successfully: {}", request.getEmail());

            return ResponseEntity.ok(Map.of(
                SUCCESS_KEY, true,
                MESSAGE_KEY, "User registered successfully",
                "user", userDto
            ));

        } catch (Exception e) {
            log.error("Mock registration failed", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                SUCCESS_KEY, false,
                MESSAGE_KEY, "Registration failed: " + e.getMessage()
            ));
        }
    }

    /**
     * Login user (mock implementation)
     */
    @PostMapping("/login")
    public ResponseEntity<?> login(@Valid @RequestBody LoginRequest request) {
        try {
            log.info("Mock login attempt for: {}", request.getEmail());
            log.debug("[MockAuth] Store snapshot before login - authUsers: {}, students: {}", store.getAuthUsers().size(), store.getStudentsByEmail().size());

            MockDataStore.MockUserAuth user = store.getAuthUsers().get(request.getEmail());
            if (user == null) {
                // Fallback: if student exists (registered via /students), create auth record on-the-fly
                MockDataStore.MockStudent student = store.getStudentsByEmail().get(request.getEmail());
                if (student != null) {
                    user = new MockDataStore.MockUserAuth(student.getId(), student.getEmail(), request.getPassword(), student.getName(), student.getCreatedAt());
                    store.getAuthUsers().put(student.getEmail(), user);
                    log.info("[MockAuth] Auto-created auth user from student record for {}", request.getEmail());
                } else {
                    return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
                        SUCCESS_KEY, false,
                        MESSAGE_KEY, "User not found: " + request.getEmail()
                    ));
                }
            }

            // Simple password check (in real app, use proper password hashing)
            if (!user.getPassword().equals(request.getPassword())) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
                    SUCCESS_KEY, false,
                    MESSAGE_KEY, "Invalid password"
                ));
            }

            // Generate mock token
            String mockToken = "mock-jwt-token-" + System.currentTimeMillis();
            TOKEN_REGISTRY.put(mockToken, user.getEmail());

            UserDto userDto = UserDto.builder()
                .id(user.getId())
                .email(user.getEmail())
                .name(user.getName())
                .build();

            LoginResponse response = LoginResponse.builder()
                .token(mockToken)
                .type("Bearer")
                .user(userDto)
                .build();

            log.info("Mock login successful for: {}", request.getEmail());
            log.debug("[MockAuth] Store snapshot after login - authUsers: {}, students: {}", store.getAuthUsers().size(), store.getStudentsByEmail().size());

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            log.error("Mock login failed", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                SUCCESS_KEY, false,
                MESSAGE_KEY, "Login failed: " + e.getMessage()
            ));
        }
    }

    /**
     * Get all registered users (for testing)
     */
    @GetMapping("/users")
    public ResponseEntity<Map<String, Object>> getUsers() {
        return ResponseEntity.ok(Map.of(
            SUCCESS_KEY, true,
            "users", store.getAuthUsers().values().stream()
                .map(user -> Map.of(
                    "id", user.getId(),
                    "email", user.getEmail(),
                    "name", user.getName(),
                    "createdAt", user.getCreatedAt()
                ))
                .toList(),
            "count", store.getAuthUsers().size()
        ));
    }

    /**
     * Health check
     */
    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> healthCheck() {
        return ResponseEntity.ok(Map.of(
            "status", "UP",
            "mode", "mock",
            "firebase_enabled", false,
            "registered_users", store.getAuthUsers().size()
        ));
    }

    /**
     * Return current user info + profile if available (mock mode). For now token not validated; in mock mode we trust provided email.
     */
    @GetMapping("/me")
    public ResponseEntity<?> me(@RequestParam(value = "email", required = false) String email,
                                @RequestHeader(value = "Authorization", required = false) String authHeader) {
        // If Authorization: Bearer <token> present, resolve email from token registry
        if ((email == null || email.isBlank()) && authHeader != null && authHeader.startsWith("Bearer ")) {
            String token = authHeader.substring("Bearer ".length()).trim();
            String resolved = TOKEN_REGISTRY.get(token);
            if (resolved != null) {
                email = resolved;
                log.debug("[MockAuth] Resolved email '{}' from bearer token", email);
            }
        }
        if (email == null || email.isBlank()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
                SUCCESS_KEY, false,
                MESSAGE_KEY, "Email not provided and token not resolvable"
            ));
        }
        MockDataStore.MockUserAuth user = store.getAuthUsers().get(email);
        if (user == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
                SUCCESS_KEY, false,
                MESSAGE_KEY, "User not found: " + email
            ));
        }
        Map<String, Object> profile = Map.of();
        if (store.getStudentsByEmail().containsKey(email)) {
            String studentId = store.getStudentsByEmail().get(email).getId();
            profile = store.getProfiles().getOrDefault(studentId, Map.of());
        }
        return ResponseEntity.ok(Map.of(
            SUCCESS_KEY, true,
            "user", Map.of(
                "id", user.getId(),
                "email", user.getEmail(),
                "name", user.getName()
            ),
            "profile", profile
        ));
    }

    // DTOs
    public static class RegisterRequest {
        private String email;
        private String password;
        private String name;

        public RegisterRequest() {}

        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }

        public String getPassword() { return password; }
        public void setPassword(String password) { this.password = password; }

        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
    }

    // Removed legacy inner MockUser (replaced by MockDataStore.MockUserAuth)
}