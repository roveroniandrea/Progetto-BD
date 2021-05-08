let count_check_input = 0;
let count_question = 0
let count_radio_input = 0;

/** If true, the user is asked if he wants to leave the page*/
let askLeaveConfirmation = false;

// Checking if the user enters some data
document.querySelector('#newForm').addEventListener('change', () => {
    askLeaveConfirmation = true;
});

// Asking the user id wants to navigate away and losing his changes
window.onbeforeunload = (e) => {
    if (askLeaveConfirmation) {
        console.log('prevented');
        e.preventDefault();
        e.returnValue = '';
    }
    else{
        delete e['returnValue'];
    }
}

/**
 * Returns the id of the container of the options. Used to add new options to a single/multi question
 */
function getOptionContainerId(question_number, isRadio) {
    return `${isRadio ? 'radio' : 'check'}_div_${question_number}`;
}

/**
 * Returns the HTML to create an option row. It can be a radio or chackbox, have an optional id and an optional remove button
 */
function getOptionHTML(isRadio, inputId, removeId) {
    return `
            <div class="col-sm-1 col-radio">
                <input class="form-check-input radio-option" type="${isRadio ? 'radio' : 'check'}" disabled>
            </div>
            <div class="col-sm-8">
                <input class="form-control form-input" type="text" placeholder="Opzione" required id="${inputId || undefined}" data-options-option="">
            </div>
            <div class="col-sm-3 col-add-option">
                ${removeId ? `<button type="button" class="btn btn-delete rounded-circle btn-tooltip"
                        data-bs-placement="bottom" title="Delete Option" onclick="delete_element('${removeId}')">
                        <img src="/static/image/close_black_24dp.svg" alt="">
                </button>` : ''}
            </div>`
}


/**
 * Adds a new option (checkbox/radio) to a question
 */
function addRadioCheckOption(question_number, isRadio) {
    if (isRadio)
        count_radio_input++;
    else
        count_check_input++;

    const idSuffix = isRadio ? `radio_${count_radio_input}` : `check_${count_check_input}`;
    const inputId = `input_${idSuffix}`;

    const new_div = document.createElement('div');
    new_div.classList.add('row', 'row-option');
    new_div.id = `row_option_${idSuffix}`;


    new_div.innerHTML = getOptionHTML(isRadio, inputId, new_div.id);

    const container = document.querySelector(`#${getOptionContainerId(question_number, isRadio)}`);
    container.appendChild(new_div);
    document.querySelector(`#${inputId}`).focus();
}


/**
 * Adds a new question to the form
 */
function newQuestion(type) {
    const rowId = `box_question_${count_question}`;
    const boxForm = document.querySelector('#boxForm');
    const new_div = document.createElement('div');
    let middleHTML = '';
    const requiredQuestionCheckboxId = `required_q_${count_question}`;

    const questionTitleInputId = `input_title_${rowId}`;

    const questionTitleInputHTML = `
        <div class="col-lg">
            <input data-question="" class="form-control form-input form-question" type="text"
                   placeholder="Domanda" required id="${questionTitleInputId}"><br>
        </div>`;

    const assembleNewQuestionHTML = (middle) => `
                                <div class="col-sm-2">
                                </div>
                                <div class="col-lg-8">
                                    <div class="card section-card">
                                        <div class="card-body">
                                            ${middle}
                                            <div class="row">
                                                <div class="col-lg">
                                                    <div class="form-check">
                                                      <input class="form-check-input" type="checkbox" value="" id="${requiredQuestionCheckboxId}" data-required="">
                                                      <label class="form-check-label" for="${requiredQuestionCheckboxId}">
                                                        Domanda obbligatoria
                                                      </label>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-sm-2">
                                    <button type="button" onclick="delete_element('${rowId}')"
                                            class="btn btn-delete-question rounded-circle btn-tooltip"
                                            data-bs-placement="bottom" title="Add Option"><img
                                            src="/static/image/close_black_24dp.svg" alt="">
                                    </button>
                                </div>`;

    new_div.classList.add('row', 'row-form');
    new_div.id = rowId;
    new_div.setAttribute('data-question-type', type);


    switch (type) {
        case 'text':
            middleHTML = `
                <div class="row">
                   ${questionTitleInputHTML}
                </div>
                <div class="row">
                    <div class="col-lg">
                    <textarea class="form-control form-input" type="text" placeholder="Risposta"
                              disabled></textarea>
                    </div>
                </div>`;
            break;
        case 'single':
            count_radio_input++;
            middleHTML = `
                <div class="row">
                    ${questionTitleInputHTML}
                    <div class="col-md-2 col-add-option">
                        <button type="button" class="btn btn-add-option rounded-circle btn-tooltip"
                                data-bs-placement="bottom" value="${count_question}" onclick="addRadioCheckOption(this.value, true)" title="Add Option"><img
                                src="/static/image/add_black_24dp.svg" alt="">
                        </button>
    
                    </div>
                </div>
    
                <div id="${getOptionContainerId(count_question, true)}" class="form-check" data-options="">
                    <div class="row">
                        ${getOptionHTML(true)}
                    </div>
                </div>`;
            break;
        case 'multi':
            count_check_input++;
            middleHTML = `
                <div class="row">
                    ${questionTitleInputHTML}
                    <div class="col-md-2 col-add-option">
                        <button type="button" class="btn btn-add-option rounded-circle btn-tooltip"
                                data-bs-placement="bottom" value="${count_question}" onclick="addRadioCheckOption(this.value, false)" title="Add Option"><img
                                src="/static/image/add_black_24dp.svg" alt="">
                        </button>
                
                    </div>
                </div>
                
                <div id="${getOptionContainerId(count_question, false)}" class="form-check" data-options="">
                    <div class="row">
                        ${getOptionHTML(false)}
                    </div>
                </div>`;
            break;

        case 'date':
            middleHTML = `
                <div class="row">
                    ${questionTitleInputHTML}
                </div>
                <div class="row">
                    <div class="col-lg">
                        <input class="form-control form-input" type="date" placeholder="Domanda" disabled>
                    </div>
                </div>`;
            break;
        default:
            alert("Errore tipo di domanda inesistente")
    }

    new_div.innerHTML = assembleNewQuestionHTML(middleHTML);
    boxForm.appendChild(new_div);

    document.querySelector(`#${questionTitleInputId}`).focus();

    count_question++;
}


/**
 * Removes a generic element
 */
function delete_element(id) {
    const row = document.querySelector(`#${id}`);
    row.remove();
}

/**
 * Submits the form. Uses a fake form to send the data and redirecting to the resulting page
 */
function submitForm() {
    const mappedData = {
        title: document.querySelector('#formTitle').value,
        questions: [],
        accesses: [], //TODO (se stesso viene già incluso lato server)
        color: 'lightcoral' //TODO
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
}