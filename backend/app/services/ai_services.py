from app import db
from app.models import Prediction
from sqlalchemy.orm import joinedload
import requests
import re
from config import Config
from flask import jsonify
import json
from string import Template

OPENROUTER_API_KEY = Config.OPENROUTER_API_KEY

core_subject_list = [
    "Programming And Problem Solving",
    "Software And Requirements",
    "Tcp/Ip Network Fundamentals",
    "Probability And Statistics For Computing",
    "Object-Oriented Application Development",
    "Database System Fundamentals",
    "Introduction To Computer Organisation And Architecture",
    "Human Computer Interaction Design",
    "Operating Systems",
    "Problem Solving With Data Structures And Algorithms",
    "Computer Ethics And Professional Responsibility",
    "Web Application Development",
    "Software Testing",
    "Software Design",
    "Software Project Management",
    "Software Construction And Configuration",
    "Wireless Application Development",
    "Advanced Web Application Development",
    "Software Quality Assurance",
    "Software Entrepreneurship",
]

elective_subject_list = [
    "Multimedia Technology",
    "Artificial Intelligence",
    "Team Project",
    "Programming With Game Engines",
    "Advanced Database Systems",
    "Cloud Computing",
    "Digital Image Processing",
    "Fundamentals Of Cybersecurity",
    "Data Mining",
    "Tcp/Ip Network Routing",
    "Server Configuration And Management",
    "Tcp/Ip Network Application Development",
    "Network Security Management",
    "Parallel Processing"
]

PRIORITY_INSTRUCTIONS = (
    "Priority Instructions:\n"
    "1. Recommend at most 6 subjects in total, with at most 3 core subjects and at most 3 elective subjects.\n"
    "2. For core subjects, prioritize subjects from lower academic years (Year 1 > Year 2 > Year 3).\n"
    "3. Below is the list of subjects with a brief description for each:\n\n"
    "Core Subjects:\n"
    "   - Programming and Problem Solving – Year 1: Introduces fundamental programming using C++ and MS Visual Studio. Covers computer hardware/software, programming languages, algorithm development, data types, variables, operators, I/O, control structures, functions, arrays, file handling, and basic data structures. Practical exercises develop problem-solving and coding skills.\n"
    "   - Software and Requirements – Year 1: Introduces software engineering and requirements engineering. Topics include software development processes, roles, functional/non-functional requirements, elicitation, specification, validation, modeling (use case, activity, DFDs), and development methodologies (Agile, RAD, UP). Hands-on with CASE tools like Enterprise Architect.\n"
    "   - TCP/IP Network Fundamentals – Year 1: Focuses on protocol layers, network addressing, subnetting, VLSM, internetworking devices, DHCP, DNS, routing (RIP, OSPF), ACLs, and IPv4/IPv6 transition. Includes labs using Packet Tracer and Wireshark for configuration, analysis, and troubleshooting.\n"
    "   - Probability and Statistics for Computing – Year 1: Covers data modeling, probability rules, distributions (discrete/continuous), estimation, hypothesis testing, and regression. Emphasis on theoretical understanding and application in computing with statistical software.\n"
    "   - Object-Oriented Application Development – Year 1: This subject require pre-requisite in Programming and Problem Solving. It introduces students to object-oriented programming (OOP) using Java. The course covers fundamental OOP concepts such as objects, classes, encapsulation, inheritance, and polymorphism, and demonstrates how to build applications with graphical user interfaces, event-driven programming, and file processing. Practical sessions using an IDE like Eclipse or Visual Studio .NET provide hands-on coding experience. The course requires prior knowledge from Programming and Problem Solving, ensuring that students have a solid programming foundation before advancing into OOP.\n"
    "   - Database System Fundamentals – Year 1: It provides an in-depth exploration of relational databases and database management systems. Students learn key concepts such as entity-relationship modeling, relational data models, and SQL for schema definition, data manipulation, and querying. The course covers database design techniques including normalization, design theory, and methodologies to create efficient, secure databases. Additionally, practical lab sessions using Oracle tools equip students with hands-on experience in creating, modifying, and querying database tables, as well as managing user accounts and ensuring basic database security.\n"
    "   - Introduction to Computer Organisation and Architecture – Year 2: It provides foundational knowledge of computer systems, their components, and underlying architecture. The course covers hardware and software fundamentals, number systems, data representation, CPU and memory structures, peripheral devices, digital logic, and assembly language programming. Students engage in practical labs using assemblers or simulators such as MPLab and QtSPIM to explore memory hierarchy, stack operations, and procedural calls. The course aims to develop a solid understanding of how computers function at a low level, essential for further studies in computer science and engineering.\n"
    "   - Human Computer Interaction Design – Year 2: Focuses on user-centered design, human cognition, usability principles, interface design, interaction styles, and the design process for various platforms, including mobile and web applications. Students gain practical experience through interactive prototyping using tools like Axure Pro, where they develop web and smartphone prototypes with dynamic interfaces, animations, and usability features. The course prepares students to design intuitive and effective user interfaces by understanding human factors and applying best practices in interaction design.\n"
    "   - Operating Systems – Year 2: Covers OS concepts: process and CPU management, memory/storage organization, scheduling, synchronization, deadlocks, partitioning, paging, segmentation, virtual memory, file systems, and OS security. Includes real-world application and analysis. \n"
    "   - Problem Solving with Data Structures and Algorithms – Year 2: This subject require pre-requisite in Object-Oriented Application Development. It introduces key data structures and algorithms essential for efficient problem-solving. It covers techniques such as recursion, generics, and the Java Collections framework, alongside core data structures like arrays, linked lists, stacks, queues, trees, and graphs. Students will explore algorithm efficiency and complexity, implementing sorting (e.g., bubble sort, quick sort) and searching algorithms (e.g., linear search, binary search). The course is designed for students who have prior knowledge in object-oriented programming, with pre-requisites including Object-Oriented Application Development, ensuring they are well-prepared to tackle advanced problem-solving techniques using Java.\n"
    "   - Computer Ethics and Professional Responsibility – Year 2: It explores ethical, legal, and professional issues related to computing and technological advancements. It covers topics such as privacy, intellectual property, cybercrime, freedom of speech, digital divide, and the responsibilities of computing professionals. Students will examine relevant laws in Malaysia and globally, including the Personal Data Protection Act (PDPA), Copyright Act, Official Secrets Act, and Whistleblower Protection Act. The course also discusses professional ethics, system failures, and the impact of technology on work and society. Through case studies and discussions, students will develop a critical understanding of ethical dilemmas in computing and their responsibilities as future IT professionals.\n"
    "   - Web Application Development – Year 2: This subject require pre-requisite in Object-Oriented Application Development. It provides a comprehensive introduction to web programming, covering both client-side and server-side technologies. It begins with an overview of WWW technologies and the installation of web servers, followed by web page creation using HTML5 and styling with CSS. Students will then learn JavaScript for client-side scripting, handling events, and manipulating the DOM. The course delves into server-side scripting, including form handling, database integration, user authentication, and MVC architecture. Finally, it introduces Ajax for building interactive web applications. Practical lab sessions reinforce theoretical concepts, ensuring hands-on experience in modern web development frameworks.\n"
    "   - Software Testing – Year 2: This subject require pre-requisite in Object-Oriented Application Development. It covers essential theoretical and practical aspects of software testing. It introduces fundamental testing principles, processes, and good practices, with a focus on unit testing and web testing. Students will learn about static and dynamic testing techniques, test-driven development (TDD), and different test levels and types. The course also explores test tools, test planning, risk management, and continuous integration. Hands-on labs provide experience with JUnit, Mockito, Selenium, and CI tools, ensuring students develop real-world testing skills for high-quality software development.\n"
    "   - Software Design – Year 2: This subject require pre-requisite in Object-Oriented Application Development. It introduces students to essential principles and practices in software design. It covers software design modeling notations, including structured and object-oriented design models, and teaches low-level and high-level design concepts such as modular decomposition, cohesion, and architectural patterns. Students will explore best practices like use case realization, software design patterns, refactoring, and frameworks. The course also introduces emerging trends such as dependency injection and Model-Driven Engineering. Hands-on lab sessions reinforce theoretical concepts through UML modeling tools like Visual Paradigm and StarUML, ensuring practical experience in designing robust software systems.\n"
    "   - Software Project Management – Year 3: This subject require pre-requisite in Software and Requirements. It provides essential knowledge in project planning, execution, monitoring, and control for software development. It covers project integration, scope, time, cost, quality, risk, human resources, procurement, and communication management. Students will learn financial analysis techniques, scheduling methods like Gantt charts and PERT, quality assurance with Six Sigma, and risk assessment tools. The course emphasizes both traditional and agile project management approaches, ensuring students gain practical skills for effective IT project execution using industry-standard tools and methodologies.\n"
    "   - Software Construction and Configuration – Year 3: It focuses on writing clean code, software configuration, version control, building, and continuous integration (CI) and deployment. Students will learn best practices in coding, refactoring, source code management (Git, SVN), automated builds (Maven, MSBuild), and CI tools (Jenkins, Hudson). Practical labs emphasize hands-on experience with development environments, versioning tools, and build automation. The course equips students with modern DevOps techniques, ensuring smooth software development and deployment processes.\n"
    "   - Wireless Application Development – Year 3: This subject require pre-requisite in Object-Oriented Application Development. It focuses on developing mobile applications for wireless devices like smartphones, tablets, and smartwatches. It covers UI/UX design, data storage (SQLite, SharedPreferences), cloud connectivity (HTTP, JSON, XML), and location-based services. Students gain hands-on experience with Android Studio, Android SDK, and mobile development tools using React Native. Practical labs emphasize building interactive apps, handling notifications, and integrating geolocation features. The course prepares students to develop modern, data-driven, and user-friendly wireless applications.\n"
    "   - Advanced Web Application Development – Year 3: This subject require pre-requisite in Web Application Development. It focuses on building modern web applications using frameworks and the Model-View-Controller (MVC) architecture. Students will learn routing, controllers, views, database interactions (ORM, raw SQL), form handling, authentication & authorization, and state management (cookies & sessions). Advanced topics include JavaScript libraries for client-side scripting, API security (JWT, OAuth), and dependency management. Practical labs provide hands-on experience with PHP, Laravel, MySQL, templating engines, and modern web development tools. This course equips students with skills to develop secure, dynamic, and scalable web applications.\n"
    "   - Software Quality Assurance – Year 3: It focuses on ensuring software quality through process monitoring, quality methodologies, and risk management. Students will learn about quality objectives, process improvement models, software metrics, defect estimation, and economic impacts. The course also covers software testing, peer reviews, inspections, and configuration management. By exploring various quality assurance tools and methodologies, students gain practical skills in evaluating and improving software quality in real-world projects.\n"
    "   - Software Entrepreneurship – Year 3: This subject require pre-requisite in Software Project Management. It equips students with the knowledge and skills to establish and manage their own software business ventures. It covers key aspects such as recognizing opportunities, crafting business plans, crossing market barriers, managing innovation, and ethical responsibilities. Students will learn about feasibility analysis, intellectual property, value creation, and entrepreneurship strategies. The course provides insights into startup challenges, success factors, and social responsibilities to help students develop sustainable and innovative software businesses.\n"
    "Elective Subjects:\n"
    "   - Multimedia Technology: It explores multimedia elements, technologies, and tools essential for developing multimedia applications. It covers static and dynamic multimedia components, multimedia design principles, interactive multimedia, and future trends like virtual and augmented reality. Students engage in both theoretical and practical activities, including multimedia storyboarding, audio and video editing, and animation creation using various tools. The course emphasizes hands-on learning in a computer laboratory, leveraging software like Figma, Audacity, Shotcut, and GIMP. Assessment includes quizzes, assignments, and a final exam, ensuring students gain both conceptual knowledge and practical expertise in multimedia technology.\n"
    "   - Artificial Intelligence: This subject require pre-requisite in Programming and Problem Solving. It provides foundational knowledge in AI, covering supervised and unsupervised learning, problem-solving techniques, neural networks, and data science. Students will explore AI's relationship with machine learning and deep learning, practical AI tools, and modern applications such as generative AI. Key topics include search strategies, genetic algorithms, regression, backpropagation, clustering, and dimensionality reduction. Practical lab sessions focus on Python programming, Jupyter Notebooks, optimization with genetic algorithms, and training neural networks using the Python Anaconda Distribution.\n"
    "   - Team Project: It enables students to apply their knowledge and skills from previous coursework to a real-world software project, either industry-based or research-oriented. Working in teams under faculty supervision, students engage in project planning, requirements elicitation, design and modeling, software implementation, testing, and iterative improvements. Emphasis is placed on collaborative problem-solving, version control, coding best practices, testing methodologies, and documentation. Assessment is 100% project-based, evaluating both individual contributions and teamwork effectiveness. The course prepares students for real-world software development by fostering teamwork, project management, and technical proficiency.\n"
    "   - Programming with Game Engines: It explores the core components and libraries within a game engine, emphasizing their evaluation and application in game development, with pre-requisites including Object-Oriented Application Development. Students learn game engine architecture, scripting, software engineering principles, rendering, animation, physics, AI, and game asset management. Through hands-on practical labs, students gain experience in scripting, character controls, UI, physics, AI, and game publishing. The course follows a 100% practical/assignment-based assessment, fostering technical proficiency, problem-solving, and software engineering practices in game development using modern game engines like Unity or Godot.\n"
    "   - Advanced Database Systems: This subject require pre-requisite in Database System Fundamentals. It delves into transaction management, concurrency control, query optimization, and recovery techniques in RDBMS, alongside an in-depth exploration of NoSQL databases. Students will study data modeling, NoSQL implementation, large data set processing, and big data technologies like Hadoop, Google BigTable, and Apache Cassandra. Hands-on practical labs include working with PL/SQL, MongoDB, and Hadoop to write queries, model data, process distributed databases, and perform big data operations. The course combines theoretical knowledge with applied learning, preparing students for modern database challenges in cloud-based and large-scale data environments.\n"
    "   - Cloud Computing: This subject require pre-requisite in Object-Oriented Application Development. It introduces the fundamentals, architecture, security, and applications of cloud computing, with a focus on big data. It covers virtualization, cloud service models (IaaS, PaaS, SaaS), security challenges, and the design of cloud applications. Practical labs involve setting up virtual environments, working with Linux OS for cloud administration, developing cloud-based applications using languages like Java, Python, or C#, and deploying them on industry-standard platforms such as AWS, OpenStack, and Hadoop. The course blends theoretical concepts with hands-on experience to equip students with the skills needed for cloud-based system design, deployment, and security in modern IT environments.\n"
    "   - Digital Image Processing: This subject require pre-requisite in Object-Oriented Application Development. It introduces fundamental concepts and practical applications of image processing and computer vision using Python and OpenCV. It covers topics such as image manipulation, arithmetic operations, spatial and frequency domain filtering, object detection, and edge detection techniques like Canny and Hough Transform. The course emphasizes mathematical foundations and algorithm implementation, enabling students to develop real-world applications. Practical labs focus on image enhancement, filtering, noise reduction, and advanced topics like face detection and morphological transformations. \n"
    "   - Fundamentals of Cybersecurity: It introduces students to essential principles, risks, and defense mechanisms in cybersecurity. Covering topics such as risk management, cryptography, database security, network security, and cloud security, the course provides a comprehensive understanding of cybersecurity technologies. It also explores malware analysis, penetration testing, web and mobile security, and forensic tools. Hands-on experience with tools like Kali Linux, TryHackMe, and Cryptool helps students develop practical skills in securing systems and mitigating cyber threats. Through theoretical and practical learning, students will gain the knowledge necessary to understand, analyze, and implement cybersecurity solutions effectively.\n"
    "   - Data Mining: This subject require pre-requisite in Database System Fundamentals, and Programming and Problem Solving. It provides students with a comprehensive understanding of data mining concepts, algorithms, and practical applications. It covers essential topics such as data preprocessing, classification techniques (K-Nearest Neighbors, Decision Trees, Naïve Bayes, and Neural Networks), regression analysis, clustering methods (K-Means), anomaly detection, and association rule mining (Apriori and FP-Growth). Through hands-on programming exercises using Python, students will develop skills in data extraction, visualization, model implementation, and evaluation.\n"
    "   - TCP/IP Network Routing: This subject require pre-requisite in TCP/IP Network Fundamentals. It provides students with a deep understanding of network design, configuration, and troubleshooting. Covering topics such as switching technologies (STP, PortFast), Access Control Lists (ACL), Network Address Translation (NAT), and various routing protocols (RIP, EIGRP, OSPF, BGP), the course emphasizes both theoretical concepts and hands-on practical applications. Using Cisco Packet Tracer, students will gain experience in configuring and verifying network settings, including IPv6 routing and WAN technologies. This course is essential for students aiming to develop networking expertise and prepare for industry certifications like CCNA.\n"
    "   - Server Configuration and Management: It equips students with the knowledge and practical skills needed to install, configure, and manage various types of servers for network system administration. Covering Linux-based network operating systems, database and web server management, network monitoring, virtualization, and cloud services, the course emphasizes hands-on experience with tools like MySQL, Apache, SSH, SAMBA, and network monitoring utilities. Students will also gain expertise in system backup and recovery techniques. This course is ideal for those pursuing careers in IT infrastructure, system administration, and cloud computing.\n"
    "   - TCP/IP Network Application Development: This subject require pre-requisite in Object-Oriented Application Development. It focuses on writing network applications that communicate over local and wide area networks. Students will gain hands-on experience in TCP, UDP, and SCTP sockets, multithreading, and secure network programming. Key topics include IPv4/IPv6 interoperability, broadcasting/multicasting, raw sockets, and secure sockets. The course also introduces scripting for network automation and developing clients for services like SMTP, FTP, and web applications. Practical labs will be conducted using Python and Flask Framework to reinforce the learning experience.\n"
    "   - Network Security Management: This course introduces penetration testing, cybersecurity threats, and defense mechanisms. Students will explore hacking techniques, malware, web attacks, and security countermeasures like firewalls, IDS, cryptography, and security protocols. Key topics include footprinting, network scanning, enumeration, trojans, backdoors, and countermeasures. Practical labs provide hands-on experience with tools like Nmap, Whois, traceroute, and security software to assess vulnerabilities and implement security defenses.\n\n"
)

core_subjects = """
- Programming and Problem Solving
- Software and Requirements
- TCP/IP Network Fundamentals
- Probability and Statistics for Computing
- Object-Oriented Application Development
- Database System Fundamentals
- Introduction to Computer Organisation and Architecture
- Human Computer Interaction Design
- Operating Systems
- Problem Solving with Data Structures and Algorithms
- Computer Ethics and Professional Responsibility
- Web Application Development
- Software Testing
- Software Design
- Software Project Management
- Software Construction and Configuration
- Wireless Application Development
- Advanced Web Application Development
- Software Quality Assurance
- Software Entrepreneurship
"""

elective_subjects = """
- Multimedia Technology
- Artificial Intelligence
- Team Project
- Programming with Game Engines
- Advanced Database Systems
- Cloud Computing
- Digital Image Processing
- Fundamentals of Cybersecurity
- Data Mining
- TCP/IP Network Routing
- Server Configuration and Management
- TCP/IP Network Application Development
- Network Security Management
"""

prompt_template = Template(
    "Below is an instruction that describes a task, paired with an input that provides further context.\n"
    "Write a response that appropriately completes the request.\n\n"

    "⚠️ **IMPORTANT LIMITATION** ⚠️\n"
    "**You MUST recommend a maximum of 3 core subjects and 3 elective subjects only.**\n"
    "**DO NOT exceed this limit under any circumstances.**\n\n"

    "### Instruction:\n"
    "You are an academic advisor for Software Engineering students at UTAR. Based on the student's personal and educational information, "
    "their completed subject grades, and available subjects and their predicted grades, provide a recommended study plan that can improve their CGPA.\n\n"

    "**Rules:**\n"
    "1. **Do NOT recommend any subjects the student has already completed.**\n"
    "2. **Recommend up to 3 core subjects** from the Core Subjects List provided below. Prioritize subjects from lower academic years first (Year 1 > Year 2 > Year 3). Among the same year subjects, **choose those with the highest predicted grades**.\n"
    "3. **Recommend up to 3 elective subjects** from the Elective Subjects List provided below, strictly based on highest predicted grades. Recommend fewer if necessary.\n"
    "4. **DO NOT mix Core and Elective categories. Select Core subjects only from the Core list, and Elective subjects only from the Elective list.**\n"
    "5. **Structure your response into THREE clearly labeled sections:**\n"
    "   - **List of Recommended Subjects:**\n"
    "     - Use bullet points under Core Subjects and Elective Subjects.\n"
    "     - Format each item as: `Subject Name (Predicted Grade)`\n"
    "   - **Justification for Recommendations:**\n"
    "     - Briefly explain **each subject’s selection (2–3 sentences per subject)** under the same headings.\n"
    "   - **Study Plan for Each Subject:**\n"
    "     - For **each recommended subject**, write **one concise paragraph** detailing:\n"
    "       - Key areas to focus on\n"
    "       - Skills to develop\n"
    "       - Tools, languages, or platforms to practice\n\n"
    "6. Be concise, structured, and professional. Avoid extra formatting beyond the specified structure.\n\n"

    "**Core Subjects:**\n"
    "$core_subjects\n\n"
    "**Elective Subjects:**\n"
    "$elective_subjects\n\n"
    "**Subject Descriptions:**\n"
    "$priority\n"

    "### Student Information:\n"
    "$student_info\n\n"

    "⚠️ **REMINDER: RECOMMEND MAXIMUM OF 3 CORE + 3 ELECTIVE SUBJECTS ONLY. DO NOT EXCEED.** ⚠️\n\n"

    "### Response:\n"
    "<think>$cot"
)

def openrouter(pid=1):
    prompt = build_study_plan_prompt(pid)
    print(prompt)
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            }),
            timeout=10
        )
        response.raise_for_status()  # raises HTTPError if response code is 4xx/5xx
        return jsonify(response.json()), 200
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": "HTTP error occurred", "details": str(http_err)}), response.status_code
    except Exception as err:
        return jsonify({"error": "Unexpected error", "details": str(err)}), 500
    
def build_study_plan_prompt(prediction_id: int) -> str:
    prediction = (
        Prediction.query
        .options(joinedload(Prediction.subjects))
        .filter_by(id=prediction_id)
        .first()
    )
    if not prediction:
        raise ValueError(f"Prediction {prediction_id} not found.")

    # Core Fields
    parts = [
        f"Gender: {prediction.gender}",
        f"Year of Birth: {prediction.yob}",
        f"Primary Language: {prediction.primary_language}",
        f"English Proficiency: {prediction.english_proficiency}",
        f"Year & Trimester: {prediction.year_trimester}",
        f"Secondary School Location: {prediction.secondary_school_location}",
        f"Science Stream: {'Yes' if prediction.science_stream else 'No'}",
        f"Qualification: {prediction.qualification}",
        f"Qualification Grades: {prediction.qualification_grades}",
        f"Assignment Collaboration Frequency: {prediction.assignment_working_frequency}",
        f"Computer Interest: {prediction.computer_interest}",
        f"Average Studying Hours per Week: {prediction.average_studying_hour}",
        f"Current CGPA: {prediction.cgpa}",
    ]

    completed = []
    available = []
    for subj in prediction.subjects:
        entry = f"{subj.name}: {subj.grade}"
        if subj.is_prediction:
            available.append(entry)
        else:
            completed.append(entry)

    parts.append("Completed Subjects: " + "; ".join(completed or ["No completed subject."]))
    parts.append("Available Subjects & Predicted Grades: " + "; ".join(available))

    # Full raw student info
    student_info = "\n".join(parts)

    # Cleaned subject helper
    def clean_completed_subjects(student_info: str) -> str:
        match = re.search(r'Completed Subjects:(.*?)(Available Subjects|$)', student_info, re.DOTALL | re.IGNORECASE)
        if not match:
            return ""
        subjects_raw = match.group(1).strip().split(';')
        cleaned = []
        for subject in subjects_raw:
            subject = subject.strip()
            if subject:
                subject = re.sub(r':.*$', '', subject)
                subject = subject.title().replace('Tcp/Ip', 'TCP/IP')
                cleaned.append(subject)
        return "\n".join(f"- {s}" for s in cleaned)

    def split_available_subjects(student_info: str):
        match = re.search(r'Available Subjects & Predicted Grades:(.*)', student_info, re.DOTALL | re.IGNORECASE)
        if not match:
            return "", ""
        subjects_raw = match.group(1).strip().split(';')
        core_list = []
        elective_list = []
        for subject in subjects_raw:
            if not subject.strip():
                continue
            name, grade = [s.strip() for s in subject.split(':', 1)]
            name = name.title().replace('Tcp/Ip', 'TCP/IP')
            if name in core_subject_list:
                core_list.append(f"- {name} ({grade})")
            elif name in elective_subject_list:
                elective_list.append(f"- {name} ({grade})")
        return "\n".join(core_list), "\n".join(elective_list)

    cleaned_completed_subjects = clean_completed_subjects(student_info)
    available_core, available_elective = split_available_subjects(student_info)

    structured_student_info = f"""
    {student_info}

    Cleaned Completed Subjects List:
    {cleaned_completed_subjects}

    Available Core Subjects and Predicted Grades:
    {available_core}

    Available Elective Subjects and Predicted Grades:
    {available_elective}
    """

    prompt = prompt_template.safe_substitute(
        core_subjects="\n".join(f"- {s}" for s in core_subject_list),
        elective_subjects="\n".join(f"- {s}" for s in elective_subject_list),
        priority=PRIORITY_INSTRUCTIONS,
        student_info=structured_student_info,
        cot=""
    )

    return prompt

def get_ai_recommendation(prediction_id: int) -> str | None:
    prediction = (
        Prediction.query
        .options(joinedload(Prediction.subjects))
        .filter_by(id=prediction_id)
        .first()
    )
    if not prediction:
        raise ValueError("Prediction not found")
    return prediction.suggestion

def save_ai_recommendation(prediction_id, suggestion):
    prediction = db.session.get(Prediction, prediction_id)
    prediction.suggestion = suggestion
    db.session.commit()


# def save_ai_recommendation(prediction_id: int, suggestion: str) -> None:
#     prediction = Prediction.query.filter_by(id=prediction_id).first()
#     if not prediction:
#         raise ValueError("Prediction not found")
#     prediction.suggestion = suggestion
#     db.session.commit()
   
# def clean_suggestion(raw: str) -> str:
#     """
#     Remove any <think>…</think> blocks and custom end marker,
#     then collapse extra whitespace.
#     """
#     # remove <think>…</think> (case‑insensitive, multiline)
#     # no_think = re.sub(r'<\s*think\s*>.*?<\s*/\s*think\s*>',
#     #                   '',
#     #                   raw,
#     #                   flags=re.IGNORECASE | re.DOTALL)
#     no_think = re.sub(r'<\s*think\s*>',
#                     '',
#                     raw,
#                     flags=re.IGNORECASE | re.DOTALL)
#     # remove the custom end tag
#     no_marker = re.sub(r'<｜end▁of▁sentence｜>', '', no_think)
#     # collapse 3+ newlines into 2, trim
#     cleaned = re.sub(r'\n{3,}', '\n\n', no_marker).strip()
#     return cleaned
 
# def call_ai_model(question: str) -> str:
#     print(COLAB_NGROK_URL)
#     print(question)
#     resp = requests.post(COLAB_NGROK_URL, json={"question": question})
#     resp.raise_for_status()
#     data = resp.json()
#     raw = data.get("response", "")
#     return clean_suggestion(raw)


# def get_ai_input(prediction_id: int) -> str:
#     prediction = (
#         Prediction.query
#         .options(joinedload(Prediction.subjects))
#         .filter_by(id=prediction_id)
#         .first()
#     )
#     if not prediction:
#         raise ValueError(f"Prediction {prediction_id} not found.")

#     # Core fields
#     parts = [
#         f"Gender: {prediction.gender}",
#         f"Year of Birth: {prediction.yob}",
#         f"Primary Language: {prediction.primary_language}",
#         f"English Proficiency: {prediction.english_proficiency}",
#         f"Year & Trimester: {prediction.year_trimester}",
#         f"Secondary School Location: {prediction.secondary_school_location}",
#         f"Science Stream: {'Yes' if prediction.science_stream else 'No'}",
#         f"Qualification: {prediction.qualification}",
#         f"Qualification Grades: {prediction.qualification_grades}",
#         f"Assignment Collaboration Frequency: {prediction.assignment_working_frequency}",
#         f"Computer Interest: {prediction.computer_interest}",
#         f"Average Studying Hours per Week: {prediction.average_studying_hour}",
#         f"Current CGPA: {prediction.cgpa}",
#     ]

#     # Subjects
#     completed = []
#     available = []
#     for subj in prediction.subjects:
#         entry = f"{subj.name}: {subj.grade}"
#         if subj.is_prediction:
#             available.append(entry)
#         else:
#             completed.append(entry)

#     if not completed:
#         completed = "No completed subject."
        
#     parts.append("Completed Subjects: " + "; ".join(completed))
#     parts.append("Available Subjects & Predicted Grades: " + "; ".join(available))

#     return "\n".join(parts)