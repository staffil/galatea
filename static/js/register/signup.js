function openSocialLogin(provider) {
    let url;
    if (provider === 'google') {
        url = "{% provider_login_url 'google' next=request.path %}";
    } else if (provider === 'github') {
        url = "{% provider_login_url 'github' next=request.path %}";
    }
    
    const popup = window.open(
        url, 
        `${provider}_login`, 
        'width=480,height=600,scrollbars=no,resizable=no,left=' + (screen.width/2 - 240) + ',top=' + (screen.height/2 - 300)
    );
    
    const interval = setInterval(() => {
        if (popup.closed) {
            clearInterval(interval);
            window.location.reload();
        }
    }, 1000);
}
