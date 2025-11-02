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
class MockStudentProfileCrudControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

        @SuppressWarnings("unused") // parameter used in payload assembly; suppress static analyzer false positive
        private String registerStudent(String email) throws Exception {
        String payload = """
                {
                  \"email\": \"" + email + "\",
                  \"fullName\": \"CRUD Student\",
                  \"password\": \"abc12345\"
                }
                """;
        MvcResult result = mockMvc.perform(post("/students/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(payload))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.success").value(true))
                .andReturn();
        JsonNode json = objectMapper.readTree(result.getResponse().getContentAsString());
        return json.path("data").path("id").asText();
    }

    @Test
    @DisplayName("Profile create should succeed then conflict on second create")
    void profileCreateConflict() throws Exception {
        String studentId = registerStudent("crud.create@example.com");
        assertThat(studentId).isNotBlank();

        String createPayload = """
                { "focus": "engineering", "years": 2 }
                """;
        mockMvc.perform(post("/students/" + studentId + "/profile")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(createPayload))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.data.profile.focus").value("engineering"));

        mockMvc.perform(post("/students/" + studentId + "/profile")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(createPayload))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.success").value(false));
    }

    @Test
    @DisplayName("Patch should merge new fields while preserving existing ones")
    void patchMergeProfile() throws Exception {
        String studentId = registerStudent("crud.patch@example.com");
        assertThat(studentId).isNotBlank();

        String initial = """
                { "interest": "math", "goal": "scientist" }
                """;
        mockMvc.perform(put("/students/" + studentId + "/profile")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(initial))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.data.profile.goal").value("scientist"));

        String patch = """
                { "goal": "researcher", "skillLevel": "beginner" }
                """;
        mockMvc.perform(patch("/students/" + studentId + "/profile")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(patch))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.data.profile.goal").value("researcher"))
                .andExpect(jsonPath("$.data.profile.interest").value("math"))
                .andExpect(jsonPath("$.data.profile.skillLevel").value("beginner"));
    }

    @Test
    @DisplayName("Delete should remove profile and subsequent get shows empty profile")
    void deleteProfile() throws Exception {
        String studentId = registerStudent("crud.delete@example.com");
        assertThat(studentId).isNotBlank();

        String initial = """
                { "path": "engineering" }
                """;
        mockMvc.perform(put("/students/" + studentId + "/profile")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(initial))
                .andExpect(status().isOk());

        mockMvc.perform(delete("/students/" + studentId + "/profile"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").value("Profile deleted (mock mode)"));

        mockMvc.perform(get("/students/" + studentId + "//profile"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.data.profile").isMap())
                .andExpect(jsonPath("$.data.profile.path").doesNotExist());
    }

    @Test
    @DisplayName("Profiles list includes created profile with student basic data")
    void listProfiles() throws Exception {
        String studentId = registerStudent("crud.list@example.com");
        assertThat(studentId).isNotBlank();
        mockMvc.perform(put("/students/" + studentId + "/profile")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{ \"focus\": \"design\" }"))
                .andExpect(status().isOk());

        mockMvc.perform(get("/students/profiles"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.data[0].id").isNotEmpty())
                .andExpect(jsonPath("$.data[0].profile.focus").value("design"));
    }
}
