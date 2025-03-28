document.addEventListener("DOMContentLoaded", function () {
    loadCourses();
});

function addCourse() {
    let courseName = document.getElementById("courseName").value;
    if (courseName.trim() === "") {
        alert("Please enter a course name");
        return;
    }
    
    let courses = JSON.parse(localStorage.getItem("courses")) || [];
    courses.push(courseName);
    localStorage.setItem("courses", JSON.stringify(courses));
    
    document.getElementById("courseName").value = "";
    loadCourses();
}

function removeCourse(index) {
    let courses = JSON.parse(localStorage.getItem("courses")) || [];
    courses.splice(index, 1);
    localStorage.setItem("courses", JSON.stringify(courses));
    loadCourses();
}

function loadCourses() {
    let courses = JSON.parse(localStorage.getItem("courses")) || [];
    let teacherCourses = document.getElementById("teacherCourses");
    teacherCourses.innerHTML = "";
    
    courses.forEach((course, index) => {
        let courseDiv = document.createElement("div");
        courseDiv.classList.add("course");
        
        courseDiv.innerHTML = `
            <img src="https://www.flaticon.com/free-icons/computer" alt="Course Icon">
            <span>${course}</span>
            <button class="button continue-btn" onclick="continueCourse('${course}')"  >Continue</button>
            <button class="button remove-btn" onclick="removeCourse(${index})">Remove</button>
            
        `;
        teacherCourses.appendChild(courseDiv);
    });
}

function continueCourse(courseName) {
    
    window.location.href = "{{ url_for('js' , filename='week_s') }}" ;
}
