package com.ruvaa.backend.controller;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(properties = {
        "firebase.enabled=false"
})
@AutoConfigureMockMvc
class MockStudentControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    @DisplayName("Should register student in mock mode and return token")
    void registerStudentMockMode() throws Exception {
        String payload = """
                {
                  "email": "test.student@example.com",
                  "name": "Test Student",
                  "gradeLevel": "10",
                  "password": "abc12345"
                }
                """;

        mockMvc.perform(post("/students/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content(payload)
                .header("Origin", "http://localhost:3000"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.success").value(true))
                .andExpect(jsonPath("$.data.email").value("test.student@example.com"))
                .andExpect(jsonPath("$.data.token").exists());
    }

    @Test
    @DisplayName("CORS preflight should succeed for allowed origin")
    void corsPreflightAllowedOrigin() throws Exception {
        mockMvc.perform(options("/students/register")
                .header("Origin", "http://localhost:3000")
                .header("Access-Control-Request-Method", "POST")
                .header("Access-Control-Request-Headers", "Content-Type"))
                .andExpect(status().isOk())
                .andExpect(header().exists("Access-Control-Allow-Origin"))
                .andExpect(header().string("Access-Control-Allow-Origin", "http://localhost:3000"));
    }
}
