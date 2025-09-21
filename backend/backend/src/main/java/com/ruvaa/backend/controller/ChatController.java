package com.ruvaa.backend.controller;

import com.ruvaa.backend.dto.ChatRequest;
import com.ruvaa.backend.dto.ChatResponse;
import com.ruvaa.backend.entity.ChatMessage;
import com.ruvaa.backend.entity.User;
import com.ruvaa.backend.repository.ChatMessageRepository;
import com.ruvaa.backend.repository.UserRepository;
import com.ruvaa.backend.service.AIService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/chat")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class ChatController {

    private final ChatMessageRepository chatMessageRepository;
    private final UserRepository userRepository;
    private final AIService aiService;

    @PostMapping("/message")
    public ResponseEntity<ChatResponse> sendMessage(@Valid @RequestBody ChatRequest request, 
                                                   Authentication authentication) {
        try {
            User user = userRepository.findByUsername(authentication.getName())
                    .orElseThrow(() -> new RuntimeException("User not found"));

            ChatMessage userMessage = new ChatMessage();
            userMessage.setUser(user);
            userMessage.setMessage(request.getMessage());
            userMessage.setIsFromUser(true);
            chatMessageRepository.save(userMessage);

            String aiResponse = aiService.generateResponse(request.getMessage());

            ChatMessage botMessage = new ChatMessage();
            botMessage.setUser(user);
            botMessage.setMessage(aiResponse);
            botMessage.setIsFromUser(false);
            botMessage.setResponse(aiResponse);
            chatMessageRepository.save(botMessage);

            return ResponseEntity.ok(new ChatResponse(
                    request.getMessage(),
                    aiResponse,
                    false,
                    LocalDateTime.now()
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping("/history")
    public ResponseEntity<List<ChatResponse>> getChatHistory(Authentication authentication) {
        try {
            User user = userRepository.findByUsername(authentication.getName())
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

            return ResponseEntity.ok(responses);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }
}