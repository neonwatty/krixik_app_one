function dropdownLogic() {
  const mobileMenuButton = document.querySelector("#hamburger-button");
  const mobileMenu = document.querySelector("#mobile-menu");
  const mobileMenuLinks = mobileMenu.querySelectorAll("a");
  let ignoreFirstOutsideClick = true;
  function toggler() {
    mobileMenu.classList.toggle("hidden");
  }
  function mobileMenuActions(e) {
    if (!ignoreFirstOutsideClick) {
      if (!mobileMenu.contains(e.target)) {
        toggler();
      } else {
        toggler();
      }
    }
    ignoreFirstOutsideClick = false;
  }
  function toggleMobileMenu(e) {
    toggler();
    if (!mobileMenu.classList.contains("hidden")) {
      ignoreFirstOutsideClick = true;
      document.addEventListener("click", mobileMenuActions);
    } else {
      document.removeEventListener("click", mobileMenuActions);
    }
  }
  mobileMenuButton.addEventListener("click", toggleMobileMenu);
}

document.addEventListener("DOMContentLoaded", dropdownLogic);
// dropdownLogic();
