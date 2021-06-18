/** Sets if the modal shoud ask the server for the users. Accepts the id of the form to request */
let setModalAskUsers = null;
/** Removes a user given its element id*/
let deleteUser = null;

/** Adds access to another user. Passing an optional value if the user can't be removed**/
const addUser = (() => {
    /** Number of user that have access to this form */
    let user_number = 1;

    const username = document.getElementById('addUserInput');
    const errorP = document.getElementById('error');
    const container = document.getElementById('userList');
    const notification = document.getElementById('span_members');

    /** If not null, the modal will retrieve the users from the server and sens every new user created */
    let modalAskForId = null;

    // On enter pressed on the input, add the user
    username.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            addChip();
        }
    });

    // See setModalAskUsers for info
    setModalAskUsers = (formId) => {
        modalAskForId = null;
        // Removing old users
        while (user_number > 1) {
            deleteUser(getUserId(user_number));
        }
        if(formId){
            // Asking server for users
            const xml = new XMLHttpRequest();
            xml.open('get', `/q/${formId}/accesses`);
            xml.onreadystatechange = () => {
                if (xml.readyState === XMLHttpRequest.DONE) {
                    for (let user of JSON.parse(xml.response)) {
                        addChip(user, true);
                    }
                }
                modalAskForId = formId;
            }
            xml.send();
        }
    }

    // See deleteUser for info
    deleteUser = (id) => {
        user_number--;
        if (notification) {
            notification.innerText = user_number.toString();
        }
        const element = document.querySelector(`#${id}`);
        element.remove();
    }

    /** Returns the id of a user chip given it's user_number */
    const getUserId = (user_number) => {
        return "userNumber_" + user_number;
    }


    /** Adds a user. If forcedEmail is passed, the field in username input is ignored */
    let addChip = function (forcedEmail, forceIgnoreServer) {
        const email = forcedEmail || username.value;
        if (email !== "" && email.includes('@')) {
            user_number++;
            errorP.innerHTML = "";
            const user = document.createElement('div');
            user.id = getUserId(user_number);

            const chip_user = `<img src="/static/image/account_circle_black_24dp.svg"  width="96" height="96" alt="" >${email}
                         ${!modalAskForId ? `<span class="closebtn" onclick="deleteUser('${user.id}')">&times;</span>` : ''}`;
            user.classList.add('chip');
            user.setAttribute('data-username', email);

            user.innerHTML = chip_user;
            username.value = "";
            container.appendChild(user);
            if (notification) {
                notification.innerText = user_number.toString();
            }

            if (modalAskForId && !forceIgnoreServer) {
                const xml = new XMLHttpRequest();
                xml.open('post', `/q/${modalAskForId}/accesses/${email}`);
                xml.send();
            }
        } else {
            errorP.innerHTML = "Inserisci un'email valida!";
        }
    };
    return addChip;
})();


