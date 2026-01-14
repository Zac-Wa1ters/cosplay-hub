document.addEventListener("DOMContentLoaded", function () {

    function setupImagePreview(config) {
        const input = document.getElementById(config.inputId);
        const preview = document.getElementById(config.previewId);
        const clearCheckbox = document.querySelector(`input[name="${config.clearName}"]`);

        if (!preview) return;

        if (input) {
            input.addEventListener("change", function () {
                const file = this.files[0];
                if (!file) return;

                const reader = new FileReader();
                reader.onload = function (e) {
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);

                if (clearCheckbox) {
                    clearCheckbox.checked = false;
                }
            });
        }

        window[config.clearFn] = function () {
            const ok = confirm(
                `Preview removing this image?\n\nIt will not be saved until you click Save.`
            );
            if (!ok) return;

            if (clearCheckbox) {
                clearCheckbox.checked = true;
            }

            if (preview.dataset.defaultSrc) {
                preview.src = preview.dataset.defaultSrc;
            }
        };
    }


    setupImagePreview({
        inputId: "id_avatar",
        previewId: "avatar-preview",
        clearName: "avatar-clear",
        clearFn: "previewClearAvatar"
    });

    setupImagePreview({
        inputId: "id_image",
        previewId: "event-image-preview",
        clearName: "image-clear",
        clearFn: "previewClearEventImage"
    });

});
