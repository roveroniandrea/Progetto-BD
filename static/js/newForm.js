let count_check_input = 0;
let count_question = 0
let count_radio_input = 0;

//ADD newRadioOption
function newRadioOption(question_number) {
    count_radio_input++;
    let new_div = document.createElement("div");

    let new_radio = `<div class="row row-option" id="row_option_radio_${count_radio_input}">
                            <div class="col-sm-1 col-radio">
                                <input class="form-check-input radio-option" type="radio" name="flexRadioDefault"
                                       id="flexRadioDefault_${count_radio_input}" disabled>
                            </div>
                            <div class="col-sm-8">
                                <input id="input_radio_${count_radio_input}" class="form-control form-input"
                                       type="text"
                                       placeholder="Opzione" required>
                            </div>
                            <div class="col-sm-3 col-add-option">
                                <button type="button" class="btn btn-delete rounded-circle btn-tooltip"
                                        data-bs-placement="bottom" title="Delete Option" id="radio_${count_radio_input}" onclick="delete_option(this.id)">
                                    <img src="/static/image/close_black_24dp.svg">
                                </button>

                            </div>
                        </div>`;

    new_div.innerHTML = new_radio;

    let container = document.getElementById('radio_div_' + question_number);
    container.appendChild(new_div);
    document.getElementById("input_radio_" + count_radio_input).focus();
}


function newCheckOption(question_number) {
    count_check_input++;

    let new_div = document.createElement("div");
    let new_check = `<div class="row row-option" id="row_option_check_${count_check_input}">
                            <div class="col-sm-1 col-radio">
                                <input class="form-check-input radio-option" type="check" name="flexRadioDefault"
                                       id="flexCheckDefault_${count_check_input}" disabled>
                            </div>
                            <div class="col-sm-8">
                                <input name="option" id="input_check_${count_check_input}" class="form-control form-input"
                                       type="text"
                                       placeholder="Opzione" required>
                            </div>
                            <div class="col-sm-3 col-add-option">
                                <button type="button" class="btn btn-delete rounded-circle btn-tooltip"
                                        data-bs-placement="bottom" title="Delete Option" id="check_${count_check_input}" onclick="delete_option(this.id)">
                                    <img src="/static/image/close_black_24dp.svg">
                                </button>

                            </div>
                        </div>`;

    new_div.innerHTML = new_check;
    let container = document.getElementById('check_div_' + question_number);
    container.appendChild(new_div);
    document.getElementById("input_check_" + count_check_input).focus();
}

//NEW QUESTION
function newQuestion(type) {
    let newQuestionRow;
    let boxForm = document.getElementById("boxForm");
    let new_div = document.createElement("div");

    switch (type) {
        case 'text':
            newQuestionRow = `<div class="row row-form" id="box_question_${count_question}" data-question-type="${type}">
                                <div class="col-sm-2">
                                </div>
                                <div class="col-lg-8">
                                    <div class="card section-card">
                                        <div class="card-body">
                                            <div class="row">
                                                <div class="col-lg">
                                                    <input data-question="" class="form-control form-input form-question" type="text"
                                                           placeholder="Domanda" required><br>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-lg">
                                                <textarea class="form-control form-input" type="text" placeholder="Risposta"
                                                          disabled></textarea>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-sm-2">
                                    <button type="button" id="question_${count_question}" onclick="delete_question(this.id)"
                                            class="btn btn-delete-question rounded-circle btn-tooltip"
                                            data-bs-placement="bottom" title="Add Option"><img
                                            src="/static/image/close_black_24dp.svg">
                                    </button>
                                </div>
                            </div>`;
            break;
        case 'single':
            count_radio_input++;
            newQuestionRow = `<div class="row row-form" id="box_question_${count_question}" data-question-type="${type}">
                                <div class="col-sm-2">
                                </div>
                                <div class="col-lg-8">
                                    <div class="card section-card">
                                        <div class="card-body">
                                            <div class="row">
                                                <div class="col-lg-10">
                                                    <input data-question="" class="form-control form-input form-question" type="text"
                                                           placeholder="Domanda"
                                                           required><br>
                                                </div>
                                                <div class="col-md-2 col-add-option">
                                                    <button type="button" class="btn btn-add-option rounded-circle btn-tooltip"
                                                            data-bs-placement="bottom" value="${count_question}" onclick="newRadioOption(this.value)" title="Add Option" id="new_radio"><img
                                                            src="/static/image/add_black_24dp.svg">
                                                    </button>
                            
                                                </div>
                                            </div>
                            
                                            <div id="radio_div_${count_question}" class="form-check" data-option="">
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
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-sm-2">
                                    <button type="button" id="question_${count_question}" onclick="delete_question(this.id)"
                                            class="btn btn-delete-question rounded-circle btn-tooltip"
                                            data-bs-placement="bottom" title="Add Option"><img
                                            src="/static/image/close_black_24dp.svg">
                                    </button>
                                </div>
                            </div>`;
            break;
        case 'multi':
            count_check_input++;
            newQuestionRow = `<div class="row row-form" id="box_question_${count_question}" data-question-type="${type}">
                                <div class="col-sm-2">
                                </div>
                                <div class="col-lg-8">
                                    <div class="card section-card">
                                        <div class="card-body">
                                            <div class="row">
                                                <div class="col-lg-10">
                                                    <input data-question="" class="form-control form-input form-question" type="text"
                                                           placeholder="Domanda"
                                                           required><br>
                                                </div>
                                                <div class="col-md-2 col-add-option">
                                                    <button type="button" class="btn btn-add-option rounded-circle btn-tooltip"
                                                            data-bs-placement="bottom" value="${count_question}" onclick="newCheckOption(this.value)" title="Add Option" id="new_check"><img
                                                            src="/static/image/add_black_24dp.svg">
                                                    </button>
                    
                                                </div>
                                            </div>
                    
                                            <div id="check_div_${count_question}" class="form-check" data-option="">
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
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-sm-2">
                                    <button type="button" id="question_${count_question}" onclick="delete_question(this.id)"
                                            class="btn btn-delete-question rounded-circle btn-tooltip"
                                            data-bs-placement="bottom" title="Add Option"><img
                                            src="/static/image/close_black_24dp.svg">
                                    </button>
                                </div>
                            </div>`;
            break;

        case 'date':
            newQuestionRow = `<div class="row row-form" id="box_question_${count_question}" data-question-type="${type}">
                                <div class="col-sm-2">
                                </div>
                                <div class="col-lg-8">
                                    <div class="card section-card">
                                        <div class="card-body">
                                            <div class="row">
                                                <div class="col-lg">
                                                    <input data-question="" class="form-control form-input form-question" type="text"
                                                           placeholder="Domanda"
                                                           required><br>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-lg">
                                                    <input class="form-control form-input" type="date" placeholder="Domanda" disabled>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-sm-2">
                                    <button type="button" id="question_${count_question}" onclick="delete_question(this.id)"
                                            class="btn btn-delete-question rounded-circle btn-tooltip"
                                            data-bs-placement="bottom" title="Add Option"><img
                                            src="/static/image/close_black_24dp.svg">
                                    </button>
                                </div>
                            </div>`;

            break;
        default:
            alert("Errore tipo di domanda inesistente")
    }
    new_div.innerHTML = newQuestionRow;
    boxForm.appendChild(new_div);

    count_question++;
}


//DELETE OPTION
function delete_option(id) {
    let row = document.getElementById("row_option_" + id);
    row.remove();
}

//DELETE QUESTION
function delete_question(id) {
    let row = document.getElementById("box_" + id);
    row.remove();
}