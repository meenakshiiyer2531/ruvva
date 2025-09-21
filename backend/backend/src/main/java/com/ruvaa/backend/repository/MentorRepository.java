package com.ruvaa.backend.repository;

import com.ruvaa.backend.entity.Mentor;
import java.util.List;
import java.util.Optional;

public interface MentorRepository {
    List<Mentor> findBySpecialization(String specialization);
    List<Mentor> findByRatingGreaterThanEqual(Double rating);
    Mentor save(Mentor mentor);
    Optional<Mentor> findById(Long id);
    void deleteById(Long id);
    List<Mentor> findAll();
    long count();
}