(() => {
  const dialog = document.getElementById("delete-confirm-dialog");
  const message = document.getElementById("delete-confirm-message");
  const confirmButton = document.getElementById("delete-confirm-yes");
  const cancelButton = document.getElementById("delete-confirm-no");
  let pendingForm = null;

  if (!dialog || !message || !confirmButton || !cancelButton) return;

  document.addEventListener("submit", (event) => {
    const form = event.target.closest("form[data-confirm-delete]");
    if (!form || form.dataset.confirmed === "yes") return;

    event.preventDefault();
    pendingForm = form;
    message.textContent = form.dataset.confirmMessage || "Are you sure you want to delete this item?";
    dialog.showModal();
    cancelButton.focus();
  });

  confirmButton.addEventListener("click", () => {
    if (!pendingForm) return;
    const confirmation = pendingForm.querySelector('[name="confirmed"]');
    if (confirmation) confirmation.value = "yes";
    pendingForm.dataset.confirmed = "yes";
    const formToSubmit = pendingForm;
    pendingForm = null;
    dialog.close();
    formToSubmit.requestSubmit();
  });

  cancelButton.addEventListener("click", () => {
    pendingForm = null;
    dialog.close();
  });

  dialog.addEventListener("cancel", () => {
    pendingForm = null;
  });
})();
