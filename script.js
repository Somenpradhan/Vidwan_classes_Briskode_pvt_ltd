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
