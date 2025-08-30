function handleClick(action) {
    switch(action) {
        case 'main':
            window.location.href = '/main';
            break;
        case 'signup':
            window.location.href = URL_SIGNUP;
            break;
        case 'login':
            window.location.href = URL_LOGIN;
            break;
    }
}
