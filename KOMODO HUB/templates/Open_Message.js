const BoxA = document.getElementById("BoxA");
const btn = document.getElementById("btn");
const openBtn = document.getElementById("PersonA");
const closeBtn = document.getElementById("close");
const modal = document.getElementById("modal");

btn.addEventListener("click", () =>{
    BoxA.classList.add("open");
});
openBtn.addEventListener("click", () => {
    modal.classList.add("open");
});
closeBtn.addEventListener("click", () =>{
    modal.classList.remove("open");
})