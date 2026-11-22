const toggle = document.querySelector("#theme");

function applyTheme(dark) {
  document.documentElement.classList.toggle("dark", dark);
  toggle.textContent = dark ? "Mode clair" : "Mode sombre";
}

let saved;
try { saved = localStorage.getItem("mode"); } catch {}
applyTheme(saved ? saved === "sombre" : window.matchMedia("(prefers-color-scheme: dark)").matches);
toggle.hidden = false;
toggle.addEventListener("click", () => {
  const dark = !document.documentElement.classList.contains("dark");
  applyTheme(dark);
  try { localStorage.setItem("mode", dark ? "sombre" : "clair"); } catch {}
});
