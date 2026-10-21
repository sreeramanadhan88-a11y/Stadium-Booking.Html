
const loginForm = document.getElementById("login-form");
const message = document.getElementById("message");

loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    // Disable button while login is processing
    const loginButton = loginForm.querySelector('button[type="submit"]');
    loginButton.disabled = true;
    loginButton.textContent = "Logging in...";

    try {
        // Send login credentials to Django
        const response = await axios.post(
            "http://127.0.0.1:8000/api/token/",
            {
                username: username,
                password: password
            }
        );

        // Receive JWT tokens
        const accessToken = response.data.access;
        const refreshToken = response.data.refresh;

        // Save tokens
        sessionStorage.setItem("access_token", accessToken);
        sessionStorage.setItem("refresh_token", refreshToken);

        // Fetch the logged-in user's profile
        const profileResponse = await axios.get(
            "http://127.0.0.1:8000/api/accounts/my-profile/",
            {
                headers: {
                    Authorization: `Bearer ${accessToken}`
                }
            }
        );

        console.log("User profile:", profileResponse.data);

        message.className = "text-success mb-3";
        message.textContent = "Login successful!";

        // Check whether the user was trying to book an event
        const pendingScheduleId =
            sessionStorage.getItem("pending_schedule_id");

        if (pendingScheduleId) {
            // Remove the saved schedule ID
            sessionStorage.removeItem("pending_schedule_id");

            // Redirect to the selected booking page
            window.location.href =
                `booking.html?schedule_id=${encodeURIComponent(pendingScheduleId)}`;
        } else {
            // No pending booking: open home page
            window.location.href = "home.html";
        }

    } catch (error) {
        message.className = "text-danger mb-3";

        if (error.response && error.response.status === 401) {
            message.textContent = "Invalid username or password.";
        } else if (error.response && error.response.data) {
            message.textContent = JSON.stringify(error.response.data);
        } else {
            message.textContent =
                "Unable to connect to the server. Please try again.";
        }

        console.error("Login error:", error);

        // Remove tokens if login/profile retrieval failed
        sessionStorage.removeItem("access_token");
        sessionStorage.removeItem("refresh_token");

    } finally {
        loginButton.disabled = false;
        loginButton.textContent = "Login";
    }
});
