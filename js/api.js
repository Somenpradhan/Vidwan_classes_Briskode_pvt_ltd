/**
 * Vidwan Classes API Client Utility Module
 * Handles API requests to FastAPI backend with automatic loading indicators and graceful fallback.
 */

const API_BASE_URL = window.VIDWAN_API_URL || "http://localhost:8000/api/v1";

const VidwanAPI = {
    baseUrl: API_BASE_URL,

    async request(endpoint, method = "GET", data = null, headers = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            method,
            headers: {
                "Content-Type": "application/json",
                ...headers
            }
        };

        if (data) {
            config.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, config);
            const resData = await response.json().catch(() => ({}));

            if (!response.ok) {
                const errorMsg = resData.detail || resData.message || "An unexpected error occurred.";
                throw new Error(errorMsg);
            }

            return { success: true, data: resData };
        } catch (error) {
            console.warn(`[VidwanAPI Request Warning] ${method} ${endpoint}:`, error.message);
            return { success: false, error: error.message };
        }
    },

    // --- FORM SUBMISSION ENDPOINTS ---

    // Submit Contact Page Form
    async submitContactForm(formData) {
        return await this.request("/contact", "POST", formData);
    },

    // Submit General Enquiries (Hero, Apply Now, Callback, Demo)
    async submitEnquiry(formData) {
        return await this.request("/enquiries", "POST", formData);
    },

    // Submit VST Scholarship Registration
    async submitVSTRegistration(vstData) {
        return await this.request("/vst/register", "POST", vstData);
    },

    // Submit Newsletter Subscription
    async subscribeNewsletter(email) {
        return await this.request("/newsletter/subscribe", "POST", { email });
    },

    // --- DYNAMIC CONTENT FETCHERS ---

    // Fetch Courses
    async getCourses(category = null) {
        const query = category ? `?category=${category}` : "";
        return await this.request(`/courses${query}`, "GET");
    },

    // Fetch Single Course by slug/id
    async getCourseDetails(idOrSlug) {
        return await this.request(`/courses/${idOrSlug}`, "GET");
    },

    // Fetch Faculty Members
    async getFaculty() {
        return await this.request("/faculty", "GET");
    },

    // Fetch Results/Achievements
    async getResults(category = null) {
        const query = category ? `?category=${category}` : "";
        return await this.request(`/results${query}`, "GET");
    },

    // Fetch Gallery Items
    async getGallery(category = null) {
        const query = category ? `?category=${category}` : "";
        return await this.request(`/gallery${query}`, "GET");
    },

    // Fetch Testimonials
    async getTestimonials() {
        return await this.request("/testimonials", "GET");
    },

    // --- ADMIN API ---

    async adminLogin(username, password) {
        return await this.request("/auth/login/json", "POST", { username, password });
    },

    async getAdminStats(token) {
        return await this.request("/admin/dashboard/stats", "GET", null, {
            "Authorization": `Bearer ${token}`
        });
    },

    async getAdminEnquiries(token, status = "") {
        const query = status ? `?status_filter=${status}` : "";
        return await this.request(`/admin/enquiries${query}`, "GET", null, {
            "Authorization": `Bearer ${token}`
        });
    },

    async updateEnquiryStatus(token, id, newStatus) {
        return await this.request(`/admin/enquiries/${id}`, "PUT", { status: newStatus }, {
            "Authorization": `Bearer ${token}`
        });
    }
};

window.VidwanAPI = VidwanAPI;
