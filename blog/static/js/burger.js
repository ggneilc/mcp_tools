const toggle = document.getElementById("nav-toggle");
const panel = document.getElementById("nav-panel");
const closeBtn = document.getElementById("nav-close");

function setOpen(open) {
  if (open) {
    panel.classList.add("open");
    toggle.setAttribute("aria-expanded", "true");
  } else {
    panel.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  }
}

toggle.addEventListener("click", () => {
  setOpen(panel.classList.toggle("open"));
});

closeBtn.addEventListener("click", () => setOpen(false));

// close on Escape
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && panel.classList.contains("open")) {
    setOpen(false);
    toggle.focus();
  }
});

// optional: close if clicked outside nav-panel
document.addEventListener("click", (e) => {
  if (!panel.contains(e.target) && !toggle.contains(e.target)) {
    setOpen(false);
  }
});
