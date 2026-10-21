
const registerForm = document.getElementById("register-form");
const message = document.getElementById("message");

registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;

    // Step 1: Check whether passwords match
    if (password !== confirmPassword) {
        message.className = "text-danger mb-3";
        message.textContent = "Passwords do not match.";
        return;
    }

    try {
        // Step 2: Send registration data to Django
        const response = await axios.post(
            "http://127.0.0.1:8000/api/accounts/register/",
            {
                username: username,
                email: email,
                password: password
            }
        );

        // Step 3: Display success message
        message.className = "text-success mb-3";
        message.textContent =
            `Account created successfully for ${response.data.username}!`;

        registerForm.reset();

    } catch (error) {
        // Step 4: Display backend validation errors
        message.className = "text-danger mb-3";

        if (error.response && error.response.data) {
            const errors = error.response.data;

            message.textContent = Object.entries(errors)
                .map(([field, details]) => {
                    const errorText = Array.isArray(details)
                        ? details.join(" ")
                        : typeof details === "object"
                            ? JSON.stringify(details)
                            : details;

                    return `${field}: ${errorText}`;
                })
                .join(" | ");
        } else {
            message.textContent =
                "Unable to connect to the server. Please try again.";
        }

        console.error(error);
    }
});
