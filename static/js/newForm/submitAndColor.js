/**
 * Submits the form. Uses a fake form to send the data and redirecting to the resulting page
 */
const submitForm = (() => {
    /** Current color of the form */
    let curr_color = "white";

    const formColorElem = document.querySelector('#formColor');

    const huebFormColorElem = new Huebee(formColorElem, {
        setText: false,
        saturations: 2
    });

    huebFormColorElem.on('change', function (color) {
        curr_color = color;
        document.body.style.backgroundColor = color;
    });

    return () => {
        const mappedData = {
            title: document.querySelector('#formTitle').value,
            questions: [],
            accesses: [...document.querySelectorAll('[data-username]')].map(u => u.getAttribute("data-username")),
            color: curr_color
        }
        const questionsBox = [...document.querySelectorAll('[data-question-type]')];

        mappedData.questions = questionsBox.map(questionBox => {
            const questionType = questionBox.getAttribute('data-question-type');
            const options = questionType === 'single' || questionType === 'multi' ?
                [...questionBox.querySelector('[data-options]').querySelectorAll('[data-options-option]')].map(q => q.value) : null
            return {
                options,
                question: questionBox.querySelector('[data-question]').value,
                required: questionBox.querySelector('[data-required]').checked,
                type: questionType,
            }
        });

        //Don't ask leave confirmation
        askLeaveConfirmation = false;

        //Creting the fake form
        const fakeForm = document.createElement('form');
        fakeForm.style.display = 'none';
        fakeForm.action = '/new';
        fakeForm.method = 'POST';
        const fakeInput = document.createElement('input');
        fakeInput.value = JSON.stringify(mappedData);
        fakeInput.name = 'data';
        document.body.appendChild(fakeForm);
        fakeForm.appendChild(fakeInput);
        fakeForm.submit();
        //This form should not submit
        return false;
    };
})();