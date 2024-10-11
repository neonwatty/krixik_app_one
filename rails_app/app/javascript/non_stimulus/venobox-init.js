import VenoBox from "venobox";

document.addEventListener("DOMContentLoaded", () => {
  new VenoBox({
    overlayClose: true,
    spinner: "cube-grid",
    closeBackground: "transparent",
    overlayColor: "rgba(82, 52, 235,0.8)",
    share: true,
    titleattr: "data-title",
  });
});
