/** Called by home.html, resets the chips in the modal, accepting an array of new emails, a bollean if they can be removed, and a callback when a new user is added*/
let resetModal = null;
/** Removes a user given it's id*/
let deleteUser = null;

/** Adds access to another user. Passing an optional value if the user can't be removed**/
const addUser = (() => {
    /** Number of user that have access to this form */
    let user_number = 1;

    const username = document.getElementById('addUserInput');
    const errorP = document.getElementById('error');
    const container = document.getElementById('userList');
    const notification = document.getElementById('span_members');

    let usersCanBeRemoved = true;
    let callbackOnAdd = null;

    // On enter pressed on the input, add the user
    username.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            addChip();
        }
    });

    // See resetModal for info
    resetModal = (newUsers, canBeRemoved, newCallbackOnAdd) => {
        usersCanBeRemoved = canBeRemoved;
        callbackOnAdd = null;
        while (user_number > 1) {
            deleteUser(getUserId(user_number));
        }
        for (let user of newUsers) {
            addUser(user);
        }
        callbackOnAdd = newCallbackOnAdd;
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
    let addChip = function (forcedEmail) {
        const email = forcedEmail || username.value;
        if (email !== "" && email.includes('@')) {
            user_number++;
            errorP.innerHTML = "";
            const user = document.createElement('div');
            user.id = getUserId(user_number);

            const chip_user = `<img src="/static/image/account_circle_black_24dp.svg"  width="96" height="96" alt="" >${email}
                         ${usersCanBeRemoved ? `<span class="closebtn" onclick="deleteUser('${user.id}')">&times;</span>` : ''}`;
            user.classList.add('chip');
            user.setAttribute('data-username', email);

            user.innerHTML = chip_user;
            username.value = "";
            container.appendChild(user);
            if (notification) {
                notification.innerText = user_number.toString();
            }

            if (callbackOnAdd) {
                callbackOnAdd(email);
            }
        } else {
            errorP.innerHTML = "Inserisci un'email valida!";
        }
    };
    return addChip;
})();


