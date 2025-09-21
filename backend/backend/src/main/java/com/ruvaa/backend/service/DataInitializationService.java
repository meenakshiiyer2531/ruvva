package com.ruvaa.backend.service;

import com.ruvaa.backend.entity.*;
import com.ruvaa.backend.repository.*;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class DataInitializationService implements CommandLineRunner {

    private final UserRepository userRepository;
    private final CareerRepository careerRepository;
    private final CollegeRepository collegeRepository;
    private final MentorRepository mentorRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) throws Exception {
        initializeUsers();
        initializeCareers();
        initializeColleges();
        initializeMentors();
    }

    private void initializeUsers() {
        if (userRepository.count() == 0) {
            User demoUser = new User();
            demoUser.setUsername("demo");
            demoUser.setPassword(passwordEncoder.encode("demo123"));
            demoUser.setName("Demo User");
            demoUser.setEmail("demo@ruvaa.com");
            demoUser.setLocation("Srinagar, J&K");
            userRepository.save(demoUser);
        }
    }

    private void initializeCareers() {
        if (careerRepository.count() == 0) {
            careerRepository.save(new Career(null, "Software Engineer", "👷‍♂️", 
                "Work on building and designing software applications, from web to mobile apps.", 
                "Programming, Problem-solving, Algorithms", "₹6-25 LPA", "High", "Technology"));

            careerRepository.save(new Career(null, "Doctor", "🩺", 
                "Provide medical care, heal patients, and save lives.", 
                "Medical Knowledge, Empathy, Critical Thinking", "₹8-50 LPA", "High", "Healthcare"));

            careerRepository.save(new Career(null, "Digital Artist", "🎨", 
                "Express creativity through digital painting, graphic design, or multimedia art.", 
                "Creativity, Design Software, Visual Arts", "₹3-15 LPA", "Medium", "Creative"));

            careerRepository.save(new Career(null, "Teacher", "📚", 
                "Educate and inspire students, shaping the future generation.", 
                "Communication, Subject Knowledge, Patience", "₹3-12 LPA", "Medium", "Education"));

            careerRepository.save(new Career(null, "Entrepreneur", "💼", 
                "Start and manage your own business, innovating in different industries.", 
                "Leadership, Innovation, Risk Management", "Varies", "High", "Business"));

            careerRepository.save(new Career(null, "Data Scientist", "🔬", 
                "Explore, research, and analyze data to understand patterns and make predictions.", 
                "Statistics, Programming, Machine Learning", "₹8-30 LPA", "Very High", "Technology"));
        }
    }

    private void initializeColleges() {
        if (collegeRepository.count() == 0) {
            collegeRepository.save(new College(null, "Govt College Srinagar", "Srinagar", 
                "BSc, BA, BCom", "www.gcsrinagar.edu.in", "0194-2123456", "Government", 
                "University of Kashmir", "Premier government college in Srinagar offering undergraduate programs.", 
                "12th pass with minimum 50% marks"));

            collegeRepository.save(new College(null, "Govt College Jammu", "Jammu", 
                "BCom, BCA, BBA", "www.gcjammu.edu.in", "0191-2345678", "Government", 
                "University of Jammu", "Government college known for commerce and computer applications.", 
                "12th pass with minimum 45% marks"));

            collegeRepository.save(new College(null, "Cluster University Srinagar", "Srinagar", 
                "BSc, BBA, BA, BTech", "www.cusrinagar.edu.in", "0194-3456789", "State University", 
                "Autonomous", "Multi-disciplinary university offering various undergraduate programs.", 
                "Merit-based admission through entrance test"));

            collegeRepository.save(new College(null, "GC Women College Jammu", "Jammu", 
                "BA, BCom, BSc", "www.gcwomenjammu.edu.in", "0191-4567890", "Government", 
                "University of Jammu", "Dedicated women's college providing quality education.", 
                "12th pass for women candidates"));

            collegeRepository.save(new College(null, "NIT Srinagar", "Srinagar", 
                "BTech, MTech, PhD", "www.nitsri.ac.in", "0194-2420500", "Institute of National Importance", 
                "Autonomous", "Premier technical institution offering engineering programs.", 
                "JEE Main qualification required"));
        }
    }

    private void initializeMentors() {
        if (mentorRepository.count() == 0) {
            mentorRepository.save(new Mentor(null, "Dr. Meenakshi Sharma", "Computer Science & AI", 
                "Learning through curiosity and practice", 
                "PhD in Computer Science with 15 years of industry experience in AI and Machine Learning.", 
                "15 years", "PhD Computer Science, IIT Delhi", "meenakshi@ruvaa.com", 4.8, 2000.0, 
                "Mon-Fri 10AM-6PM"));

            mentorRepository.save(new Mentor(null, "Mr. Rajesh Kumar", "Business & Entrepreneurship", 
                "Focus on problem-solving and creativity", 
                "Serial entrepreneur who has founded 3 successful startups in the technology sector.", 
                "12 years", "MBA from IIM Bangalore", "rajesh@ruvaa.com", 4.6, 2500.0, 
                "Tue-Thu 2PM-8PM, Sat 10AM-4PM"));

            mentorRepository.save(new Mentor(null, "Ms. Priya Kapoor", "Career Counselling & Psychology", 
                "Guidance with patience and empathy", 
                "Licensed clinical psychologist specializing in career counselling and student mentorship.", 
                "10 years", "MSc Psychology, PhD in Counselling", "priya@ruvaa.com", 4.9, 1800.0, 
                "Mon-Wed-Fri 9AM-5PM"));

            mentorRepository.save(new Mentor(null, "Dr. Amit Singh", "Engineering & Technology", 
                "Innovation through systematic learning", 
                "Former ISRO scientist with expertise in aerospace engineering and project management.", 
                "18 years", "PhD Aerospace Engineering", "amit@ruvaa.com", 4.7, 2200.0, 
                "Weekends 10AM-6PM"));
        }
    }
}