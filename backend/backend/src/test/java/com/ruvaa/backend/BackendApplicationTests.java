package com.ruvaa.backend;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest(classes = CareerConnectApplication.class, properties = {"firebase.enabled=false"})
class BackendApplicationTests {

	@Test
	void contextLoads() {
	}

}
