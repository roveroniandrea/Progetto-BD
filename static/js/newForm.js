let count_check_input = 0;
let count_question = 0
let count_radio_input = 0;

/**
 * Returns the id of the container of the options. Used to add new options to a single/multi question
 */
function getOptionContainerId(question_number, isRadio) {
    return `${isRadio ? 'radio' : 'check'}_div_${question_number}`;
}

/**
 * Adds a new option (checkbox/radio) to a question
 */
function addRadioCheckOption(question_number, isRadio) {
    if (isRadio)
        count_radio_input++;
    else
        count_check_input++;

    let idSuffix = isRadio ? `radio_${count_radio_input}` : `check_${count_check_input}`;
    let inputId = `input_${idSuffix}`;

    let new_div = document.createElement('div');
    new_div.classList.add('row', 'row-option');
    new_div.id = `row_option_${idSuffix}`;


    new_div.innerHTML = `
            <div class="col-sm-1 col-radio">
                <input class="form-check-input radio-option" type="${isRadio ? 'radio' : 'check'}" disabled>
            </div>
            <div class="col-sm-8">
                <input class="form-control form-input" type="text" placeholder="Opzione" required id="${inputId}">
            </div>
            <div class="col-sm-3 col-add-option">
                <button type="button" class="btn btn-delete rounded-circle btn-tooltip"
                        data-bs-placement="bottom" title="Delete Option" onclick="delete_element('${new_div.id}')">
                        <img src="/static/image/close_black_24dp.svg" alt="">
                </button>
            </div>`;

    let container = document.querySelector(`#${getOptionContainerId(question_number, isRadio)}`);
    container.appendChild(new_div);
    document.querySelector(`#${inputId}`).focus();
}


/**
 * Adds a new question to the form
 */
function newQuestion(type) {
    let rowId = `box_question_${count_question}`;
    let boxForm = document.querySelector('#boxForm');
    let new_div = document.createElement('div');
    let middleHTML = '';
    let requiredQuestionCheckboxId = `required_q_${count_question}`;

    let questionTitleInputId = `input_title_${rowId}`;

    let questionTitleInputHTML = `
        <div class="col-lg">
            <input data-question="" class="form-control form-input form-question" type="text"
                   placeholder="Domanda" required id="${questionTitleInputId}"><br>
        </div>`;

    let assembleNewQuestionHTML = (middle) => `
                                <div class="col-sm-2">
                                </div>
                                <div class="col-lg-8">
                                    <div class="card section-card">
                                        <div class="card-body">
                                            ${middle}
                                            <div class="row">
                                                <div class="col-lg">
                                                    <div class="form-check" data-required="">
                                                      <input class="form-check-input" type="checkbox" value="" id="${requiredQuestionCheckboxId}">
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
                                data-bs-placement="bottom" value="${count_question}" onclick="addRadioCheckOption(this.value, true)" title="Add Option" id="new_radio"><img
                                src="/static/image/add_black_24dp.svg" alt="">
                        </button>
    
                    </div>
                </div>
    
                <div id="${getOptionContainerId(count_question, true)}" class="form-check" data-option="">
                    <div class="row">
                        <div class="col-sm-1 ">
                            <input class="form-check-input radio-option" type="radio" name="flexRadioDefault"
                                   id="flexRadioDefault_${count_radio_input}" disabled>
                        </div>
                        <div class="col-sm-8">
                            <input name="option" id="input_radio_${count_radio_input}" class="form-control form-input"
                                   type="text"
                                   placeholder="Opzione" required>
                        </div>
                        <div class="col-sm-3 col-add-option">
                        </div>
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
                                data-bs-placement="bottom" value="${count_question}" onclick="addRadioCheckOption(this.value, false)" title="Add Option" id="new_check"><img
                                src="/static/image/add_black_24dp.svg" alt="">
                        </button>
                
                    </div>
                </div>
                
                <div id="${getOptionContainerId(count_question, false)}" class="form-check" data-option="">
                    <div class="row">
                        <div class="col-sm-1 ">
                            <input class="form-check-input radio-option" type="check" name="flexRadioDefault"
                                   id="flexCheckDefault_${count_check_input}" disabled>
                        </div>
                        <div class="col-sm-8">
                            <input name="option" id="input_check_${count_check_input}" class="form-control form-input"
                                   type="text"
                                   placeholder="Opzione" required>
                        </div>
                        <div class="col-sm-3 col-add-option">
                        </div>
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
    let row = document.querySelector(`#${id}`);
    row.remove();
}