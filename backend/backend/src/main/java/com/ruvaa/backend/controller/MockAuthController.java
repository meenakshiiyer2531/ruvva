package com.ruvaa.backend.controller;

import com.ruvaa.backend.dto.LoginRequest;
import com.ruvaa.backend.dto.LoginResponse;
import com.ruvaa.backend.dto.UserDto;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import java.time.LocalDateTime;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

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

    // Simple in-memory user storage for testing
    private final Map<String, MockUser> users = new ConcurrentHashMap<>();

    /**
     * Register a new user (mock implementation)
     */
    @PostMapping("/register")
    public ResponseEntity<?> register(@Valid @RequestBody RegisterRequest request) {
        try {
            log.info("Mock registration request for email: {}", request.getEmail());

            // Check if user already exists
            if (users.containsKey(request.getEmail())) {
                return ResponseEntity.badRequest().body(Map.of(
                    "success", false,
                    "message", "User already exists with email: " + request.getEmail()
                ));
            }

            // Create mock user
            MockUser user = new MockUser(
                String.valueOf(System.currentTimeMillis()),
                request.getEmail(),
                request.getPassword(), // In real app, this would be hashed
                request.getName(),
                LocalDateTime.now()
            );

            users.put(request.getEmail(), user);

            UserDto userDto = UserDto.builder()
                .id(user.getId())
                .email(user.getEmail())
                .name(user.getName())
                .build();

            log.info("Mock user registered successfully: {}", request.getEmail());

            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "User registered successfully",
                "user", userDto
            ));

        } catch (Exception e) {
            log.error("Mock registration failed", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                "success", false,
                "message", "Registration failed: " + e.getMessage()
            ));
        }
    }

    /**
     * Login user (mock implementation)
     */
    @PostMapping("/login")
    public ResponseEntity<?> login(@Valid @RequestBody LoginRequest request) {
        try {
            log.info("Mock login attempt for: {}", request.getUsername());

            MockUser user = users.get(request.getUsername());
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
                    "success", false,
                    "message", "User not found: " + request.getUsername()
                ));
            }

            // Simple password check (in real app, use proper password hashing)
            if (!user.getPassword().equals(request.getPassword())) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
                    "success", false,
                    "message", "Invalid password"
                ));
            }

            // Generate mock token
            String mockToken = "mock-jwt-token-" + System.currentTimeMillis();

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

            log.info("Mock login successful for: {}", request.getUsername());

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            log.error("Mock login failed", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                "success", false,
                "message", "Login failed: " + e.getMessage()
            ));
        }
    }

    /**
     * Get all registered users (for testing)
     */
    @GetMapping("/users")
    public ResponseEntity<Map<String, Object>> getUsers() {
        return ResponseEntity.ok(Map.of(
            "success", true,
            "users", users.values().stream()
                .map(user -> Map.of(
                    "id", user.getId(),
                    "email", user.getEmail(),
                    "name", user.getName(),
                    "createdAt", user.getCreatedAt()
                ))
                .toList(),
            "count", users.size()
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
            "registered_users", users.size()
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

    public static class MockUser {
        private String id;
        private String email;
        private String password;
        private String name;
        private LocalDateTime createdAt;

        public MockUser(String id, String email, String password, String name, LocalDateTime createdAt) {
            this.id = id;
            this.email = email;
            this.password = password;
            this.name = name;
            this.createdAt = createdAt;
        }

        public String getId() { return id; }
        public String getEmail() { return email; }
        public String getPassword() { return password; }
        public String getName() { return name; }
        public LocalDateTime getCreatedAt() { return createdAt; }
    }
}