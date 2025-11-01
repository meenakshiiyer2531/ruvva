package com.ruvaa.backend.controller;

import com.google.firebase.auth.FirebaseAuthException;
import com.ruvaa.backend.dto.LoginRequest;
import com.ruvaa.backend.dto.LoginResponse;
import com.ruvaa.backend.dto.UserDto;
import com.ruvaa.backend.entity.User;
import com.ruvaa.backend.service.AuthService;
import com.ruvaa.backend.service.FirebaseAuthService;
import com.ruvaa.backend.service.FirebaseUserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "true", matchIfMissing = false)
public class AuthController {

    private final AuthService authService;
    private final FirebaseAuthService firebaseAuthService;
    private final FirebaseUserService firebaseUserService;

    @PostMapping("/login")
    public ResponseEntity<LoginResponse> login(@Valid @RequestBody LoginRequest request) {
        try {
            // Try Firebase authentication first
            if (firebaseAuthService.isFirebaseAuthAvailable()) {
                return loginWithFirebase(request);
            } else {
                log.warn("Firebase not available, falling back to mock authentication");
                LoginResponse response = authService.mockLogin(request);
                return ResponseEntity.ok(response);
            }
        } catch (Exception e) {
            log.error("Login failed: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
    }

    @PostMapping("/firebase-login")
    public ResponseEntity<LoginResponse> firebaseLogin(@RequestBody Map<String, String> request) {
        try {
            String idToken = request.get("idToken");
            if (idToken == null || idToken.trim().isEmpty()) {
                return ResponseEntity.badRequest().build();
            }

            var firebaseToken = firebaseAuthService.verifyIdToken(idToken);
            var userRecord = firebaseAuthService.getUserRecord(firebaseToken.getUid());

            // Update last login
            firebaseUserService.updateLastLogin(firebaseToken.getUid());

            LoginResponse response = LoginResponse.builder()
                    .token(idToken) // Use Firebase token directly
                    .user(UserDto.builder()
                            .id(firebaseToken.getUid())
                            .email(userRecord.getEmail())
                            .name(userRecord.getDisplayName())
                            .build())
                    .build();

            return ResponseEntity.ok(response);
        } catch (FirebaseAuthException e) {
            log.error("Firebase authentication failed: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        } catch (Exception e) {
            log.error("Login failed: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    private ResponseEntity<LoginResponse> loginWithFirebase(LoginRequest request) {
        try {
            LoginResponse response = authService.login(request);
            // Try to create/update user document in Firebase
            try {
                firebaseUserService.createUserDocument(
                    response.getUser().getId(),
                    response.getUser().getEmail(),
                    response.getUser().getName()
                );
            } catch (Exception e) {
                log.warn("Failed to create Firebase user document, continuing with mock auth: {}", e.getMessage());
            }

            return ResponseEntity.ok(response);
        } catch (Exception e) {
            throw e;
        }
    }

    @PostMapping("/register")
    public ResponseEntity<UserDto> register(@RequestBody User user) {
        try {
            // Try Firebase registration if available
            if (firebaseAuthService.isFirebaseAuthAvailable()) {
                return registerWithFirebase(user);
            } else {
                log.warn("Firebase not available, falling back to mock registration");
                UserDto userDto = authService.register(user);
                return ResponseEntity.ok(userDto);
            }
        } catch (Exception e) {
            log.error("Registration failed: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        }
    }

    @PostMapping("/firebase-register")
    public ResponseEntity<UserDto> firebaseRegister(@RequestBody Map<String, String> request) {
        try {
            String email = request.get("email");
            String password = request.get("password");
            String displayName = request.get("displayName");

            if (email == null || password == null) {
                return ResponseEntity.badRequest().build();
            }

            var userRecord = firebaseAuthService.createUser(email, password, displayName);

            // Create user document in Firestore
            firebaseUserService.createUserDocument(userRecord.getUid(), email, displayName);

            UserDto userDto = UserDto.builder()
                    .id(userRecord.getUid())
                    .email(userRecord.getEmail())
                    .name(userRecord.getDisplayName())
                    .build();

            return ResponseEntity.ok(userDto);
        } catch (FirebaseAuthException e) {
            log.error("Firebase registration failed: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        } catch (Exception e) {
            log.error("Registration failed: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    private ResponseEntity<UserDto> registerWithFirebase(User user) {
        // For MVP, use mock registration but create Firebase document
        try {
            UserDto userDto = authService.register(user);

            // Try to create user document in Firebase
            try {
                firebaseUserService.createUserDocument(
                    userDto.getId(),
                    userDto.getEmail(),
                    userDto.getName()
                );
            } catch (Exception e) {
                log.warn("Failed to create Firebase user document, continuing with mock registration: {}", e.getMessage());
            }

            return ResponseEntity.ok(userDto);
        } catch (Exception e) {
            throw e;
        }
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> healthCheck() {
        Map<String, Object> health = Map.of(
            "status", "UP",
            "firebase_auth", firebaseAuthService.isFirebaseAuthAvailable(),
            "firebase_db", firebaseUserService.isFirestoreHealthy()
        );
        return ResponseEntity.ok(health);
    }
}