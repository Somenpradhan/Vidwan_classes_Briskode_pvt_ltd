import os
import sys

# Ensure backend folder is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User
from app.models.course import Course
from app.models.faculty import Faculty
from app.models.result import Result
from app.models.gallery import GalleryItem
from app.models.testimonial import Testimonial


def seed_database():
    print("Initializing Database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Seed Default Admin User
        admin_email = "admin@vidwanclasses.com"
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        if not existing_admin:
            print("Seeding Admin User...")
            admin_user = User(
                email=admin_email,
                hashed_password=get_password_hash("Admin@12345"),
                full_name="Vidwan Administrator",
                is_admin=True,
                is_active=True
            )
            db.add(admin_user)
            print(f"Created Admin: {admin_email} / Admin@12345")
        else:
            print("Admin user already exists.")

        # 2. Seed Initial Courses if empty
        if db.query(Course).count() == 0:
            print("Seeding Initial Courses...")
            courses = [
                Course(
                    slug="nurture",
                    title="Nurture Program",
                    badge="Class 11 | 2-Year Program",
                    target="JEE (Main + Advanced) & NEET-UG",
                    category="jee",
                    image="assets/images/courses/nurture.jpg",
                    tagline="2-Year Classroom Program for Class 11 Students",
                    overview="The Nurture program is meticulously crafted for Class 11 students, providing a rock-solid foundation for JEE/NEET over a 2-year timeline. It covers the complete syllabus with step-by-step conceptual depth, regular problem-solving drills, and continuous progress tracking.",
                    duration="2 Years (Class 11 & 12)",
                    eligibility="Class 10th Passed / Moving to Class 11th",
                    frequency="4-5 Days/Week (3-4 Hours/Day)",
                    highlights=[
                        "Complete Coverage of Class 11 & 12 Syllabus for Board & Competitive Exams",
                        "Daily Practice Problems (DPPs) with video solutions",
                        "Bi-weekly All India Test Series (AITS) matching exact exam patterns",
                        "Dedicated Doubt Clearance Counters after regular classes",
                        "Personalized Mentorship and Performance Analytics"
                    ],
                    curriculum=[
                        {"phase": "Phase 1 (Class 11)", "topics": "Basic Mathematics, Physics Mechanics, Physical & Inorganic Chemistry, Class 11 Biology"},
                        {"phase": "Phase 2 (Class 11-12 Transition)", "topics": "Advanced Mechanics, Organic Fundamentals, Calculus, Human Physiology"},
                        {"phase": "Phase 3 (Class 12)", "topics": "Electrodynamics, Optics, Organic Synthesis, Genetics, Class 12 Board Prep"},
                        {"phase": "Phase 4 (Revision)", "topics": "Full Syllabus Mock Tests, Past 10 Years Question Solving, Strategy Workshops"}
                    ],
                    faculties=["Er. Somen Pradhan", "Dr. A. K. Sharma", "Prof. R. C. Verma"],
                    display_order=1
                ),
                Course(
                    slug="qualifier",
                    title="Qualifier Program",
                    badge="Class 12 | 1-Year Program",
                    target="JEE Main & NEET-UG",
                    category="jee",
                    image="assets/images/courses/qualifier.jpg",
                    tagline="1-Year Intensive Program for Class 12 Students",
                    overview="Designed for Class 12 students aiming for high ranks in JEE Main and NEET. It balances board examination syllabus with rapid competitive problem-solving strategies and high-yield topic masterclasses.",
                    duration="1 Year (Class 12)",
                    eligibility="Class 11th Passed / Moving to Class 12th",
                    frequency="5 Days/Week (4 Hours/Day)",
                    highlights=[
                        "Dual Focus on Class 12 Board Exams & JEE/NEET Rank Improvement",
                        "Class 11 Rapid Revision Modules included",
                        "Special Focus on High-Weightage Chapters",
                        "Comprehensive Study Material & Revision Question Banks"
                    ],
                    curriculum=[
                        {"phase": "Phase 1", "topics": "Class 12 Core Concepts & Problem Solving"},
                        {"phase": "Phase 2", "topics": "Class 11 High-Yield Chapter Revisit"},
                        {"phase": "Phase 3", "topics": "Board Exam Mock Tests & Competitive Rank Booster Series"}
                    ],
                    faculties=["Er. Somen Pradhan", "Dr. A. K. Sharma"],
                    display_order=2
                ),
                Course(
                    slug="target",
                    title="Target / Dropper Program",
                    badge="Class 12 Pass | 1-Year Repeater",
                    target="JEE Advanced & NEET-UG Top Ranks",
                    category="jee",
                    image="assets/images/courses/target.jpg",
                    tagline="1-Year Dedicated Rank Improvement Batch for Class 12 Passed Students",
                    overview="An intense, focused 1-year program tailored exclusively for XII passed students aiming to crack top IITs, NITs, and AIIMS. Eliminates foundational gaps and sharpens speed, accuracy, and examination temperament.",
                    duration="1 Year (Repeater / Dropper)",
                    eligibility="Class 12th Passed Students",
                    frequency="6 Days/Week (5 Hours/Day)",
                    highlights=[
                        "Zero-Level to Advanced Conceptual Breakdown",
                        "Over 10,000+ Curated High-Difficulty Practice Questions",
                        "Rigorous Weekly Test Engine with Rank Analytics",
                        "1-on-1 Faculty Mentorship & Doubt Resolution"
                    ],
                    curriculum=[
                        {"phase": "Phase 1", "topics": "Complete Class 11 & 12 Fundamental Masterclasses"},
                        {"phase": "Phase 2", "topics": "Advanced Problem Solving & Multi-Concept Drills"},
                        {"phase": "Phase 3", "topics": "Rank Refinement Test Series & Exam Simulation"}
                    ],
                    faculties=["Er. Somen Pradhan", "Prof. R. C. Verma"],
                    display_order=3
                ),
                Course(
                    slug="pre-foundation",
                    title="Pre-Foundation Program",
                    badge="Class 8, 9 & 10",
                    target="Olympiads, NTSE & Foundation for JEE/NEET",
                    category="foundation",
                    image="assets/images/courses/foundation.jpg",
                    tagline="Early Advantage Program for Classes 8, 9 & 10",
                    overview="Builds strong analytical thinking, logical reasoning, and scientific curiosity early on. Prepares students for School Exams, Olympiads (IJSO, NSO, IMO), and lays the foundation for future competitive success.",
                    duration="1 to 3 Years",
                    eligibility="Students studying in Class 8th, 9th, or 10th",
                    frequency="3 Days/Week (2 Hours/Day)",
                    highlights=[
                        "Strengthens School Science & Mathematics Core Concepts",
                        "Develops Logical Reasoning & Mental Ability Skills",
                        "Special Training for National & International Olympiads",
                        "Interactive Practical Demonstrations & Fun Learning"
                    ],
                    curriculum=[
                        {"phase": "Phase 1", "topics": "School Syllabus Mastery & Conceptual Depth"},
                        {"phase": "Phase 2", "topics": "Mental Ability & Competitive Aptitude Training"},
                        {"phase": "Phase 3", "topics": "Olympiad Level Test Series & Mock Exams"}
                    ],
                    faculties=["Dr. A. K. Sharma"],
                    display_order=4
                ),
                Course(
                    slug="digi-connect",
                    title="Digi-Connect Hybrid",
                    badge="Hybrid / Online",
                    target="Live Online Classes & Doubt Support",
                    category="vst",
                    image="assets/images/courses/digi.jpg",
                    tagline="Learn from Home with Live Interactive Classes & Digital Study Resources",
                    overview="Brings Vidwan's expert classroom pedagogy directly to your home with live interactive lectures, digital notes, recorded video lectures for revision, and online test series.",
                    duration="1 or 2 Years",
                    eligibility="Class 8th to 12th & Dropper Students",
                    frequency="Live Daily Online Sessions + Weekend Doubt Clearance",
                    highlights=[
                        "HD Live Interactive Classes with Chat Doubt Feature",
                        "Instant Recording Access for missed lectures",
                        "Digital Study Material & E-Books",
                        "Online Computer-Based Testing (CBT) Platform"
                    ],
                    curriculum=[
                        {"phase": "Phase 1", "topics": "Live Syllabus Lectures & Interactive E-Notes"},
                        {"phase": "Phase 2", "topics": "Online Sectional & Full Syllabus CBT Tests"}
                    ],
                    faculties=["Er. Somen Pradhan", "Dr. A. K. Sharma"],
                    display_order=5
                ),
                Course(
                    slug="success",
                    title="Success Crash Course",
                    badge="Short-Term Intensive",
                    target="JEE Main & NEET Final Booster",
                    category="jee",
                    image="assets/images/courses/success.jpg",
                    tagline="Short-Term High-Yield Revision & Test Series",
                    overview="A 45-day rapid revision crash course designed to maximize score in the final weeks leading up to JEE Main and NEET. Focuses on formula shortcuts, mock test practice, and error analysis.",
                    duration="45 Days",
                    eligibility="Class 12th Appearing or Passed Students",
                    frequency="Daily 6 Hours Intensive Sessions",
                    highlights=[
                        "Rapid Revision of Top 50 High-Weightage Topics",
                        "15+ Full Syllabus Mock Exams matching actual exam UI",
                        "Shortcuts, Memory Tricks & Time Management Techniques"
                    ],
                    curriculum=[
                        {"phase": "Phase 1", "topics": "Formula Speed Revision & Topic Wise Shortcuts"},
                        {"phase": "Phase 2", "topics": "Daily CBT Mock Tests & Live Error Analysis"}
                    ],
                    faculties=["Er. Somen Pradhan"],
                    display_order=6
                )
            ]
            db.add_all(courses)

        # 3. Seed Initial Faculty if empty
        if db.query(Faculty).count() == 0:
            print("Seeding Initial Faculty...")
            faculties = [
                Faculty(
                    name="Er. Somen Pradhan",
                    designation="Founder & Director (Physics Department)",
                    qualification="B.Tech (IIT), 12+ Yrs Experience",
                    experience="12+ Years Coaching Experience",
                    specialization="Physics for JEE Advanced & NEET",
                    photo="assets/images/faculty/somen_pradhan.jpg",
                    bio="Renowned Physics mentor known for simplifying complex mechanics and electrodynamics concepts. Has mentored over 500+ IITians and top medical rankers.",
                    display_order=1
                ),
                Faculty(
                    name="Dr. A. K. Sharma",
                    designation="Senior Faculty (Chemistry Department)",
                    qualification="Ph.D. Chemistry, M.Sc. (Gold Medalist)",
                    experience="15+ Years Experience",
                    specialization="Organic & Physical Chemistry",
                    photo="assets/images/faculty/sharma.jpg",
                    bio="Expert in Organic Chemistry reaction mechanisms and physical chemistry numericals. Author of multiple competitive chemistry problem books.",
                    display_order=2
                ),
                Faculty(
                    name="Prof. R. C. Verma",
                    designation="Head of Mathematics",
                    qualification="M.Sc. Mathematics, Ex-HOD Premier Institute",
                    experience="14+ Years Experience",
                    specialization="Calculus & Coordinate Geometry",
                    photo="assets/images/faculty/verma.jpg",
                    bio="Master of shortcut methods and problem-solving techniques in Calculus and Algebra. Dedicated to building deep logical clarity.",
                    display_order=3
                )
            ]
            db.add_all(faculties)

        # 4. Seed Initial Results if empty
        if db.query(Result).count() == 0:
            print("Seeding Initial Results...")
            results = [
                Result(
                    student_name="Aarav Sharma",
                    exam="JEE Advanced 2024",
                    rank="AIR 42",
                    year="2024",
                    college="IIT Bombay (Computer Science)",
                    course="Nurture 2-Year Program",
                    achievement="Qualified JEE Advanced with Top AIR 42. Scored 100 percentile in Physics.",
                    photo="assets/images/results/aarav.jpg",
                    badge_class="rank-gold",
                    category="jee",
                    is_featured=True,
                    display_order=1
                ),
                Result(
                    student_name="Priya Patel",
                    exam="NEET UG 2024",
                    rank="AIR 115",
                    year="2024",
                    college="AIIMS New Delhi",
                    course="Target Dropper Program",
                    achievement="Scored 710/720 in NEET UG 2024. Secured admission at AIIMS Delhi.",
                    photo="assets/images/results/priya.jpg",
                    badge_class="rank-gold",
                    category="neet",
                    is_featured=True,
                    display_order=2
                ),
                Result(
                    student_name="Rohan Verma",
                    exam="JEE Main 2024",
                    rank="AIR 189",
                    year="2024",
                    college="IIT Kharagpur",
                    course="Qualifier Program",
                    achievement="99.98 Percentile Overall in JEE Main 2024.",
                    photo="assets/images/results/rohan.jpg",
                    badge_class="rank-silver",
                    category="jee",
                    is_featured=True,
                    display_order=3
                )
            ]
            db.add_all(results)

        # 5. Seed Initial Gallery Items if empty
        if db.query(GalleryItem).count() == 0:
            print("Seeding Initial Gallery Items...")
            gallery_items = [
                GalleryItem(
                    title="Interactive Physics Classroom Session",
                    description="Students engaging in live problem solving at Vidwan Classes classroom.",
                    image_url="assets/images/gallery/classroom1.jpg",
                    category="experience",
                    display_order=1
                ),
                GalleryItem(
                    title="Annual Ranker Felicitations & Award Ceremony",
                    description="Celebrating top rankers of JEE & NEET with parents and faculty.",
                    image_url="assets/images/gallery/ceremony1.jpg",
                    category="our_students",
                    display_order=2
                ),
                GalleryItem(
                    title="Doubt Resolution Counter in Action",
                    description="One-on-one doubt clearing sessions with expert faculty after class.",
                    image_url="assets/images/gallery/doubts.jpg",
                    category="student_reviews",
                    display_order=3
                )
            ]
            db.add_all(gallery_items)

        # 6. Seed Initial Testimonials if empty
        if db.query(Testimonial).count() == 0:
            print("Seeding Initial Testimonials...")
            testimonials = [
                Testimonial(
                    student_name="Aarav Sharma",
                    course="Nurture Program (IIT Bombay CS)",
                    testimonial="The structured material and constant encouragement from Somen Sir and team helped me secure AIR 42 in JEE Advanced. The doubt counters were an absolute game-changer!",
                    rating=5,
                    is_featured=True,
                    is_approved=True
                ),
                Testimonial(
                    student_name="Priya Patel",
                    course="Target Program (AIIMS Delhi)",
                    testimonial="Vidwan Classes provided me the exact focus and exam temperament needed to score 710 in NEET. Regular mock tests perfectly mirrored the actual exam environment.",
                    rating=5,
                    is_featured=True,
                    is_approved=True
                )
            ]
            db.add_all(testimonials)

        db.commit()
        print("Database Seeding Completed Successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
