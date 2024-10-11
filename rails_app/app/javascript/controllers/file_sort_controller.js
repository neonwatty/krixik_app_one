// file_sort_controller.js
import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  static targets = ["fileList"];

  // Sorts the list in ascending order
  sortAscending() {
    this.sortList((a, b) => new Date(a.dataset.createdAt) - new Date(b.dataset.createdAt));
  }

  // Sorts the list in descending order
  sortDescending() {
    this.sortList((a, b) => new Date(b.dataset.createdAt) - new Date(a.dataset.createdAt));
  }

  // Generic sort function to handle sorting logic
  sortList(compareFn) {
    const rows = Array.from(this.fileListTarget.querySelectorAll('tr')); // Get all rows
    rows.sort(compareFn); // Sort rows using the provided comparison function

    // Clear the current list and re-append the sorted rows
    this.fileListTarget.innerHTML = ""; // Clear existing items
    rows.forEach(row => this.fileListTarget.appendChild(row)); // Append sorted rows
  }
}
