package com.ruvaa.backend.service;

import com.ruvaa.backend.dto.LoginRequest;
import com.ruvaa.backend.dto.LoginResponse;
import com.ruvaa.backend.dto.UserDto;

import com.ruvaa.backend.entity.User;
import com.ruvaa.backend.model.entity.Student;
import com.ruvaa.backend.repository.UserRepository;
import com.ruvaa.backend.service.StudentService;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
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
    private final StudentService studentService; // Inject StudentService
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;
    private final AuthenticationManager authenticationManager;

    public LoginResponse login(LoginRequest request) {
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword())
        );

        Student student = studentService.findByEmail(request.getEmail())
                .orElseThrow(() -> new RuntimeException("Student not found"));

        String token = jwtUtil.generateToken(student);

        UserDto userDto = UserDto.builder()
                .id(student.getId())
                .username(student.getEmail())
                .name(student.getFullName())
                .email(student.getEmail())
                .phone(student.getPhoneNumber())
                .age(student.getAge())
                .location(student.getCity() + ", " + student.getState())
                .education(student.getEducationLevel() != null ? student.getEducationLevel().getDisplayName() : null)
                .interests(String.join(", ", student.getInterestedDomains()))
                .createdAt(student.getCreatedAt() != null ? LocalDateTime.ofInstant(student.getCreatedAt().toDate().toInstant(), ZoneOffset.UTC) : null)
                .build();

        return new LoginResponse(token, "Bearer", userDto);
    }

    public LoginResponse mockLogin(LoginRequest request) {
        if (request.getEmail() == null || request.getEmail().trim().isEmpty() ||
            request.getPassword() == null || request.getPassword().trim().isEmpty()) {
            throw new RuntimeException("Email and password are required");
        }

        User mockUser = new User();
        mockUser.setId(System.currentTimeMillis());
        mockUser.setUsername(request.getEmail());
        mockUser.setName(request.getEmail());
        mockUser.setEmail(request.getEmail() + "@example.com");
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