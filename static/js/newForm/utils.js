/** If true, the user is asked if he wants to leave the page */
let askLeaveConfirmation = false;

// Checking if the user enters some data
document.querySelector('#newForm').addEventListener('change', () => {
    askLeaveConfirmation = true;
});

// Asking the user id wants to navigate away and losing his changes
window.onbeforeunload = (e) => {
    if (askLeaveConfirmation) {
        e.preventDefault();
        e.returnValue = '';
    } else {
        delete e['returnValue'];
    }
}

/** Removes a generic element */
function delete_element(id) {
    const element = document.querySelector(`#${id}`);
    element.remove();
}

// Enables the dropdown to add a question
new bootstrap.Dropdown(document.querySelector('.dropdown-toggle'));