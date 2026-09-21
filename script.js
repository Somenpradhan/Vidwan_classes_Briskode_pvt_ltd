/* ==========================================================================
   Vidwan Classes - Interactive JavaScript Engine
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initBannerSlider();
    initCounters();
    initCourseFilter();
    initResultFilter();
    initCountdown();
    initModals();
    initCourseDetailsPage();
    highlightActiveNav();
});

/* 0. Photo Banner Scrolling Slider */
let currentSlide = 0;
let sliderInterval = null;

function initBannerSlider() {
    const track = document.getElementById('bannerTrack');
    const slides = document.querySelectorAll('.banner-slide');
    const dots = document.querySelectorAll('.dot-indicator');
    const prevBtn = document.getElementById('sliderPrev');
    const nextBtn = document.getElementById('sliderNext');
    const container = document.querySelector('.banner-slider-container');

    if (!track || slides.length === 0) return;

    function updateSlider(index) {
        currentSlide = (index + slides.length) % slides.length;
        track.style.transform = `translateX(-${currentSlide * 100}%)`;
        
        dots.forEach((dot, i) => {
            if (i === currentSlide) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }

    window.goToSlide = (i) => {
        updateSlider(i);
        restartAutoPlay();
    };

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            updateSlider(currentSlide - 1);
            restartAutoPlay();
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            updateSlider(currentSlide + 1);
            restartAutoPlay();
        });
    }

    function startAutoPlay() {
        if (!sliderInterval) {
            sliderInterval = setInterval(() => {
                updateSlider(currentSlide + 1);
            }, 3500);
        }
    }

    function stopAutoPlay() {
        if (sliderInterval) {
            clearInterval(sliderInterval);
            sliderInterval = null;
        }
    }

    function restartAutoPlay() {
        stopAutoPlay();
        startAutoPlay();
    }

    if (container) {
        container.addEventListener('mouseenter', stopAutoPlay);
        container.addEventListener('mouseleave', startAutoPlay);
    }

    startAutoPlay();
}

/* 1. Sticky Navigation & Mobile Toggle */
function initNavigation() {
    const navbar = document.getElementById('navbar');
    const mobileToggle = document.getElementById('mobileMenuToggle');
    const navMenu = document.getElementById('navMenu');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        highlightNavOnScroll();
    });

    if (mobileToggle && navMenu) {
        mobileToggle.addEventListener('click', () => {
            navMenu.classList.toggle('mobile-active');
            const icon = mobileToggle.querySelector('i');
            if (navMenu.classList.contains('mobile-active')) {
                icon.className = 'ri-close-line';
            } else {
                icon.className = 'ri-menu-3-line';
            }
        });

        // Close menu on link click
        navMenu.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('mobile-active');
                if (mobileToggle.querySelector('i')) {
                    mobileToggle.querySelector('i').className = 'ri-menu-3-line';
                }
            });
        });
    }
}

function highlightNavOnScroll() {
    const sections = document.querySelectorAll('section[id]');
    const scrollY = window.pageYOffset;

    sections.forEach(current => {
        const sectionHeight = current.offsetHeight;
        const sectionTop = current.offsetTop - 100;
        const sectionId = current.getAttribute('id');
        const navLink = document.querySelector(`.nav-menu a[href*=${sectionId}]`);

        if (navLink) {
            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                navLink.classList.add('active');
            } else {
                navLink.classList.remove('active');
            }
        }
    });
}

/* 2. Stat Counter Animation */
function initCounters() {
    const counters = document.querySelectorAll('.counter');
    let animated = false;

    const animateOnScroll = () => {
        const statSection = document.querySelector('.stat-strip');
        if (!statSection) return;

        const pos = statSection.getBoundingClientRect().top;
        const winHeight = window.innerHeight;

        if (pos < winHeight && !animated) {
            animated = true;
            counters.forEach(counter => {
                const target = +counter.getAttribute('data-target');
                const duration = 2000;
                const increment = target / (duration / 16);

                let current = 0;
                const updateCount = () => {
                    current += increment;
                    if (current < target) {
                        counter.innerText = Math.ceil(current) + (target === 73 ? '%' : '+');
                        requestAnimationFrame(updateCount);
                    } else {
                        counter.innerText = target + (target === 73 ? '%' : '+');
                    }
                };
                updateCount();
            });
        }
    };

    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Trigger check initially
}

/* 3. Course Filter Tabs */
function initCourseFilter() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const courseCards = document.querySelectorAll('.course-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filterValue = btn.getAttribute('data-filter');
            filterCourses(filterValue);
        });
    });
}

function filterCourses(category) {
    const courseCards = document.querySelectorAll('.course-card');
    courseCards.forEach(card => {
        const cardCat = card.getAttribute('data-category');
        if (category === 'all' || cardCat.includes(category)) {
            card.style.display = 'flex';
            card.style.animation = 'fadeIn 0.4s ease';
        } else {
            card.style.display = 'none';
        }
    });
}

/* 4. Result / Hall of Fame Filter */
function initResultFilter() {
    const filterBtns = document.querySelectorAll('.result-filter-btn');
    const rankerCards = document.querySelectorAll('.ranker-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filterValue = btn.getAttribute('data-resfilter');
            rankerCards.forEach(card => {
                const cardCat = card.getAttribute('data-category');
                if (filterValue === 'all' || cardCat === filterValue) {
                    card.style.display = 'block';
                    card.style.animation = 'fadeIn 0.4s ease';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

/* 5. Smart Course Finder Wizard Logic */
const wizardSelection = {
    class: '',
    goal: '',
    mode: ''
};

function selectWizardOption(step, key, val) {
    wizardSelection[key] = val;

    const currentStepEl = document.getElementById(`step-${step}`);
    const nextStepEl = document.getElementById(`step-${step + 1}`);

    const currentDot = document.getElementById(`dot-${step}`);
    const nextDot = document.getElementById(`dot-${step + 1}`);

    if (currentStepEl) currentStepEl.classList.remove('active');

    if (step < 3) {
        if (nextStepEl) nextStepEl.classList.add('active');
        if (nextDot) nextDot.classList.add('active');
    } else {
        // Show result
        const resultStep = document.getElementById('step-result');
        if (resultStep) resultStep.classList.add('active');
        calculateWizardRecommendation();
    }
}

function calculateWizardRecommendation() {
    const container = document.getElementById('wizardResultContainer');
    if (!container) return;

    let programTitle = "NURTURE Integrated 2-Year Program";
    let desc = "Ideal 2-year classroom course for Class 11 students aiming for top ranks in IIT-JEE & NEET along with CBSE Board excellence.";

    if (wizardSelection.class === '6-8' || wizardSelection.class === '9-10' || wizardSelection.goal === 'olympiad') {
        programTitle = "PRE-FOUNDATION & OLYMPIAD BATCH";
        desc = "Specially structured to build early problem-solving skills for Class 6th to 10th students targeting NTSE, Olympiads & early JEE/NEET grounding.";
    } else if (wizardSelection.class === '12') {
        programTitle = "TARGET / QUALIFIER INTENSIVE BATCH";
        desc = "Dedicated fast-track batch engineered for Class 12 & Dropper students focusing on rank booster problem solving and mock tests.";
    } else if (wizardSelection.mode === 'digital') {
        programTitle = "DIGI-CONNECT DISTANCE PROGRAM";
        desc = "Interactive live online classes, digital smart study material, and real-time doubt resolution from anywhere in India.";
    }

    container.innerHTML = `
        <div class="rec-badge"><i class="ri-sparkles-line"></i> RECOMMENDED PATHWAY</div>
        <h3 class="rec-title">${programTitle}</h3>
        <p style="color: var(--text-secondary); max-width: 600px; margin: 0 auto 1.5rem auto;">${desc}</p>
        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
            <button class="btn btn-primary glow-btn" onclick="openApplyModalFor('${programTitle}')">
                <i class="ri-send-plane-fill"></i> Enroll in ${programTitle}
            </button>
            <button class="btn btn-outline" onclick="resetWizard()">
                <i class="ri-refresh-line"></i> Restart Finder
            </button>
        </div>
    `;
}

function resetWizard() {
    wizardSelection.class = '';
    wizardSelection.goal = '';
    wizardSelection.mode = '';

    document.querySelectorAll('.wizard-step-content').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.step-dot').forEach(d => d.classList.remove('active'));

    document.getElementById('step-1').classList.add('active');
    document.getElementById('dot-1').classList.add('active');
}

/* 6. VST Countdown Timer */
function initCountdown() {
    // Set deadline 5 days from now
    const targetDate = new Date().getTime() + (5 * 24 * 60 * 60 * 1000);

    setInterval(() => {
        const now = new Date().getTime();
        const difference = targetDate - now;

        if (difference > 0) {
            const days = Math.floor(difference / (1000 * 60 * 60 * 24));
            const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((difference % (1000 * 60)) / 1000);

            if (document.getElementById('days')) document.getElementById('days').innerText = String(days).padStart(2, '0');
            if (document.getElementById('hours')) document.getElementById('hours').innerText = String(hours).padStart(2, '0');
            if (document.getElementById('minutes')) document.getElementById('minutes').innerText = String(minutes).padStart(2, '0');
            if (document.getElementById('seconds')) document.getElementById('seconds').innerText = String(seconds).padStart(2, '0');
        }
    }, 1000);
}

/* 7. Instant Scholarship Fee Estimator */
function updateScholarshipCalc(score) {
    const scoreVal = document.getElementById('scoreVal');
    const scholarshipPercent = document.getElementById('scholarshipPercent');
    if (scoreVal) scoreVal.innerText = `${score}%`;

    let waiver = 25;
    if (score >= 95) waiver = 90;
    else if (score >= 90) waiver = 75;
    else if (score >= 80) waiver = 50;
    else if (score >= 70) waiver = 35;

    if (scholarshipPercent) {
        scholarshipPercent.innerText = `${waiver}% Scholarship`;
    }
}

/* 8. Modal Controller */
function initModals() {
    const applyModal = document.getElementById('applyModal');
    const callbackModal = document.getElementById('callbackModal');
    const syllabusModal = document.getElementById('syllabusModal');

    document.getElementById('openApplyModal')?.addEventListener('click', () => openModal('applyModal'));
    document.getElementById('openCallbackModal')?.addEventListener('click', () => openModal('callbackModal'));
    document.getElementById('openBrochureBtn')?.addEventListener('click', () => openModal('applyModal'));
    document.getElementById('openDemoBtn')?.addEventListener('click', () => openModal('applyModal'));

    // Close on backdrop click
    document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
        backdrop.addEventListener('click', (e) => {
            if (e.target === backdrop) {
                backdrop.classList.remove('active');
            }
        });
    });
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.add('active');
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('active');
}

function openApplyModalFor(courseName) {
    openModal('applyModal');
    const courseSelect = document.getElementById('modalSelectedCourse');
    if (courseSelect) {
        for (let i = 0; i < courseSelect.options.length; i++) {
            if (courseSelect.options[i].text.toLowerCase().includes(courseName.toLowerCase()) || courseSelect.options[i].value === courseName) {
                courseSelect.selectedIndex = i;
                break;
            }
        }
    }
}

function openVSTModal() {
    openApplyModalFor('VST Scholarship Test');
}

function openSyllabusModal(programName) {
    const title = document.getElementById('syllabusModalTitle');
    const body = document.getElementById('syllabusModalBody');

    if (title) title.innerText = `${programName} - Syllabus & Course Structure`;
    if (body) {
        body.innerHTML = `
            <p><strong>Target Objective:</strong> Complete mastery of Class 11 & 12 board curriculum + competitive problem solving for IIT-JEE / NEET.</p>
            
            <h4>Physics Coverage</h4>
            <ul>
                <li>Mechanics, Kinematics, Laws of Motion & Energy</li>
                <li>Electrostatics, Magnetism, Optics & Modern Physics</li>
            </ul>

            <h4>Chemistry Coverage</h4>
            <ul>
                <li>Physical Chemistry: Thermodynamics, Equilibrium, Kinetics</li>
                <li>Organic & Inorganic Chemistry: Reaction Mechanisms, Periodic Table</li>
            </ul>

            <h4>Mathematics / Biology Coverage</h4>
            <ul>
                <li>Math: Calculus, Algebra, Coordinate Geometry, Vectors 3D</li>
                <li>Biology: Cell Structure, Plant & Human Physiology, Genetics</li>
            </ul>

            <h4 style="margin-top: 1rem;">Batch Schedule & Details</h4>
            <p>• 6 Days / Week Regular Classroom Coaching<br>
            • Daily 3 Hours Lectures + 1 Hour Doubt Clearing<br>
            • Weekly OMR & Online CBT Computer Based Tests</p>
        `;
    }
    openModal('syllabusModal');
}

/* 9. FAQ Accordion Toggle */
function toggleFaq(buttonEl) {
    const item = buttonEl.parentElement;
    const isActive = item.classList.contains('active');

    document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('active'));

    if (!isActive) {
        item.classList.add('active');
    }
}

/* 10. Form Submission Toast Handlers */
function handleFormSubmit(e, formName) {
    e.preventDefault();
    showToast(`Success! Your ${formName} has been submitted. Our senior counselor will contact you shortly.`);

    // Reset forms and close modal if open
    e.target.reset();
    document.querySelectorAll('.modal-backdrop').forEach(m => m.classList.remove('active'));
}

function handleNewsletter(e) {
    e.preventDefault();
    showToast(`Thank you! You have successfully subscribed to Vidwan Exam Alerts.`);
    e.target.reset();
}

function downloadResource(fileName) {
    showToast(`Preparing download for ${fileName}. PDF download starting now!`);
}

function showToast(message) {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<i class="ri-checkbox-circle-fill" style="color: var(--emerald); font-size: 1.25rem;"></i> <span>${message}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(-100%)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

/* 11. Route Active Link Highlight */
function highlightActiveNav() {
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-menu .nav-link');

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (!href) return;
        const pageName = href.split('#')[0].split('/').pop();
        
        if (pageName === currentPath || (currentPath === 'index.html' && (pageName === '' || pageName === '#hero'))) {
            link.classList.add('active');
        } else if (pageName && currentPath.includes(pageName) && pageName !== 'index.html' && pageName !== '#') {
            link.classList.add('active');
        }
    });
}

/* 12. Dynamic Course Details Data Store & Renderer */
const COURSES_DATA = {
    nurture: {
        id: 'nurture',
        title: 'NURTURE PROGRAM',
        badge: '2-Year Integrated Course',
        target: 'Class XI Students Moving to Class XII',
        category: 'IIT-JEE (Main & Adv) / NEET Medical',
        image: 'assets/course_nurture.png',
        tagline: 'Comprehensive 2-Year Integrated Classroom Foundation for IIT-JEE & NEET with Complete CBSE Board Mastery.',
        overview: `The <strong>Nurture Program</strong> is meticulously engineered for Class 11 students aspiring to crack IIT-JEE (Main & Advanced) or NEET with top All India Ranks. Over two academic years, students undergo step-by-step conceptual mastering in Physics, Chemistry, and Mathematics/Biology, perfectly synchronized with their XI & XII CBSE Board school curriculum.`,
        duration: '2 Academic Years (2026 - 2028)',
        eligibility: 'Class X Passed / Appearing Students',
        frequency: '4 to 5 Days a Week (3 Hours/Day) + Sunday AITS Test',
        highlights: [
            '100% Concept Building from Fundamentals to Advanced Rank Level',
            'Synchronized CBSE / NCERT Board Syllabus Preparation',
            'Weekly All India Test Series (AITS) with All India Rank Analysis',
            'Exclusive 1-on-1 Daily Faculty Doubt Clearing Desks',
            'Complete Hardcopy Printed Study Modules & Micro Problem Sets'
        ],
        curriculum: [
            {
                subject: 'Physics',
                topics: 'Kinematics, Laws of Motion, Work Energy & Power, Rotational Dynamics, Gravitation, Thermodynamics, Electrostatics, Magnetism, Ray Optics & Modern Physics.'
            },
            {
                subject: 'Chemistry',
                topics: 'Atomic Structure, Chemical Bonding, Gaseous State, Thermodynamics, Equilibrium, Organic Chemistry Fundamentals, Hydrocarbons, Coordination Chemistry & Metallurgy.'
            },
            {
                subject: 'Mathematics / Biology',
                topics: 'Algebra, Trigonometry, Calculus, Coordinate Geometry, Vectors & 3D / Diversity in Living World, Cell Biology, Human Physiology, Genetics & Biotechnology.'
            }
        ],
        faculties: ['Er. S. Malla (IIT Kharagpur Alumnus)', 'Dr. P. Dash (Senior AIIMS Medical Mentor)', 'Er. R. K. Mohapatra (Senior Physics Specialist)']
    },
    digiconnect: {
        id: 'digiconnect',
        title: 'DIGI-CONNECT PROGRAM',
        badge: 'Online & Distance Learning',
        target: 'Class 6th to 12th & Dropper Students',
        category: 'Interactive Hybrid / Live Classes',
        image: 'assets/course_digiconnect.png',
        tagline: 'State-of-the-Art Digital Smart Classroom Experience with Live Interactive Classes & Real-Time Analytics.',
        overview: `<strong>Digi-Connect</strong> brings Vidwan Classes\' top-tier IITian & Doctor faculty team directly to your home. Designed for outstation students and self-paced learners, it delivers HD live classes, instant chat doubt resolution, smart digital study notebooks, and full access to recorded backups.`,
        duration: '1 Year / 2 Year Flexible Options',
        eligibility: 'Class VI to XII & Passed Students',
        frequency: 'Live Daily Evening Classes + 24/7 Recorded Library Access',
        highlights: [
            'Live Interactive HD Lectures with Real-Time Q&A',
            'Unlimited Access to Recorded Video Library & Class Notes',
            'Automated Computer-Based Test (CBT) Series & Analytics',
            '1-on-1 Video Call Doubt Clarification Slots',
            'Home Delivery of Printed Study Material Package'
        ],
        curriculum: [
            {
                subject: 'Physics',
                topics: 'Core syllabus tailored to target exam (Olympiad, NTSE, JEE, or NEET).'
            },
            {
                subject: 'Chemistry & Biology',
                topics: 'Comprehensive NCERT + Competitive Level online lectures and periodic drills.'
            },
            {
                subject: 'Mathematics & Aptitude',
                topics: 'Analytical problem solving, mental ability drills, and test-taking strategies.'
            }
        ],
        faculties: ['Er. A. K. Swain (Digital Academic Lead)', 'Dr. M. Priyadarshini (NEET Biology Expert)', 'Er. B. B. Sahoo (Maths Wizard)']
    },
    success: {
        id: 'success',
        title: 'SUCCESS PROGRAM',
        badge: 'Class XI Advance Batch',
        target: 'Class XI Students Aiming For Early Competitive Lead',
        category: 'IIT-JEE & NEET Special Fast-Track',
        image: 'assets/course_success.png',
        tagline: 'Accelerated Learning Module Covering Core Class XI Fundamentals with Early Advanced Problem Drills.',
        overview: `The <strong>Success Program</strong> is crafted for ambitious Class 11 students who want to build early momentum. It covers foundational topics rapidly and moves quickly into high-difficulty JEE Advanced and NEET question-solving patterns.`,
        duration: '2 Academic Years',
        eligibility: 'Class X High Achievers (Above 85% Marks)',
        frequency: '5 Days a Week + Special Weekend Rankers Workshop',
        highlights: [
            'Advanced Multi-Concept Problem Solving Techniques',
            'Analysis of 20+ Years Past Examination Questions (PYQs)',
            'Special Focus on Physics Numerical Rigor & Organic Mechanisms',
            'Personal Mentorship by Founder Faculties'
        ],
        curriculum: [
            {
                subject: 'Advanced Physics',
                topics: 'Rotational Motion, Fluid Mechanics, Waves, Electrodynamics & Quantum Physics.'
            },
            {
                subject: 'Advanced Chemistry',
                topics: 'Physical Chemistry Thermodynamics, Reaction Mechanisms & Inorganic Complexes.'
            },
            {
                subject: 'Advanced Mathematics',
                topics: 'Permutations & Combinations, Complex Numbers, Differential Calculus, Integral Calculus.'
            }
        ],
        faculties: ['Er. S. Malla (Chief Mentor)', 'Er. R. K. Mohapatra (Head of Physics)', 'Dr. P. Dash (Medical Lead)']
    },
    qualifier: {
        id: 'qualifier',
        title: 'QUALIFIER PROGRAM',
        badge: '1-Year Intensive Course',
        target: 'Class XII Students',
        category: 'IIT-JEE / NEET + Class 12 Boards',
        image: 'assets/course_nurture.png',
        tagline: 'Power-Packed 1-Year Course Synchronizing Class XII Board Syllabus with Complete Competitive Entrance Preparation.',
        overview: `The <strong>Qualifier Program</strong> is designed for Class 12 students to master their final board exams while concurrently revising Class 11 concepts and solving full-length competitive mock papers for JEE Main, Advanced, and NEET.`,
        duration: '1 Academic Year (2026 - 2027)',
        eligibility: 'Class XI Passed Students',
        frequency: '5 Days a Week (3.5 Hours/Day)',
        highlights: [
            'Complete Coverage of Class 12 Syllabus by November',
            'Dedicated Class 11 Revision Drills from December to January',
            'Intensive Full-Syllabus Mock Test Series (AITS)',
            'Board Exam Answer Writing Practice & Practical Lab Guidance'
        ],
        curriculum: [
            {
                subject: 'Physics',
                topics: 'Electrostatics, Current Electricity, Optics, Magnetism, Semiconductors, Electromagnetic Waves.'
            },
            {
                subject: 'Chemistry',
                topics: 'Electrochemistry, Chemical Kinetics, Biomolecules, Haloalkanes, Aldehydes & Ketones.'
            },
            {
                subject: 'Mathematics / Biology',
                topics: 'Calculus, Matrices, Vectors, Probability / Reproduction, Genetics, Human Welfare.'
            }
        ],
        faculties: ['Er. B. B. Sahoo (Maths Lead)', 'Dr. M. Priyadarshini (Senior Medical Mentor)', 'Er. A. K. Swain (Physics Expert)']
    },
    target: {
        id: 'target',
        title: 'TARGET PROGRAM (DROPPER BATCH)',
        badge: 'Dropper / Repeater Special',
        target: 'Class XII Passed Students Taking a Gap Year',
        category: 'Rank Maximization Batch for JEE & NEET',
        image: 'assets/course_success.png',
        tagline: 'Uncompromising 1-Year Dedicated Rank Booster Course for Repeaters & Gap-Year Aspirants.',
        overview: `The <strong>Target Program</strong> is an intensive 1-year course for XII passed students who wish to dedicate a focused year to rank enhancement. Operating with extended classroom hours and daily test drills, it transforms gaps into top ranks.`,
        duration: '1 Year (Targeting 2027 Entrance)',
        eligibility: 'Class XII Passed Students',
        frequency: '6 Days a Week (5-6 Hours Daily Intensive Sessions)',
        highlights: [
            'Daily Practice Problems (DPP) & Instant Doubt Solving',
            'Speed, Accuracy & Negative Marking Reduction Strategies',
            'Over 60+ Full-Length CBT & OMR Mock Tests',
            'Exclusive Small Batch Size for Maximum Individual Care'
        ],
        curriculum: [
            {
                subject: 'Physics Mastery',
                topics: 'Full XI & XII Competitive Physics syllabus with extreme problem variety.'
            },
            {
                subject: 'Chemistry Mastery',
                topics: 'Integrated Physical, Organic, and Inorganic Chemistry with reaction drills.'
            },
            {
                subject: 'Maths / Biology Mastery',
                topics: 'Complete entrance syllabus with shortcut tricks and time management tactics.'
            }
        ],
        faculties: ['Er. S. Malla (IIT Kharagpur)', 'Er. R. K. Mohapatra', 'Dr. P. Dash', 'Er. B. B. Sahoo']
    },
    prefoundation: {
        id: 'prefoundation',
        title: 'PRE-FOUNDATION PROGRAM',
        badge: 'Class 6th to 10th Foundation',
        target: 'Students in Class VI, VII, VIII, IX & X',
        category: 'Olympiad, NTSE, JMO & STEM Foundation',
        image: 'assets/course_foundation.png',
        tagline: 'Nurturing Scientific Curiosity, Analytical Thinking, and Early Mastery for Future JEE/NEET Rankers.',
        overview: `The <strong>Pre-Foundation Program</strong> lays a rock-solid base in Science, Mathematics, Mental Ability, and Logical Reasoning. It prepares junior students to excel in school exams while competing confidently in NTSE, Olympiads (NSEP, NSEC, NSEB, INMO), and KVPY.`,
        duration: '1 Year / 2 Year Programs per Class',
        eligibility: 'Students entering Class 6th to 10th',
        frequency: '3 to 4 Days a Week (2 Hours/Day)',
        highlights: [
            'Deep Conceptual Clarity in Physics, Chemistry, Biology & Maths',
            'Special Logical Reasoning & Aptitude Development Sessions',
            'Olympiad & NTSE Specialized Practice Question Sets',
            'School Exam Top Performance Assurance'
        ],
        curriculum: [
            {
                subject: 'Science (Physics, Chemistry, Biology)',
                topics: 'Motion, Light, Sound, Matter, Acids & Bases, Cell structure, Plant & Human Life.'
            },
            {
                subject: 'Mathematics',
                topics: 'Number Systems, Geometry, Mensuration, Linear Equations, Polynomials, Trigonometry.'
            },
            {
                subject: 'Mental Ability (MAT)',
                topics: 'Verbal & Non-Verbal Reasoning, Coding-Decoding, Series, Pattern Recognition.'
            }
        ],
        faculties: ['Er. A. K. Swain (Foundation Lead)', 'Dr. M. Priyadarshini (Junior Science Mentor)']
    }
};

function initCourseDetailsPage() {
    const container = document.getElementById('courseDetailContainer');
    if (!container) return;

    const urlParams = new URLSearchParams(window.location.search);
    const courseId = urlParams.get('id') || 'nurture';
    const course = COURSES_DATA[courseId.toLowerCase()] || COURSES_DATA['nurture'];

    // Update document title and breadcrumb
    document.title = `${course.title} | Vidwan Classes`;
    const breadcrumbCourseName = document.getElementById('breadcrumbCourseName');
    if (breadcrumbCourseName) breadcrumbCourseName.textContent = course.title;

    // Render course detail HTML
    container.innerHTML = `
        <div class="course-detail-header glass-panel">
            <div class="cd-grid">
                <div class="cd-main">
                    <span class="banner-badge gold-badge"><i class="ri-graduation-cap-fill"></i> ${course.badge}</span>
                    <h1 class="cd-title">${course.title}</h1>
                    <p class="cd-tagline">${course.tagline}</p>
                    <div class="cd-meta-row">
                        <div class="cd-meta"><i class="ri-calendar-event-line"></i> <strong>Duration:</strong> ${course.duration}</div>
                        <div class="cd-meta"><i class="ri-user-star-line"></i> <strong>Eligibility:</strong> ${course.eligibility}</div>
                        <div class="cd-meta"><i class="ri-time-line"></i> <strong>Class Frequency:</strong> ${course.frequency}</div>
                    </div>
                    <div class="cd-cta-group">
                        <button class="btn btn-primary glow-btn btn-lg" onclick="openApplyModalFor('${course.id.toUpperCase()}')">
                            <i class="ri-edit-box-line"></i> Apply For ${course.title}
                        </button>
                        <button class="btn btn-outline btn-lg" onclick="openSyllabusModal('${course.title}')">
                            <i class="ri-file-download-line"></i> Download Detailed Syllabus
                        </button>
                    </div>
                </div>
                <div class="cd-image-box">
                    <img src="${course.image}" alt="${course.title}">
                    <div class="cd-quick-card">
                        <i class="ri-shield-check-fill" style="color: var(--gold); font-size: 1.5rem;"></i>
                        <div>
                            <h4>Guaranteed Mentorship</h4>
                            <p>Taught by Senior IITian & Doctor Faculty</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="cd-content-grid">
            <div class="cd-left-column">
                <div class="cd-section-card glass-panel">
                    <h3><i class="ri-book-read-line"></i> Program Overview</h3>
                    <p class="cd-body-text">${course.overview}</p>
                </div>

                <div class="cd-section-card glass-panel">
                    <h3><i class="ri-star-line"></i> Key Features & Benefits</h3>
                    <ul class="cd-feature-list">
                        ${course.highlights.map(h => `<li><i class="ri-checkbox-circle-fill" style="color: var(--cyan-glow);"></i> <span>${h}</span></li>`).join('')}
                    </ul>
                </div>

                <div class="cd-section-card glass-panel">
                    <h3><i class="ri-list-check-3"></i> Subject-Wise Curriculum Coverage</h3>
                    <div class="curriculum-accordion">
                        ${course.curriculum.map((curr, i) => `
                            <div class="curriculum-box">
                                <h4><i class="ri-bookmark-3-fill" style="color: var(--amber-orange);"></i> ${curr.subject}</h4>
                                <p>${curr.topics}</p>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div class="cd-section-card glass-panel">
                    <h3><i class="ri-team-line"></i> Assigned Lead Faculty Team</h3>
                    <ul class="cd-faculty-list">
                        ${course.faculties.map(fac => `<li><i class="ri-user-follow-line" style="color: var(--emerald);"></i> ${fac}</li>`).join('')}
                    </ul>
                </div>
            </div>

            <div class="cd-right-column">
                <div class="cd-sidebar-card glass-panel sticky-sidebar">
                    <h3><i class="ri-calculator-line"></i> Quick Admission & Fee Aid</h3>
                    <p>Register for Vidwan Talent Search Test (VST 2026) to claim up to <strong>90% scholarship</strong> on this course!</p>
                    
                    <div class="sidebar-stat">
                        <span class="lbl">Available Modes:</span>
                        <span class="val">Classroom & Digi-Connect</span>
                    </div>
                    <div class="sidebar-stat">
                        <span class="lbl">Campus Location:</span>
                        <span class="val">Bhubaneswar Centre</span>
                    </div>

                    <a href="vst.html" class="btn btn-gold btn-block glow-btn margin-top-1">
                        <i class="ri-flashlight-fill"></i> Check VST Scholarship Waiver
                    </a>

                    <button class="btn btn-secondary btn-block margin-top-1" onclick="openModal('callbackModal')">
                        <i class="ri-customer-service-2-line"></i> Speak To Program Director
                    </button>
                </div>
    `;
}

/* 13. Gallery Page Interactive Engine */
function openLightbox(imgSrc, captionText) {
    const modal = document.getElementById('galleryLightbox');
    const img = document.getElementById('lightboxImg');
    const caption = document.getElementById('lightboxCaption');
    if (!modal || !img || !caption) return;

    img.src = imgSrc;
    caption.textContent = captionText;
    modal.classList.add('active');
}

function closeLightbox() {
    const modal = document.getElementById('galleryLightbox');
    if (modal) modal.classList.remove('active');
}

function filterGallery(category, buttonEl) {
    const filterBtns = document.querySelectorAll('#experienceFilter .filter-btn');
    filterBtns.forEach(btn => btn.classList.remove('active'));
    if (buttonEl) buttonEl.classList.add('active');

    const items = document.querySelectorAll('#experienceGrid .gallery-item');
    items.forEach(item => {
        const itemCat = item.getAttribute('data-category');
        if (category === 'all' || itemCat === category) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}

/* Testimonial Slider Engine */
let currentTestimonialIndex = 0;

function updateTestimonialSlider(index) {
    const slides = document.querySelectorAll('.testimonial-slide');
    const dots = document.querySelectorAll('.t-dot');
    if (slides.length === 0) return;

    currentTestimonialIndex = (index + slides.length) % slides.length;

    slides.forEach((slide, i) => {
        if (i === currentTestimonialIndex) {
            slide.classList.add('active');
        } else {
            slide.classList.remove('active');
        }
    });

    dots.forEach((dot, i) => {
        if (i === currentTestimonialIndex) {
            dot.classList.add('active');
        } else {
            dot.classList.remove('active');
        }
    });
}

function nextTestimonial() {
    updateTestimonialSlider(currentTestimonialIndex + 1);
}

function prevTestimonial() {
    updateTestimonialSlider(currentTestimonialIndex - 1);
}

function goToTestimonial(index) {
    updateTestimonialSlider(index);
}

/* Student Photo Gallery Carousel Engine */
let studentCarouselPosition = 0;

function scrollStudentCarousel(direction) {
    const track = document.getElementById('studentCarouselTrack');
    if (!track) return;

    const cards = track.querySelectorAll('.student-card-item');
    if (cards.length === 0) return;

    const cardWidth = cards[0].offsetWidth + 24; // Width + gap
    const maxScroll = (cards.length - 4) * cardWidth;

    studentCarouselPosition += direction * cardWidth;

    if (studentCarouselPosition < 0) studentCarouselPosition = 0;
    if (studentCarouselPosition > maxScroll && maxScroll > 0) studentCarouselPosition = maxScroll;

    track.style.transform = `translateX(-${studentCarouselPosition}px)`;
}


