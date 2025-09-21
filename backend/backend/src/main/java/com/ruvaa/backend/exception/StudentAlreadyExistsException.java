package com.ruvaa.backend.exception;

/**
 * Exception thrown when attempting to register a student that already exists
 */
public class StudentAlreadyExistsException extends RuntimeException {
    
    public StudentAlreadyExistsException(String message) {
        super(message);
    }
    
    public StudentAlreadyExistsException(String message, Throwable cause) {
        super(message, cause);
    }
}