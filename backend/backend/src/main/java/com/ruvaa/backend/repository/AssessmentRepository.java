package com.ruvaa.backend.repository;

import com.ruvaa.backend.entity.Assessment;
import com.ruvaa.backend.entity.User;
import java.util.List;
import java.util.Optional;

public interface AssessmentRepository {
    List<Assessment> findByUserOrderByCreatedAtDesc(User user);
    Optional<Assessment> findFirstByUserOrderByCreatedAtDesc(User user);
    Assessment save(Assessment assessment);
    Optional<Assessment> findById(Long id);
    void deleteById(Long id);
}