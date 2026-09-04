(() => {
  const copyText = async (text) => {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }

    const helper = document.createElement("textarea");
    helper.value = text;
    helper.setAttribute("readonly", "");
    helper.style.position = "fixed";
    helper.style.opacity = "0";
    document.body.appendChild(helper);
    helper.select();
    const copied = document.execCommand("copy");
    helper.remove();

    if (!copied) {
      throw new Error("Copy command was unavailable");
    }
  };

  document.querySelectorAll("[data-copy-target]").forEach((button) => {
    button.addEventListener("click", async () => {
      const target = document.getElementById(button.dataset.copyTarget);
      const label = button.querySelector("span");
      if (!target || !label || button.disabled) return;

      const originalLabel = label.textContent;
      button.disabled = true;

      try {
        await copyText(target.textContent.trim());
        label.textContent = "Copied";
        button.classList.add("is-copied");
      } catch {
        label.textContent = "Select";
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(target);
        selection.removeAllRanges();
        selection.addRange(range);
      }

      window.setTimeout(() => {
        label.textContent = originalLabel;
        button.classList.remove("is-copied");
        button.disabled = false;
      }, 1600);
    });
  });
})();
