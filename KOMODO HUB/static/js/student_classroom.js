document.addEventListener("DOMContentLoaded", function () {
    loadCourses();
});

function loadCourses() {
    let courses = JSON.parse(localStorage.getItem("courses")) || [];
    let studentCourses = document.getElementById("studentCourses");
    studentCourses.innerHTML = "";
    
    courses.forEach(course => {
        let courseDiv = document.createElement("div");
        courseDiv.classList.add("course");
        
        courseDiv.innerHTML = `
            <img src="/static/images/images.png" alt="Course">
            <span>${course}</span>
            <button class="button">Continue</button>
        `;
        studentCourses.appendChild(courseDiv);
    });
} 