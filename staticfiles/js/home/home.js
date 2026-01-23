   function handleClick(action) {
        console.log(`${action} button clicked`);
        switch(action) {
            case 'main':
                window.location.href = '/main'; 
                break;
            case 'signup':
                window.location.href ="{% url 'register:signup' %}"; 
                break;
            case 'login':
                window.location.href ="{% url 'register:login' %}"; 
                break;
        }
    }