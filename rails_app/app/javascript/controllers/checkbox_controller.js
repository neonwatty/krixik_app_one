import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  static targets = ["checkbox", "output"];

  connect() {
    this.loadCheckboxStates();
    this.showBoxesChecked();
  }

  get checkedCheckboxes() {
    return this.checkboxTargets
      .filter(checkbox => checkbox.checked)
      .map(checkbox => checkbox.value);
  }

  checkStatus(event) {
    const checkbox = event.target;
    const index = checkbox.id.split('-')[1]; // Extract the index from the checkbox ID
    this.saveCheckboxState(index, checkbox.checked);
    this.showBoxesChecked();
    this.showDeleteButton(); // Show or hide the delete button
  }

  saveCheckboxState(index, isChecked) {
    localStorage.setItem(`checkbox-${index}`, isChecked);
  }

  loadCheckboxStates() {
    this.checkboxTargets.forEach((checkbox, index) => {
      const savedState = localStorage.getItem(`checkbox-${index}`);
      checkbox.checked = savedState === 'true';
      const deleteButton = document.getElementById(`delete-checkbox-${index}`); // Reference the delete button by ID
      if (deleteButton) {
        deleteButton.classList.toggle('hidden', !checkbox.checked); // Show or hide based on checkbox state
      }
    });
  }

  showBoxesChecked() {
    this.outputTarget.textContent = this.checkedCheckboxes.length > 0
      ? this.checkedCheckboxes.join(', ')
      : 'No checkboxes selected.';
  }

  showDeleteButton() {
    this.checkboxTargets.forEach((checkbox, index) => {
      const deleteButton = document.getElementById(`delete-checkbox-${index}`);
      if (deleteButton) {
        deleteButton.classList.toggle('hidden', !checkbox.checked);
      }
    });
  }

  removeCheckboxFromLocalStorage(index) {
    console.log(`Removing checkbox-${index} from localStorage`);
    this.saveCheckboxState(index, false); // Save the state as false
    localStorage.removeItem(`checkbox-${index}`);
  }

  confirmDelete(index) {
    if (confirm("Are you sure you want to delete this upload?")) {
      // load in all checkbox indices
      
    }
  }
}
