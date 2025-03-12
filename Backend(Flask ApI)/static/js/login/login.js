//document.addEventListener("DOMContentLoaded", function () {
//    const loginForm = document.getElementById("login-form");
//
//    if (loginForm) {
//        loginForm.addEventListener("submit", async function (event) {
//            event.preventDefault();
//
//            const formData = new FormData(loginForm);
//            const data = {
//                email: formData.get("email"),
//                password: formData.get("password"),
//            };
//
//            try {
//                const response = await fetch("/login", {
//                    method: "POST",
//                    headers: {
//                        "Content-Type": "application/json",
//                    },
//                    body: JSON.stringify(data),
//                });
//
//                const result = await response.json();
//
//                if (response.ok) {
//                    alert(result.message);
//                    window.location.href = result.redirect;
//                } else {
//                    alert(result.error);
//                }
//            } catch (error) {
//                console.error("Error during login:", error);
//                alert("Something went wrong. Please try again.");
//            }
//        });
//    }
//});
