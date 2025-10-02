package com.ruvaa.backend.service;

import com.ruvaa.backend.dto.LoginRequest;
import com.ruvaa.backend.dto.LoginResponse;
import com.ruvaa.backend.dto.UserDto;
import com.ruvaa.backend.entity.User;
import com.ruvaa.backend.repository.UserRepository;
import com.ruvaa.backend.security.JwtUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "true", matchIfMissing = false)
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;
    private final AuthenticationManager authenticationManager;

    public LoginResponse login(LoginRequest request) {
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getUsername(), request.getPassword())
        );

        User user = userRepository.findByUsername(request.getUsername())
                .orElseThrow(() -> new RuntimeException("User not found"));

        String token = jwtUtil.generateToken(user);

        UserDto userDto = convertToDto(user);

        return new LoginResponse(token, "Bearer", userDto);
    }

    public LoginResponse mockLogin(LoginRequest request) {
        if (request.getUsername() == null || request.getUsername().trim().isEmpty() ||
            request.getPassword() == null || request.getPassword().trim().isEmpty()) {
            throw new RuntimeException("Username and password are required");
        }

        User mockUser = new User();
        mockUser.setId(System.currentTimeMillis());
        mockUser.setUsername(request.getUsername());
        mockUser.setName(request.getUsername());
        mockUser.setEmail(request.getUsername() + "@example.com");
        mockUser.onCreate();

        String mockToken = "mock-jwt-token-" + System.currentTimeMillis();

        UserDto userDto = convertToDto(mockUser);

        return new LoginResponse(mockToken, "Bearer", userDto);
    }

    public UserDto register(User user) {
        if (userRepository.existsByUsername(user.getUsername())) {
            throw new RuntimeException("Username already exists");
        }

        user.setPassword(passwordEncoder.encode(user.getPassword()));
        User savedUser = userRepository.save(user);
        return convertToDto(savedUser);
    }

    private UserDto convertToDto(User user) {
        UserDto dto = new UserDto();
        dto.setId(user.getId() != null ? user.getId().toString() : null);
        dto.setUsername(user.getUsername());
        dto.setName(user.getName());
        dto.setEmail(user.getEmail());
        dto.setPhone(user.getPhone());
        dto.setAge(user.getAge());
        dto.setLocation(user.getLocation());
        dto.setEducation(user.getEducation());
        dto.setInterests(user.getInterests());
        dto.setCreatedAt(user.getCreatedAt());
        return dto;
    }
}