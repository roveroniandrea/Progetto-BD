/** Number of user that have access to this form */
let user_number = 1;

const notification = document.getElementById('span_members');

/** Add user access **/
const addUser = (() => {

    const username = document.getElementById('addUserInput');
    const errorP = document.getElementById('error');
    const container = document.getElementById('userList');

    username.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            addChip();
        }
    });

    let addChip = function(){
        if (username.value !== "" && username.value.includes('@')) {
            user_number++;
            errorP.innerHTML = "";
            const user = document.createElement('div');
            user.id = "userNumber_" + user_number;

            const chip_user = `<img src="/static/image/account_circle_black_24dp.svg"  width="96" height="96" alt="" >${username.value}
                         <span class="closebtn" onclick="deleteUser('${user.id}')">&times;</span>`;
            user.classList.add('chip');
            user.setAttribute('data-username', username.value);

            user.innerHTML = chip_user;
            username.value = "";
            container.appendChild(user);
            notification.innerText = user_number.toString();
        } else {
            errorP.innerHTML = "Inserisci un'email valida!";
        }
    };
    return addChip;
})();

function deleteUser(id) {
    user_number--;
    notification.innerText = user_number.toString();
    delete_element(id);
}
