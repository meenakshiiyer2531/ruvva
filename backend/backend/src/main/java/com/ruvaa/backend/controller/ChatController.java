package com.ruvaa.backend.controller;

import com.ruvaa.backend.dto.ChatRequest;
import com.ruvaa.backend.dto.ChatResponse;
import com.ruvaa.backend.dto.SimpleChatResponse;
import com.ruvaa.backend.entity.ChatMessage;
import com.ruvaa.backend.entity.User;
import com.ruvaa.backend.repository.ChatMessageRepository;
import com.ruvaa.backend.repository.UserRepository;
import com.ruvaa.backend.service.AIService;
import com.ruvaa.backend.service.FirebaseUserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@RestController
@RequestMapping("/chat")
@RequiredArgsConstructor
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "true", matchIfMissing = false)
@CrossOrigin(origins = "*")
public class ChatController {

    private final ChatMessageRepository chatMessageRepository;
    private final UserRepository userRepository;
    private final AIService aiService;
    private final FirebaseUserService firebaseUserService;

    @PostMapping("/message")
    public ResponseEntity<SimpleChatResponse> sendMessage(@Valid @RequestBody ChatRequest request,
                                                   Authentication authentication) {
        try {
            String username = authentication != null ? authentication.getName() : "anonymous";

            String aiResponse;
            try {
                aiResponse = aiService.generateResponse(request.getMessage());
            } catch (Exception e) {
                aiResponse = "Thanks for your message: \"" + request.getMessage() + "\". I'm here to help with your career questions. Could you tell me more about your interests or goals?";
            }

            // Save to both Firebase and local DB for redundancy
            if (authentication != null && !"anonymous".equals(username)) {
                // Save to Firebase
                try {
                    firebaseUserService.saveChatMessage(username, request.getMessage(), aiResponse);
                    log.debug("Chat saved to Firebase for user: {}", username);
                } catch (Exception e) {
                    log.warn("Failed to save chat to Firebase: {}", e.getMessage());
                }

                // Save to local DB as backup
                try {
                    User user = userRepository.findByUsername(username).orElse(null);
                    if (user != null) {
                        ChatMessage userMessage = new ChatMessage();
                        userMessage.setUser(user);
                        userMessage.setMessage(request.getMessage());
                        userMessage.setIsFromUser(true);
                        chatMessageRepository.save(userMessage);

                        ChatMessage botMessage = new ChatMessage();
                        botMessage.setUser(user);
                        botMessage.setMessage(aiResponse);
                        botMessage.setIsFromUser(false);
                        botMessage.setResponse(aiResponse);
                        chatMessageRepository.save(botMessage);
                    }
                } catch (Exception e) {
                    log.warn("Failed to save chat to local DB: {}", e.getMessage());
                }
            }

            return ResponseEntity.ok(new SimpleChatResponse(aiResponse));
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping("/history")
    public ResponseEntity<List<ChatResponse>> getChatHistory(Authentication authentication,
                                                           @RequestParam(defaultValue = "20") int limit) {
        try {
            String username = authentication.getName();

            // Try to get from Firebase first
            try {
                if (firebaseUserService.isFirestoreHealthy()) {
                    List<Map<String, Object>> firebaseHistory = firebaseUserService.getChatHistory(username, limit);

                    List<ChatResponse> responses = firebaseHistory.stream()
                            .map(chatData -> {
                                String userMessage = (String) chatData.get("userMessage");
                                String aiResponse = (String) chatData.get("aiResponse");
                                Object timestampObj = chatData.get("timestamp");

                                LocalDateTime timestamp = LocalDateTime.now();
                                try {
                                    if (timestampObj != null) {
                                        timestamp = Instant.parse(timestampObj.toString()).atZone(java.time.ZoneOffset.UTC).toLocalDateTime();
                                    }
                                } catch (Exception e) {
                                    log.debug("Could not parse timestamp from Firebase: {}", timestampObj);
                                }

                                return new ChatResponse(userMessage, aiResponse, false, timestamp);
                            })
                            .collect(Collectors.toList());

                    if (!responses.isEmpty()) {
                        log.debug("Retrieved {} chat messages from Firebase for user: {}", responses.size(), username);
                        return ResponseEntity.ok(responses);
                    }
                }
            } catch (Exception e) {
                log.warn("Failed to get chat history from Firebase: {}", e.getMessage());
            }

            // Fallback to local database
            try {
                User user = userRepository.findByUsername(username)
                        .orElseThrow(() -> new RuntimeException("User not found"));

                List<ChatMessage> messages = chatMessageRepository.findByUserOrderByCreatedAtAsc(user);

                List<ChatResponse> responses = messages.stream()
                        .map(msg -> new ChatResponse(
                                msg.getMessage(),
                                msg.getResponse(),
                                msg.getIsFromUser(),
                                msg.getCreatedAt()
                        ))
                        .collect(Collectors.toList());

                log.debug("Retrieved {} chat messages from local DB for user: {}", responses.size(), username);
                return ResponseEntity.ok(responses);
            } catch (Exception e) {
                log.error("Failed to get chat history from local DB: {}", e.getMessage());
                return ResponseEntity.ok(java.util.Collections.emptyList());
            }
        } catch (Exception e) {
            log.error("Chat history request failed: {}", e.getMessage());
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> healthCheck() {
        Map<String, Object> health = new HashMap<>();
        health.put("status", "UP");
        health.put("firebase_db", firebaseUserService.isFirestoreHealthy());
        health.put("ai_service", aiService.isPythonAIServiceAvailable());
        return ResponseEntity.ok(health);
    }
}