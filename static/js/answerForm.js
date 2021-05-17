/**
 * Submits the form. Uses a fake form to send the data and redirecting to the resulting page
 */
function answerForm(formId) {
    const answersBox = [...document.querySelectorAll('[data-answer-id]')];

    let answers = answersBox.map(answerBox => {
        const type = answerBox.getAttribute('data-answer-type');
        const answerValue = answerBox.querySelector('[data-answer-value]');
        let answer = null;
        if (type === 'text' || type === 'date') {
            answer = answerValue.value || null;
        }
        if (type === 'single') {
            const checkbox = [...answerValue.querySelectorAll('input')].filter(i => i.checked)[0];
            answer = checkbox ? checkbox.getAttribute('data-option-text') : null;
        }
        if (type === 'multi') {
            const checkboxes = [...answerValue.querySelectorAll('input')].filter(i => i.checked) || [];
            answer = checkboxes.length > 0 ? checkboxes.map(ch => ch.getAttribute('data-option-text')) : null;
        }

        return {
            id: parseInt(answerBox.getAttribute('data-answer-id')),
            answer,
        }
    });

    answers = answers.filter(a => a.answer !== null);

    //Craeting the fake form
    const fakeForm = document.createElement('form');
    fakeForm.action = `/q/${formId}`;
    fakeForm.method = 'POST';
    const fakeInput = document.createElement('input');
    fakeInput.value = JSON.stringify(answers);
    fakeInput.name = 'answers';
    document.body.appendChild(fakeForm);
    fakeForm.appendChild(fakeInput);
    console.log(answers)
    fakeForm.submit();
    //This form should not submit
    return false;
}