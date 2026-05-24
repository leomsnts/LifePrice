const RESPONSIVE_WIDTH = 1024;

if (localStorage.getItem("color-mode") === "dark" ||
    (!("color-mode" in localStorage) && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
    document.documentElement.classList.add("tw-dark");
} else {
    document.documentElement.classList.remove("tw-dark");
}
updateToggleModeBtn();

function toggleMode() {
    document.documentElement.classList.toggle("tw-dark");
    updateToggleModeBtn();
}

function updateToggleModeBtn() {
    const icon = document.querySelector("#toggle-mode-icon");
    if (!icon) return;

    if (document.documentElement.classList.contains("tw-dark")) {
        icon.classList.remove("bi-sun");
        icon.classList.add("bi-moon");
        localStorage.setItem("color-mode", "dark");
    } else {
        icon.classList.add("bi-sun");
        icon.classList.remove("bi-moon");
        localStorage.setItem("color-mode", "light");
    }
}

// No celular os atalhos ficam logo acima da caixa de digitar.
// No desktop eles voltam pra coluna da esquerda, como sempre.
function ajustarBotoesMobile() {
    const win = document.querySelector(".lp-window");
    const aside = document.querySelector(".lp-sidebar");
    const terminal = document.getElementById("terminal");
    const form = document.getElementById("cmd-form");
    if (!win || !aside || !terminal || !form) return;

    if (window.innerWidth < RESPONSIVE_WIDTH) {
        if (aside.parentElement !== terminal) terminal.insertBefore(aside, form);
    } else {
        if (aside.parentElement !== win) win.insertBefore(aside, terminal);
    }
}

window.addEventListener("resize", ajustarBotoesMobile);
ajustarBotoesMobile();

window.addEventListener("load", initAnimations);

function initAnimations() {

    if (typeof gsap === "undefined") {
        document.querySelectorAll(".reveal-up").forEach((e) => { e.style.opacity = 1; });
        const dash = document.querySelector("#dashboard");
        if (dash) dash.style.transform = "none";
        return;
    }

    if (typeof ScrollTrigger !== "undefined") {
        gsap.registerPlugin(ScrollTrigger);
    }

    gsap.set(".reveal-up", { opacity: 0, y: "100%" });

    const dash = document.querySelector("#dashboard");
    if (dash && typeof ScrollTrigger !== "undefined") {
        gsap.to("#dashboard", {
            scale: 1,
            translateY: 0,
            rotateX: "0deg",
            scrollTrigger: {
                trigger: "#hero-section",
                start: window.innerWidth > RESPONSIVE_WIDTH ? "top 95%" : "top 70%",
                end: "bottom bottom",
                scrub: 1,
            },
        });
    } else if (dash) {
        dash.style.transform = "none";
    }

    const sections = gsap.utils.toArray("section");
    sections.forEach((sec) => {
        const tl = gsap.timeline({
            paused: true,
            scrollTrigger: { trigger: sec, start: "10% 80%", end: "20% 90%" },
        });
        tl.to(sec.querySelectorAll(".reveal-up"), {
            opacity: 1,
            duration: 0.8,
            y: "0%",
            stagger: 0.2,
        });
    });
}
