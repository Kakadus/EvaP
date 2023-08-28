import { selectOrError } from "./utils.js";
import { CSRF_HEADERS } from "./csrf-utils.js";

export function attachFormSubmitDownloadAndRedirect(form_id: string, filename: string, redirectUrl: string): void {
    const form: HTMLFormElement = selectOrError("#" + form_id);
    const formData = new FormData(form);
    form.onsubmit = _ => {
        fetch(form.action, {
            body: formData,
            headers: CSRF_HEADERS,
            method: form.method,
        })
            .then(resp => resp.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.style.display = "none";
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                window.location.href = redirectUrl; //redirect
            })
            .catch(reason => alert(reason));
        return false; // stop event propagation
    };
}
