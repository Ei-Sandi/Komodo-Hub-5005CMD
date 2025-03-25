const users = [];

//Join chat
function userJoin( username1, username2){
    const user = { username1, username2 };

    users.push(user);

    return user;
};

//Current User
function getCurrentUser(username1) {
    return users.find(user => user.username1 === username1);
};

module.exports = {
    userJoin,
    getCurrentUser
};