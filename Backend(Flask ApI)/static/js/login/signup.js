//document.addEventListener("DOMContentLoaded", function () {
//    const signupForm = document.getElementById("signup-form");
//
//    if (signupForm) {
//        signupForm.addEventListener("submit", async function (event) {
//            event.preventDefault();
//
//            const formData = new FormData(signupForm);
//            const data = {
//                full_name: formData.get("full_name"),
//                email: formData.get("email"),
//                password: formData.get("password"),
//            };
//
//            try {
//                const response = await fetch("/signup", {
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
//                console.error("Error during signup:", error);
//                alert("Something went wrong. Please try again.");
//            }
//        });
//    }
//});
