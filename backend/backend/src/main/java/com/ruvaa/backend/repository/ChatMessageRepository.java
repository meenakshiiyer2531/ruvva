package com.ruvaa.backend.repository;

import com.ruvaa.backend.entity.ChatMessage;
import com.ruvaa.backend.entity.User;
import java.util.List;
import java.util.Optional;

public interface ChatMessageRepository {
    List<ChatMessage> findByUserOrderByCreatedAtAsc(User user);
    List<ChatMessage> findTop20ByUserOrderByCreatedAtDesc(User user);
    ChatMessage save(ChatMessage chatMessage);
    Optional<ChatMessage> findById(Long id);
    void deleteById(Long id);
}