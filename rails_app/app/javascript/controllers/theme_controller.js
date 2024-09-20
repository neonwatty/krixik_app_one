import { Controller } from "@hotwired/stimulus";

// Connects to data-controller="theme"
export default class extends Controller {
  static targets = ["checkbox"];

  connect() {
    this.loadCheckboxState();
  }

  saveCheckboxState() {
    localStorage.setItem('synthwaveTheme', this.checkboxTarget.checked);
  }

  loadCheckboxState() {
    const savedState = localStorage.getItem('synthwaveTheme');
    this.checkboxTarget.checked = savedState === 'true';
  }
}