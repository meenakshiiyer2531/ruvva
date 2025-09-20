export const careers = [
  {
    id: "c1",
    title: "Software Engineer",
    tags: ["Programming", "Computer Science", "Technology"],
    desc: "Designs, develops, and maintains software applications and systems. They write code, test software, and collaborate on project teams.",
    scoreMatch: 0.95,
    learningPath: [
      { step: "Learn programming basics (e.g., Python, JavaScript)", resources: ["https://www.freecodecamp.org/", "https://www.theodinproject.com/", "https://www.coursera.org/courses?query=python%20for%20everybody", "https://www.codecademy.com/"] },
      { step: "Master Data Structures & Algorithms", resources: ["https://www.geeksforgeeks.org/data-structures/", "https://leetcode.com/", "https://www.coursera.org/courses?query=algorithms%20and%20data%20structures", "https://www.udemy.com/topic/data-structures-and-algorithms/"] },
      { step: "Build a portfolio with personal projects", resources: ["https://github.com/", "https://www.freecodecamp.org/news/how-to-build-a-great-portfolio-as-a-developer-without-any-experience/", "https://dev.to/"] },
      { step: "Specialize in a domain (e.g., front-end, back-end, mobile)", resources: ["https://roadmap.sh/", "https://www.frontendmentor.io/", "https://nodejs.org/en/", "https://react.dev/", "https://www.tensorflow.org/"] }
    ]
  },
  {
    id: "c2",
    title: "Data Scientist",
    tags: ["Data", "Analytics", "AI", "Statistics", "Technology"],
    desc: "Analyzes and interprets complex data to help organizations make better decisions. They use statistical methods and machine learning.",
    scoreMatch: 0.92,
    learningPath: [
      { step: "Learn statistics and probability", resources: ["https://www.coursera.org/courses?query=introduction%20to%20statistics", "https://www.khanacademy.org/math/statistics-probability", "https://www.edx.org/learn/statistics"] },
      { step: "Master programming languages for data (Python, R)", resources: ["https://www.coursera.org/courses?query=python%20for%20data%20science", "https://www.datacamp.com/", "https://www.r-project.org/"] },
      { step: "Learn machine learning and deep learning", resources: ["https://www.coursera.org/courses?query=machine%20learning%20specialization", "https://scikit-learn.org/stable/", "https://www.tensorflow.org/", "https://pytorch.org/"] },
      { step: "Work on data science projects and competitions", resources: ["https://www.kaggle.com/", "https://www.linkedin.com/pulse/how-start-your-data-science-portfolio-projects-prashant-goyal/"] }
    ]
  },
  {
    id: "c3",
    title: "UX/UI Designer",
    tags: ["Design", "User Experience", "Creativity", "Technology"],
    desc: "Focuses on the user experience (UX) and user interface (UI) of digital products. They create intuitive, accessible, and enjoyable designs.",
    scoreMatch: 0.88,
    learningPath: [
      { step: "Understand design principles and user psychology", resources: ["https://www.nngroup.com/articles/usability-101-introduction-to-usability/", "https://www.interaction-design.org/literature/topics/usability-101", "https://www.coursera.org/specializations/google-ux-design"] },
      { step: "Learn design tools (Figma, Adobe XD)", resources: ["https://www.figma.com/learn/", "https://www.adobe.com/products/xd/tutorials.html", "https://www.skillshare.com/"] },
      { step: "Practice user research and prototyping", resources: ["https://www.invisionapp.com/inside-design/user-research-guide/", "https://www.usability.gov/what-and-why/user-research.html"] },
      { step: "Build a portfolio with case studies", resources: ["https://www.behance.net/", "https://dribbble.com/", "https://www.uxfol.io/"] }
    ]
  },
  {
    id: "c4",
    title: "Cloud Architect",
    tags: ["Cloud", "IT", "Infrastructure", "Technology"],
    desc: "Designs and oversees an organization's cloud computing strategy. They are experts in platforms like AWS, Azure, and Google Cloud.",
    scoreMatch: 0.90,
    learningPath: [
      { step: "Master foundational IT concepts (networking, OS)", resources: ["https://www.comptia.org/certifications/network", "https://www.comptia.org/certifications/a"] },
      { step: "Learn a major cloud platform (AWS, Azure, GCP)", resources: ["https://aws.amazon.com/training/", "https://learn.microsoft.com/en-us/training/browse/", "https://cloud.google.com/training"] },
      { step: "Obtain professional certifications", resources: ["https://aws.amazon.com/certification/", "https://learn.microsoft.com/en-us/certifications/browse/", "https://cloud.google.com/certification"] },
      { step: "Gain hands-on experience with cloud projects", resources: ["https://acloudguru.com/", "https://www.qwiklabs.com/"] }
    ]
  },
  {
    id: "c5",
    title: "Product Manager",
    tags: ["Management", "Business", "Technology", "Strategy"],
    desc: "Defines the product vision and strategy. They coordinate teams (engineering, design, marketing) to bring a product to market.",
    scoreMatch: 0.85,
    learningPath: [
      { step: "Understand business and market fundamentals", resources: ["https://www.coursera.org/courses?query=business%20fundamentals", "https://www.hbs.edu/online/"] },
      { step: "Learn product management frameworks", resources: ["https://www.productplan.com/glossary/product-management-framework", "https://www.coursera.org/courses?query=product%20management"] },
      { step: "Develop strong communication and leadership skills", resources: ["https://www.edx.org/learn/leadership", "https://www.coursera.org/courses?query=communication%20skills"] },
      { step: "Practice through internships or entry-level roles", resources: ["https://www.productschool.com/blog/product-management-guide/getting-first-product-management-job"] }
    ]
  },
  {
    id: "c6",
    title: "Cybersecurity Analyst",
    tags: ["Cybersecurity", "IT", "Security", "Technology"],
    desc: "Protects computer systems and networks from cyber threats. They monitor for vulnerabilities and respond to security incidents.",
    scoreMatch: 0.91,
    learningPath: [
      { step: "Learn networking and operating systems", resources: ["https://www.comptia.org/certifications/a", "https://www.comptia.org/certifications/network"] },
      { step: "Understand cybersecurity fundamentals", resources: ["https://www.comptia.org/certifications/security", "https://www.cybrary.it/"] },
      { step: "Gain hands-on experience with security tools", resources: ["https://tryhackme.com/", "https://www.hackthebox.com/", "https://portswigger.net/burp"] },
      { step: "Obtain specialized certifications (e.g., CISSP, OSCP)", resources: ["https://www.isc2.org/Certifications/CISSP", "https://www.offensive-security.com/pwk-oscp/"] }
    ]
  },
  {
    id: "c7",
    title: "Machine Learning Engineer",
    tags: ["AI", "Programming", "Data", "Technology"],
    desc: "Builds and deploys machine learning models in production environments. This role combines data science and software engineering.",
    scoreMatch: 0.94,
    learningPath: [
      { step: "Master programming (Python) and data structures", resources: ["https://www.coursera.org/courses?query=python%20for%20everybody", "https://www.edx.org/learn/data-structures"] },
      { step: "Learn machine learning theory and algorithms", resources: ["https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops", "https://www.udemy.com/topic/machine-learning/"] },
      { step: "Familiarize yourself with ML frameworks (TensorFlow, PyTorch)", resources: ["https://www.tensorflow.org/tutorials", "https://pytorch.org/tutorials/"] },
      { step: "Practice building and deploying models", resources: ["https://www.kaggle.com/", "https://www.huggingface.co/"] }
    ]
  },
  {
    id: "c8",
    title: "DevOps Engineer",
    tags: ["DevOps", "IT", "Automation", "Technology"],
    desc: "Bridges the gap between software development and IT operations. They automate the processes of building, testing, and deploying code.",
    scoreMatch: 0.89,
    learningPath: [
      { step: "Learn Linux, networking, and shell scripting", resources: ["https://linuxjourney.com/", "https://www.comptia.org/certifications/linux", "https://www.shellscript.sh/"] },
      { step: "Master version control (Git) and CI/CD tools", resources: ["https://git-scm.com/doc", "https://jenkins.io/doc/", "https://docs.gitlab.com/"] },
      { step: "Learn containerization (Docker, Kubernetes)", resources: ["https://www.docker.com/get-started", "https://kubernetes.io/docs/"] },
      { step: "Understand cloud infrastructure (AWS, Azure, GCP)", resources: ["https://aws.amazon.com/training/", "https://learn.microsoft.com/en-us/training/browse/", "https://cloud.google.com/training"] }
    ]
  },
  {
    id: "c9",
    title: "Digital Marketing Manager",
    tags: ["Marketing", "Business", "Communication"],
    desc: "Develops, implements, and manages marketing campaigns that promote a company and its products or services.",
    scoreMatch: 0.82,
    learningPath: [
      { step: "Learn the fundamentals of marketing and SEO", resources: ["https://www.semrush.com/academy/", "https://www.hubspot.com/digital-marketing", "https://ahrefs.com/blog/seo-basics/"] },
      { step: "Master tools for analytics and advertising", resources: ["https://analytics.google.com/analytics/web/provision/#/provision", "https://ads.google.com/"] },
      { step: "Gain experience with social media and content marketing", resources: ["https://buffer.com/library/social-media-marketing/", "https://blog.hootsuite.com/social-media-marketing-strategy/"] },
      { step: "Build a portfolio by running small-scale campaigns", resources: ["https://www.udemy.com/topic/digital-marketing-portfolio/"] }
    ]
  },
  {
    id: "c10",
    title: "Financial Analyst",
    tags: ["Finance", "Business", "Data", "Analytics"],
    desc: "Analyzes financial data to help businesses and individuals make informed investment and financial decisions.",
    scoreMatch: 0.87,
    learningPath: [
      { step: "Understand accounting and financial principles", resources: ["https://www.coursera.org/learn/financial-markets", "https://www.edx.org/learn/finance"] },
      { step: "Master financial modeling and valuation", resources: ["https://www.wallstreetprep.com/", "https://corporatefinanceinstitute.com/"] },
      { step: "Learn data analysis tools (Excel, SQL, Python)", resources: ["https://www.microsoft.com/en-us/learning/excel-training.aspx", "https://www.w3schools.com/sql/", "https://www.coursera.org/courses?query=python%20for%20finance"] },
      { step: "Pursue certifications (e.g., CFA, FRM)", resources: ["https://www.cfainstitute.org/en/programs/cfa", "https://www.garp.org/frm"] }
    ]
  },
  {
    id: "c11",
    title: "Mechanical Engineer",
    tags: ["Engineering", "Design", "Physics", "Manufacturing"],
    desc: "Designs, analyzes, and manufactures mechanical systems, from small components to large plants and machinery.",
    scoreMatch: 0.86,
    learningPath: [
      { step: "Master core engineering concepts (physics, thermodynamics)", resources: ["https://www.khanacademy.org/science/physics", "https://ocw.mit.edu/courses/mechanical-engineering/"] },
      { step: "Learn CAD software (AutoCAD, SolidWorks)", resources: ["https://www.autodesk.com/education/free-software/autocad", "https://www.solidworks.com/"] },
      { step: "Gain hands-on experience through projects", resources: ["https://www.instructables.com/"] },
      { step: "Pursue an accredited bachelor's degree", resources: ["https://www.abet.org/accreditation/find-programs/"] }
    ]
  },
  {
    id: "c12",
    title: "Network Administrator",
    tags: ["IT", "Networking", "Systems", "Security"],
    desc: "Manages an organization's computer networks. They install, configure, and maintain network hardware and software.",
    scoreMatch: 0.85,
    learningPath: [
      { step: "Learn network fundamentals (TCP/IP, LAN/WAN)", resources: ["https://www.comptia.org/certifications/network", "https://www.cisco.com/c/en/us/training-events/training-certifications/certifications.html"] },
      { step: "Gain hands-on experience with hardware", resources: ["https://www.cisco.com/c/en/us/training-events/training-certifications/certifications/associate/ccna.html"] },
      { step: "Master operating systems (Windows Server, Linux)", resources: ["https://learn.microsoft.com/en-us/training/browse/", "https://linuxjourney.com/"] },
      { step: "Pursue certifications (e.g., CCNA, CompTIA Network+)", resources: ["https://www.cisco.com/c/en/us/training-events/training-certifications/certifications/associate/ccna.html", "https://www.comptia.org/certifications/network"] }
    ]
  },
  {
    id: "c13",
    title: "Content Creator",
    tags: ["Creativity", "Marketing", "Communication", "Media"],
    desc: "Produces and shares digital content (videos, blogs, podcasts) for an online audience, often specializing in a niche.",
    scoreMatch: 0.78,
    learningPath: [
      { step: "Define your niche and target audience", resources: ["https://www.socialmediaexaminer.com/how-to-find-your-niche-and-build-a-loyal-audience/", "https://www.forbes.com/sites/forbesagencycouncil/2021/08/25/defining-your-niche-how-to-build-a-strong-personal-brand/"] },
      { step: "Learn content production tools (editing, design)", resources: ["https://www.adobe.com/creativecloud/video.html", "https://www.canva.com/", "https://www.audacityteam.org/"] },
      { step: "Study SEO and social media algorithms", resources: ["https://www.semrush.com/academy/", "https://creator.youtube.com/"] },
      { step: "Start creating and publishing consistently", resources: ["https://www.youtube.com/", "https://medium.com/", "https://spotifyforpodcasters.spotify.com/"] }
    ]
  },
  {
    id: "c14",
    title: "Urban Planner",
    tags: ["Design", "Environment", "Community", "Government"],
    desc: "Develops plans and programs for the use of land. They consider the needs of a community and the environment for sustainable growth.",
    scoreMatch: 0.81,
    learningPath: [
      { step: "Understand public policy, economics, and sociology", resources: ["https://www.coursera.org/courses?query=urban%20planning", "https://www.edx.org/learn/public-policy"] },
      { step: "Learn GIS (Geographic Information Systems) software", resources: ["https://www.esri.com/en-us/training/"] },
      { step: "Gain experience through internships or community projects", resources: ["https://www.planning.org/job-center/"] },
      { step: "Pursue a master's degree in urban planning", resources: ["https://www.planning.org/learning/"] }
    ]
  },
  {
    id: "c15",
    title: "Architect",
    tags: ["Design", "Art", "Engineering", "Construction"],
    desc: "Plans and designs buildings and other structures. They balance aesthetics with safety and functionality.",
    scoreMatch: 0.84,
    learningPath: [
      { step: "Develop strong foundational skills in art and math", resources: ["https://www.khanacademy.org/math", "https://www.skillshare.com/browse/drawing"] },
      { step: "Learn CAD software (AutoCAD, Revit)", resources: ["https://www.autodesk.com/education/free-software/autocad", "https://www.autodesk.com/revit/"] },
      { step: "Gain professional experience through internships", resources: ["https://www.aia.org/"] },
      { step: "Complete a professional degree and licensure", resources: ["https://www.naab.org/"] }
    ]
  },
  {
    id: "c16",
    title: "Game Developer",
    tags: ["Gaming", "Programming", "Art", "Design"],
    desc: "Creates video games. This can include programming, art, game design, and sound design.",
    scoreMatch: 0.89,
    learningPath: [
      { step: "Learn a game engine (Unity, Unreal Engine)", resources: ["https://learn.unity.com/", "https://www.unrealengine.com/en-US/onlinelearning-courses"] },
      { step: "Master programming languages (C++, C#)", resources: ["https://www.learncpp.com/", "https://docs.microsoft.com/en-us/dotnet/csharp/"] },
      { step: "Work on small game projects from start to finish", resources: ["https://itch.io/", "https://gamejolt.com/"] },
      { step: "Specialize in a specific area (e.g., character artist, level designer)", resources: ["https://www.gamedev.net/"] }
    ]
  },
  {
    id: "c17",
    title: "Nurse",
    tags: ["Healthcare", "Science", "Helping"],
    desc: "Provides direct patient care, administers medications, and educates patients and their families on health management.",
    scoreMatch: 0.90,
    learningPath: [
      { step: "Complete a nursing degree (BSN, ADN)", resources: ["https://www.ncsbn.org/"] },
      { step: "Pass the NCLEX-RN exam for licensure", resources: ["https://www.ncsbn.org/nclex.htm"] },
      { step: "Gain clinical experience through rotations", resources: ["https://www.nursingworld.org/"] },
      { step: "Pursue specializations and continuing education", resources: ["https://www.aanp.org/", "https://www.ons.org/"] }
    ]
  },
  {
    id: "c18",
    title: "Graphic Designer",
    tags: ["Design", "Art", "Marketing"],
    desc: "Creates visual concepts to communicate ideas that inspire, inform, and captivate consumers.",
    scoreMatch: 0.80,
    learningPath: [
      { step: "Master design principles (typography, color theory)", resources: ["https://www.canva.com/learn/graphic-design-basics/", "https://www.coursera.org/specializations/graphic-design"] },
      { step: "Learn professional software (Adobe Creative Suite)", resources: ["https://www.adobe.com/education.html"] },
      { step: "Build a strong portfolio with diverse projects", resources: ["https://www.behance.net/", "https://dribbble.com/"] },
      { step: "Network with other designers and professionals", resources: ["https://www.aiga.org/"] }
    ]
  },
  {
    id: "c19",
    title: "Physician",
    tags: ["Healthcare", "Science", "Medicine", "Helping"],
    desc: "Diagnoses and treats illnesses and injuries. They prescribe medication and provide medical advice.",
    scoreMatch: 0.95,
    learningPath: [
      { step: "Complete a bachelor's degree with pre-med coursework", resources: ["https://www.aamc.org/students/applying-medical-school/"] },
      { step: "Pass the MCAT and apply to medical school", resources: ["https://www.aamc.org/students/applying-medical-school/mcat/"] },
      { step: "Complete medical school and a residency program", resources: ["https://www.ama-assn.org/education/medical-student-resources/medical-school-guide"] },
      { step: "Obtain licensure and specialty board certification", resources: ["https://www.abms.org/"] }
    ]
  },
  {
    id: "c20",
    title: "Teacher",
    tags: ["Education", "Helping", "Communication"],
    desc: "Educates and inspires students. They develop lesson plans, instruct students, and evaluate their progress.",
    scoreMatch: 0.85,
    learningPath: [
      { step: "Earn a bachelor's degree in education or a subject area", resources: ["https://www.teach.org/"] },
      { step: "Complete a student teaching practicum", resources: ["https://www.neafoundation.org/for-educators/student-teaching/"] },
      { step: "Obtain state teaching certification/licensure", resources: ["https://www.ecs.org/teaching-licensure/"] },
      { step: "Pursue a master's degree for professional development", resources: ["https://www.gradschools.com/programs/education"] }
    ]
  },
  {
    id: "c21",
    title: "Biomedical Engineer",
    tags: ["Engineering", "Biology", "Healthcare", "Technology"],
    desc: "Designs and builds medical devices, equipment, and systems. They apply engineering principles to medicine and biology.",
    scoreMatch: 0.90,
    learningPath: [
      { step: "Master biology, chemistry, and engineering fundamentals", resources: ["https://www.khanacademy.org/science/biology", "https://ocw.mit.edu/courses/biological-engineering/"] },
      { step: "Learn CAD software and programming languages (e.g., MATLAB)", resources: ["https://www.autodesk.com/education/free-software/autocad", "https://www.mathworks.com/help/matlab/"] },
      { step: "Gain hands-on experience through lab work and projects", resources: ["https://www.bmes.org/"] },
      { step: "Pursue a bachelor's or master's degree in biomedical engineering", resources: ["https://www.abet.org/accreditation/find-programs/"] }
    ]
  },
  {
    id: "c22",
    title: "Lawyer",
    tags: ["Law", "Justice", "Communication", "Research"],
    desc: "Represents clients in legal matters, provides legal advice, and prepares legal documents.",
    scoreMatch: 0.88,
    learningPath: [
      { step: "Complete a bachelor's degree in any field", resources: ["https://www.americanbar.org/groups/legal_education/resources/undergraduate_education/"] },
      { step: "Pass the LSAT and attend an accredited law school", resources: ["https://www.lsac.org/"] },
      { step: "Complete internships and gain practical experience", resources: ["https://www.americanbar.org/groups/legal_education/"] },
      { step: "Pass the state bar examination for licensure", resources: ["https://www.ncbex.org/exams/bar-exam/"] }
    ]
  },
  {
    id: "c23",
    title: "Accountant",
    tags: ["Finance", "Business", "Numbers"],
    desc: "Prepares and examines financial records. They ensure that financial records are accurate and that taxes are paid correctly and on time.",
    scoreMatch: 0.85,
    learningPath: [
      { step: "Earn a bachelor's degree in accounting", resources: ["https://www.accountingcoach.com/"] },
      { step: "Master spreadsheet software (Excel)", resources: ["https://www.microsoft.com/en-us/learning/excel-training.aspx"] },
      { step: "Gain experience through internships or entry-level jobs", resources: ["https://www.aicpa.org/career/career-guidance.html"] },
      { step: "Pursue professional certifications (e.g., CPA)", resources: ["https://www.aicpa.org/becomeacpa.html"] }
    ]
  },
  {
    id: "c24",
    title: "Civil Engineer",
    tags: ["Engineering", "Construction", "Design", "Infrastructure"],
    desc: "Designs, builds, and maintains infrastructure projects, such as roads, bridges, and dams.",
    scoreMatch: 0.86,
    learningPath: [
      { step: "Master core engineering concepts (statics, mechanics)", resources: ["https://www.asce.org/education-and-careers/"] },
      { step: "Learn CAD software and structural analysis tools", resources: ["https://www.autodesk.com/education/free-software/autocad", "https://www.ramstructural.com/"] },
      { step: "Gain hands-on experience through internships and projects", resources: ["https://www.asce.org/education-and-careers/student-members/"] },
      { step: "Pursue a bachelor's degree and professional licensure (P.E.)", resources: ["https://www.abet.org/accreditation/find-programs/"] }
    ]
  },
  {
    id: "c25",
    title: "Physical Therapist",
    tags: ["Healthcare", "Movement", "Helping"],
    desc: "Helps patients restore function, improve mobility, and manage pain after an injury or illness.",
    scoreMatch: 0.89,
    learningPath: [
      { step: "Complete a bachelor's degree in a related field", resources: ["https://www.apta.org/"] },
      { step: "Gain clinical observation hours", resources: ["https://www.apta.org/"] },
      { step: "Earn a Doctor of Physical Therapy (DPT) degree", resources: ["https://www.capteonline.org/home"] },
      { step: "Pass the National Physical Therapy Examination (NPTE)", resources: ["https://www.fsbpt.org/"] }
    ]
  },
  {
    id: "c26",
    title: "Electrician",
    tags: ["Skilled Trades", "Construction", "Technical"],
    desc: "Installs, maintains, and repairs electrical systems, wiring, and lighting.",
    scoreMatch: 0.82,
    learningPath: [
      { step: "Complete a high school diploma or GED", resources: ["https://www.dol.gov/agencies/eta/apprenticeship"] },
      { step: "Enroll in an apprenticeship program", resources: ["https://www.dol.gov/agencies/eta/apprenticeship"] },
      { step: "Complete on-the-job training and classroom instruction", resources: ["https://www.ibew.org/"] },
      { step: "Pass a licensing exam for the state you work in", resources: ["https://www.nccer.org/workforce-development/credentialing"] }
    ]
  },
  {
    id: "c27",
    title: "Financial Advisor",
    tags: ["Finance", "Business", "Communication"],
    desc: "Helps clients manage their money, plan for retirement, and achieve other financial goals.",
    scoreMatch: 0.84,
    learningPath: [
      { step: "Earn a bachelor's degree (finance, economics, business)", resources: ["https://www.investopedia.com/articles/financial-careers/09/become-financial-advisor.asp"] },
      { step: "Pass the Series 7 and Series 66/63 exams", resources: ["https://www.finra.org/registration-exams-ce/qualification-exams/series7"] },
      { step: "Gain experience with a firm or brokerage", resources: ["https://www.cfp.net/"] },
      { step: "Pursue a Certified Financial Planner (CFP) designation", resources: ["https://www.cfp.net/"] }
    ]
  },
  {
    id: "c28",
    title: "Journalist",
    tags: ["Communication", "Writing", "Research"],
    desc: "Researches, writes, and reports on news stories and events for various media.",
    scoreMatch: 0.79,
    learningPath: [
      { step: "Develop strong writing and research skills", resources: ["https://www.poynter.org/", "https://www.coursera.org/courses?query=journalism"] },
      { step: "Learn media law and ethical reporting", resources: ["https://www.spj.org/"] },
      { step: "Gain experience through student newspapers or internships", resources: ["https://www.spj.org/internships.asp"] },
      { step: "Build a portfolio of published work", resources: ["https://muckrack.com/"] }
    ]
  },
  {
    id: "c29",
    title: "Chef",
    tags: ["Culinary", "Creativity", "Food", "Management"],
    desc: "Plans menus, oversees kitchen staff, and prepares meals in a professional setting.",
    scoreMatch: 0.81,
    learningPath: [
      { step: "Learn basic cooking techniques and food safety", resources: ["https://www.culinaryschools.org/", "https://www.servsafe.com/"] },
      { step: "Enroll in a culinary arts program or apprenticeship", resources: ["https://www.acfchefs.org/"] },
      { step: "Gain extensive hands-on experience in various kitchens", resources: ["https://www.starchefs.com/"] },
      { step: "Specialize in a type of cuisine", resources: ["https://www.escoffier.edu/blog/"] }
    ]
  },
  {
    id: "c30",
    title: "Dentist",
    tags: ["Healthcare", "Science", "Medicine"],
    desc: "Diagnoses and treats diseases and conditions of the teeth and gums.",
    scoreMatch: 0.92,
    learningPath: [
      { step: "Complete a bachelor's degree with pre-dental coursework", resources: ["https://www.ada.org/education/dental-schools/admission-to-dental-school"] },
      { step: "Pass the DAT and apply to dental school", resources: ["https://www.ada.org/education/dental-admission-test-dat"] },
      { step: "Complete dental school and a residency (if specializing)", resources: ["https://www.adea.org/go-dental.aspx"] },
      { step: "Pass the national and state board exams for licensure", resources: ["https://www.ada.org/en/education/licensure/"] }
    ]
  },
  {
    id: "c31",
    title: "Interior Designer",
    tags: ["Design", "Art", "Space", "Creativity"],
    desc: "Plans and designs the interior spaces of buildings, making them functional, safe, and beautiful.",
    scoreMatch: 0.80,
    learningPath: [
      { step: "Learn design principles and color theory", resources: ["https://www.houzz.com/professionals/interior-designer", "https://www.udemy.com/topic/interior-design/"] },
      { step: "Master design software (AutoCAD, SketchUp)", resources: ["https://www.autodesk.com/education/free-software/autocad", "https://www.sketchup.com/"] },
      { step: "Build a portfolio with diverse projects", resources: ["https://www.asid.org/career-center/portfolio-tips"] },
      { step: "Pursue a degree and professional certification (NCIDQ)", resources: ["https://www.cidq.org/"] }
    ]
  },
  {
    id: "c32",
    title: "Pharmacist",
    tags: ["Healthcare", "Science", "Medicine"],
    desc: "Dispenses medications and provides drug information to patients and other healthcare professionals.",
    scoreMatch: 0.89,
    learningPath: [
      { step: "Complete a bachelor's degree with pre-pharmacy coursework", resources: ["https://www.acpe-accredit.org/"] },
      { step: "Pass the PCAT and apply to a Doctor of Pharmacy (Pharm.D.) program", resources: ["https://www.pcatweb.net/"] },
      { step: "Complete a Pharm.D. degree", resources: ["https://www.acpe-accredit.org/"] },
      { step: "Pass the NAPLEX and state board exams for licensure", resources: ["https://nabp.pharmacy/programs/naplex/"] }
    ]
  },
  {
    id: "c33",
    title: "Speech-Language Pathologist",
    tags: ["Healthcare", "Communication", "Helping"],
    desc: "Diagnoses and treats communication and swallowing disorders.",
    scoreMatch: 0.88,
    learningPath: [
      { step: "Earn a bachelor's degree in a related field", resources: ["https://www.asha.org/"] },
      { step: "Complete a master's degree in Speech-Language Pathology", resources: ["https://www.asha.org/"] },
      { step: "Complete a clinical fellowship year (CFY)", resources: ["https://www.asha.org/"] },
      { step: "Pass the Praxis Exam and obtain state licensure", resources: ["https://www.ets.org/praxis/prepare/materials/5331"] }
    ]
  },
  {
    id: "c34",
    title: "Social Worker",
    tags: ["Helping", "Community", "Psychology", "Sociology"],
    desc: "Helps individuals, families, and communities cope with and solve problems in their everyday lives.",
    scoreMatch: 0.85,
    learningPath: [
      { step: "Earn a bachelor's degree in social work (BSW) or a related field", resources: ["https://www.cswe.org/"] },
      { step: "Gain experience through internships and volunteering", resources: ["https://www.socialworkers.org/"] },
      { step: "Complete a master's degree in social work (MSW)", resources: ["https://www.cswe.org/"] },
      { step: "Obtain state licensure or certification", resources: ["https://www.aswb.org/"] }
    ]
  },
  {
    id: "c35",
    title: "Psychologist",
    tags: ["Psychology", "Science", "Mental Health", "Research"],
    desc: "Studies the human mind and behavior. They diagnose and treat mental, emotional, and behavioral disorders.",
    scoreMatch: 0.91,
    learningPath: [
      { step: "Complete a bachelor's degree in psychology", resources: ["https://www.apa.org/education/undergrad/"] },
      { step: "Gain research or clinical experience", resources: ["https://www.apa.org/education/grad/internships"] },
      { step: "Earn a doctoral degree (Ph.D. or Psy.D.)", resources: ["https://www.apa.org/education/grad/"] },
      { step: "Complete a postdoctoral fellowship and obtain state licensure", resources: ["https://www.aspppb.net/"] }
    ]
  },
  {
    id: "c36",
    title: "Dietitian/Nutritionist",
    tags: ["Healthcare", "Health", "Food", "Science"],
    desc: "Assesses and plans nutrition programs to improve the health of individuals and communities.",
    scoreMatch: 0.87,
    learningPath: [
      { step: "Earn a bachelor's degree in nutrition or dietetics", resources: ["https://www.eatrightpro.org/"] },
      { step: "Complete a supervised practice program/internship", resources: ["https://www.eatrightpro.org/acend/accredited-programs/internships-and-preselect"] },
      { step: "Pass the Registration Examination for Dietitians", resources: ["https://www.cdrnet.org/certifications/registered-dietitian-rd"] },
      { step: "Maintain continuing education to stay licensed", resources: ["https://www.cdrnet.org/certifications/registered-dietitian-rd"] }
    ]
  },
  {
    id: "c37",
    title: "Aerospace Engineer",
    tags: ["Engineering", "Science", "Aviation", "Space"],
    desc: "Designs and develops aircraft, spacecraft, and missiles. They work with aerodynamics, propulsion, and structural design.",
    scoreMatch: 0.93,
    learningPath: [
      { step: "Master physics, calculus, and fluid dynamics", resources: ["https://www.khanacademy.org/science/physics", "https://ocw.mit.edu/courses/aeronautics-and-astronautics/"] },
      { step: "Learn industry-standard software (CATIA, MATLAB)", resources: ["https://www.3ds.com/products-services/catia/education/", "https://www.mathworks.com/help/matlab/"] },
      { step: "Gain experience through internships at companies like NASA or SpaceX", resources: ["https://www.aiaa.org/careers/internships"] },
      { step: "Pursue a bachelor's or master's degree in aerospace engineering", resources: ["https://www.abet.org/accreditation/find-programs/"] }
    ]
  },
  {
    id: "c38",
    title: "User Researcher",
    tags: ["Research", "Design", "Psychology", "Technology"],
    desc: "Studies how people interact with products and services. They provide insights to help create better user experiences.",
    scoreMatch: 0.88,
    learningPath: [
      { step: "Understand research methodologies and psychology", resources: ["https://www.nngroup.com/articles/user-research-methods/", "https://www.coursera.org/specializations/google-ux-design"] },
      { step: "Learn tools for qualitative and quantitative research", resources: ["https://www.userzoom.com/", "https://www.usertesting.com/"] },
      { step: "Practice conducting interviews and usability tests", resources: ["https://www.interaction-design.org/literature/topics/user-research"] },
      { step: "Build a portfolio of research projects and case studies", resources: ["https://www.uxfol.io/"] }
    ]
  },
  {
    id: "c39",
    title: "Video Editor",
    tags: ["Media", "Creativity", "Art", "Film"],
    desc: "Manipulates and rearranges video footage to create a final, cohesive production.",
    scoreMatch: 0.79,
    learningPath: [
      { step: "Learn the principles of storytelling and pacing", resources: ["https://www.storyblocks.com/blog/video-editing-basics-for-beginners"] },
      { step: "Master professional editing software (Adobe Premiere Pro, DaVinci Resolve)", resources: ["https://www.adobe.com/products/premiere/free-trial-download.html", "https://www.blackmagicdesign.com/products/davinciresolve/"] },
      { step: "Build a portfolio with various video projects", resources: ["https://www.youtube.com/", "https://vimeo.com/"] },
      { step: "Network and find freelance or full-time opportunities", resources: ["https://www.upwork.com/", "https://www.freelancer.com/"] }
    ]
  },
  {
    id: "c40",
    title: "IT Project Manager",
    tags: ["Management", "Technology", "Business", "IT"],
    desc: "Oversees information technology projects from planning to execution. They ensure projects are completed on time and within budget.",
    scoreMatch: 0.86,
    learningPath: [
      { step: "Understand project management methodologies (Agile, Scrum)", resources: ["https://www.pmi.org/", "https://www.scrum.org/"] },
      { step: "Learn project management software (Jira, Trello)", resources: ["https://www.atlassian.com/software/jira", "https://trello.com/"] },
      { step: "Gain experience leading small teams or projects", resources: ["https://www.coursera.org/specializations/google-project-management"] },
      { step: "Obtain professional certifications (PMP, CAPM)", resources: ["https://www.pmi.org/certifications"] }
    ]
  },
  {
    id: "c41",
    title: "Photographer",
    tags: ["Art", "Creativity", "Visuals", "Media"],
    desc: "Captures images using a camera to tell a story or document an event. They may specialize in portraits, nature, or journalism.",
    scoreMatch: 0.77,
    learningPath: [
      { step: "Learn the fundamentals of camera settings and composition", resources: ["https://www.digital-photography-school.com/", "https://www.skillshare.com/browse/photography"] },
      { step: "Master photo editing software (Adobe Photoshop, Lightroom)", resources: ["https://www.adobe.com/products/photoshop.html", "https://www.adobe.com/products/photoshop-lightroom.html"] },
      { step: "Build a diverse portfolio of work", resources: ["https://www.behance.net/", "https://www.flickr.com/"] },
      { step: "Specialize in a niche and network with clients", resources: ["https://500px.com/", "https://www.freelancewriting.com/freelance-photographer-jobs/"] }
    ]
  },
  {
    id: "c42",
    title: "Chemist",
    tags: ["Science", "Research", "Lab", "STEM"],
    desc: "Studies the properties and composition of matter and the reactions they undergo. They work in research, manufacturing, or academia.",
    scoreMatch: 0.88,
    learningPath: [
      { step: "Master chemistry, physics, and mathematics", resources: ["https://www.khanacademy.org/science/chemistry", "https://ocw.mit.edu/courses/chemistry/"] },
      { step: "Gain hands-on experience in a lab environment", resources: ["https://www.acs.org/"] },
      { step: "Pursue a bachelor's or master's degree in chemistry", resources: ["https://www.acs.org/education/undergraduate.html"] },
      { step: "Specialize in a field like organic, physical, or analytical chemistry", resources: ["https://www.acs.org/content/acs/en/careers/career-paths.html"] }
    ]
  },
  {
    id: "c43",
    title: "Zoologist",
    tags: ["Science", "Animals", "Biology", "Environment"],
    desc: "Studies animals and their behavior, habitats, and ecosystems. They work in research, conservation, and education.",
    scoreMatch: 0.84,
    learningPath: [
      { step: "Master biology, ecology, and animal behavior", resources: ["https://www.khanacademy.org/science/biology", "https://www.coursera.org/courses?query=animal%20behavior"] },
      { step: "Gain hands-on experience through volunteering or internships", resources: ["https://www.aazk.org/job-search/internships", "https://www.aza.org/"] },
      { step: "Earn a bachelor's degree in zoology or a related field", resources: ["https://www.aza.org/"] },
      { step: "Pursue a master's or doctoral degree for research roles", resources: ["https://www.aza.org/"] }
    ]
  },
  {
    id: "c44",
    title: "Technical Writer",
    tags: ["Writing", "Technology", "Communication", "Documentation"],
    desc: "Creates technical documents, such as user manuals, how-to guides, and tutorials for products and services.",
    scoreMatch: 0.85,
    learningPath: [
      { step: "Develop strong writing and communication skills", resources: ["https://www.coursera.org/courses?query=technical%20writing", "https://www.stc.org/"] },
      { step: "Learn a specific technical domain (e.g., software, engineering)", resources: ["https://www.udemy.com/topic/technical-writing/"] },
      { step: "Master documentation tools and markup languages", resources: ["https://www.oxygenxml.com/", "https://www.doxygen.nl/"] },
      { step: "Build a portfolio with writing samples", resources: ["https://medium.com/"] }
    ]
  },
  {
    id: "c45",
    title: "Human Resources Manager",
    tags: ["Management", "Business", "People", "HR"],
    desc: "Oversees the administrative functions of an organization, including hiring, employee relations, and benefits.",
    scoreMatch: 0.83,
    learningPath: [
      { step: "Understand employment law and HR principles", resources: ["https://www.shrm.org/learning-and-development/education-and-professional-development/shrm-body-of-competency-and-knowledge", "https://www.coursera.org/courses?query=human%20resources"] },
      { step: "Develop strong communication and conflict resolution skills", resources: ["https://www.udemy.com/topic/hr-management/"] },
      { step: "Gain experience through internships or entry-level roles", resources: ["https://www.shrm.org/"] },
      { step: "Obtain professional certifications (e.g., SHRM-CP, PHR)", resources: ["https://www.shrm.org/certifications"] }
    ]
  },
  {
    id: "c46",
    title: "Librarian",
    tags: ["Education", "Information", "Research", "Community"],
    desc: "Manages and organizes information resources for a community. They assist people with research and provide educational programming.",
    scoreMatch: 0.78,
    learningPath: [
      { step: "Develop strong research and organizational skills", resources: ["https://www.ala.org/educationcareers/"] },
      { step: "Gain experience through volunteering or library assistant roles", resources: ["https://www.ala.org/educationcareers/ala-career-services-and-resources"] },
      { step: "Earn a Master of Library Science (MLS) or equivalent degree", resources: ["https://www.ala.org/educationcareers/accreditedprograms/directory"] },
      { step: "Specialize in an area (e.g., school, medical, or law library)", resources: ["https://www.ala.org/educationcareers/type-libraries-librarians"] }
    ]
  },
  {
    id: "c47",
    title: "Physical Therapist Assistant",
    tags: ["Healthcare", "Movement", "Helping"],
    desc: "Works under the supervision of a physical therapist to help patients with exercises and treatments.",
    scoreMatch: 0.86,
    learningPath: [
      { step: "Earn an associate's degree from a CAPTE-accredited program", resources: ["https://www.capteonline.org/home"] },
      { step: "Complete clinical rotations to gain hands-on experience", resources: ["https://www.apta.org/"] },
      { step: "Pass the National Physical Therapy Examination (NPTE) for PTAs", resources: ["https://www.fsbpt.org/"] },
      { step: "Obtain state licensure", resources: ["https://www.fsbpt.org/"] }
    ]
  },
  {
    id: "c48",
    title: "Pilot",
    tags: ["Aviation", "Travel", "Transportation", "Technical"],
    desc: "Flies aircraft for commercial airlines, private companies, or the military. They are responsible for the safety of the crew and passengers.",
    scoreMatch: 0.89,
    learningPath: [
      { step: "Complete a flight training program or military service", resources: ["https://www.faa.gov/training_testing/training/"] },
      { step: "Obtain a private pilot license (PPL)", resources: ["https://www.faa.gov/pilots/become/private_pilot"] },
      { step: "Build flight hours and obtain additional ratings (instrument, multi-engine)", resources: ["https://www.faa.gov/pilots/become/commercial_pilot"] },
      { step: "Earn a commercial pilot license (CPL) and air transport pilot (ATP) certificate", resources: ["https://www.faa.gov/pilots/become/atp"] }
    ]
  },
  {
    id: "c49",
    title: "Technical Support Specialist",
    tags: ["IT", "Customer Service", "Problem-Solving", "Technology"],
    desc: "Provides assistance and support to users experiencing technical issues with hardware, software, or systems.",
    scoreMatch: 0.82,
    learningPath: [
      { step: "Master troubleshooting basics and computer systems", resources: ["https://www.comptia.org/certifications/a"] },
      { step: "Develop strong communication and problem-solving skills", resources: ["https://www.coursera.org/specializations/google-it-support"] },
      { step: "Obtain certifications (e.g., CompTIA A+)", resources: ["https://www.comptia.org/certifications/a"] },
      { step: "Gain experience through help desk or call center roles", resources: ["https://www.coursera.org/specializations/google-it-support"] }
    ]
  },
  {
    id: "c50",
    title: "Medical Assistant",
    tags: ["Healthcare", "Administrative", "Helping"],
    desc: "Performs administrative and clinical tasks in a healthcare setting under the supervision of a physician.",
    scoreMatch: 0.85,
    learningPath: [
      { step: "Complete an accredited medical assisting program", resources: ["https://www.caahep.org/accreditation/find-an-accredited-program.html"] },
      { step: "Gain clinical experience through externships", resources: ["https://www.aama-ntl.org/"] },
      { step: "Obtain professional certification (e.g., CMA, RMA)", resources: ["https://www.aama-ntl.org/certification"] },
      { step: "Maintain certification through continuing education", resources: ["https://www.aama-ntl.org/certification/maintaining-certification"] }
    ]
  }
];

export const RIASEC_INFO = {
  Realistic: "Practical, hands-on, physical activities",
  Investigative: "Curious, analytical, research-oriented",
  Artistic: "Creative, imaginative, expressive",
  Social: "Helping, teaching, counseling",
  Enterprising: "Leadership, persuasion, business-oriented",
  Conventional: "Organized, detail-oriented, administrative"
};
