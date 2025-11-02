package com.ruvaa.backend.controller;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(properties = {
        "firebase.enabled=false"
})
@AutoConfigureMockMvc
class MockStudentProfileControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    @DisplayName("Should create and then update/retrieve student profile in mock mode")
    void updateAndRetrieveProfile() throws Exception {
        // 1. Register a new mock student
        String registerPayload = """
                {
                  "email": "profile.student@example.com",
                  "fullName": "Profile Student",
                  "password": "abc12345"
                }
                """;

        MvcResult regResult = mockMvc.perform(post("/students/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(registerPayload))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.success").value(true))
                .andReturn();

        JsonNode regJson = objectMapper.readTree(regResult.getResponse().getContentAsString());
        String studentId = regJson.path("data").path("id").asText();
        assertThat(studentId).isNotBlank();

        // 2. PUT profile update
        String profilePayload = """
                {
                  "interests": ["math", "science"],
                  "goals": "Become an engineer",
                  "availability": "weekends"
                }
                """;

        mockMvc.perform(put("/students/" + studentId + "/profile")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(profilePayload))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.success").value(true))
                .andExpect(jsonPath("$.data.profile.goals").value("Become an engineer"))
                .andExpect(jsonPath("$.data.profile.interests[0]").value("math"));

        // 3. GET profile retrieve
        mockMvc.perform(get("/students/" + studentId + "/profile"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.success").value(true))
                .andExpect(jsonPath("$.data.id").value(studentId))
                .andExpect(jsonPath("$.data.profile.goals").value("Become an engineer"));
    }
}
