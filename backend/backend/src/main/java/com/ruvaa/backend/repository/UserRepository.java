package com.ruvaa.backend.repository;

import com.ruvaa.backend.entity.User;
import java.util.Optional;

public interface UserRepository {
    Optional<User> findByUsername(String username);
    boolean existsByUsername(String username);
    boolean existsByEmail(String email);
    User save(User user);
    Optional<User> findById(Long id);
    void deleteById(Long id);
    long count();
}