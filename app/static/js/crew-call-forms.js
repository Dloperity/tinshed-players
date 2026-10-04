(() => {
  const wholeNumber = /^-?\d+$/;

  function showErrors(form, errors) {
    const message = form.querySelector("[data-crew-call-error]");
    if (!message) return;
    message.textContent = errors.join(" ");
    message.hidden = errors.length === 0;
  }

  function validateCrewCallRows(form) {
    const errors = [];
    const rows = [...form.querySelectorAll("[data-crew-call-row]")];
    const requireRole = form.hasAttribute("data-require-role");

    for (const row of rows) {
      const role = row.querySelector('[name="role"]')?.value.trim() ?? "";
      const rawCount = row.querySelector('[name="count"]')?.value.trim() ?? "";
      const isEmpty = !role && (rawCount === "" || rawCount === "0");

      if (isEmpty && !requireRole) continue;
      if (!wholeNumber.test(rawCount)) {
        errors.push("Enter a valid whole number for the crew-call headcount.");
        continue;
      }
      if (!role) {
        errors.push("Enter a role for each crew-call headcount.");
        continue;
      }
      if (role.length > 80) {
        errors.push("Crew-call role names must be 80 characters or fewer.");
        continue;
      }
      if (Number(rawCount) <= 0) {
        errors.push("Headcount for each crew-call role must be greater than 0.");
      }
    }

    showErrors(form, errors);
    return errors.length === 0;
  }

  function updateTimeRange(form) {
    const start = form.querySelector('[name="start_time"]')?.value ?? "";
    const durationValue = form.querySelector('[name="duration_minutes"]')?.value ?? "";
    const preview = form.querySelector("[data-time-range-preview]");
    if (!preview) return;

    const match = /^(\d{2}):(\d{2})$/.exec(start);
    const duration = Number(durationValue);
    if (!match || !Number.isInteger(duration) || duration <= 0) {
      preview.textContent = "Enter a start time and duration to see the time range.";
      return;
    }

    const startMinutes = Number(match[1]) * 60 + Number(match[2]);
    const endTotal = startMinutes + duration;
    const endMinutes = endTotal % 1440;
    const endTime = `${String(Math.floor(endMinutes / 60)).padStart(2, "0")}:${String(endMinutes % 60).padStart(2, "0")}`;
    const daysLater = Math.floor(endTotal / 1440);
    const daySuffix = daysLater ? ` (+${daysLater} day${daysLater === 1 ? "" : "s"})` : "";
    preview.textContent = `${start} - ${endTime}${daySuffix}`;
  }

  document.addEventListener("click", (event) => {
    const addButton = event.target.closest("[data-add-crew-row]");
    if (addButton) {
      const form = addButton.closest("form");
      const list = form?.querySelector("[data-crew-call-list]");
      const template = form?.querySelector("template[data-crew-row-template]");
      if (list && template) {
        list.append(template.content.cloneNode(true));
        list.lastElementChild?.querySelector('[name="role"]')?.focus();
      }
      return;
    }

    const removeButton = event.target.closest("[data-remove-crew-row]");
    if (removeButton) {
      removeButton.closest("[data-crew-call-row]")?.remove();
      return;
    }

    const stepButton = event.target.closest("[data-count-step]");
    if (stepButton) {
      const input = stepButton.closest(".input-group")?.querySelector('[name="count"]');
      if (!input) return;
      const current = wholeNumber.test(input.value.trim()) ? Number(input.value) : 0;
      input.value = String(Math.max(0, current + Number(stepButton.dataset.countStep)));
    }
  });

  document.addEventListener("input", (event) => {
    const form = event.target.closest("form[data-time-range-form]");
    if (form) updateTimeRange(form);
  });

  document.addEventListener("submit", (event) => {
    const form = event.target;
    if (form.matches("form[data-time-range-form]")) {
      updateTimeRange(form);
    }
    if (form.matches("form[data-crew-call-form]") && !validateCrewCallRows(form)) {
      event.preventDefault();
    }
  });

  document.querySelectorAll("form[data-time-range-form]").forEach(updateTimeRange);
})();
