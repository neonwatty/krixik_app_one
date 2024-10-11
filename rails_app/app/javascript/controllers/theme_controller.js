import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  static targets = ["checkbox"];

  connect() {
    this.loadCheckboxState();
  }

  saveCheckboxState() {
    document.documentElement.classList.toggle("dark");
    document.getElementById("moon").classList.toggle("hidden");
    document.getElementById("sun").classList.toggle("hidden");
    localStorage.setItem("appTheme", this.checkboxTarget.checked);
  }

  loadCheckboxState() {
    const savedState = localStorage.getItem("appTheme");
    this.checkboxTarget.checked = savedState === "true";
    if (this.checkboxTarget.checked) {
      document.documentElement.classList.remove("dark");
      document.getElementById("moon").classList.remove("hidden");
      document.getElementById("sun").classList.add("hidden");
    } else {
      document.documentElement.classList.add("dark");
      document.getElementById("moon").classList.add("hidden");
      document.getElementById("sun").classList.remove("hidden");
    }
  }
}
