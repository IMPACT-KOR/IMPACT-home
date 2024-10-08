// Initialize the MD3 button ripple effect
document.querySelectorAll('.mdc-button').forEach(button => {
    mdc.ripple.MDCRipple.attachTo(button);
});

// Initialize cards for projects
document.querySelectorAll('.mdc-card').forEach(card => {
    mdc.ripple.MDCRipple.attachTo(card);
});


// Navigation handler
document.querySelectorAll('nav ul li a').forEach(link => {
    link.addEventListener('click', (event) => {
        event.preventDefault();
        const section = event.target.getAttribute('data-nav');
        navigateTo(section);
    });
});

function navigateTo(section) {
    // Basic navigation logic for different pages/sections
    if (section === 'home') {
        window.location.href = '/homepage/';
    } else if (section === 'about') {
        window.location.href = '/homepage/about/';
    } else if (section === 'stories') {
        window.location.href = '/homepage/stories/';
    } else if (section === 'projects') {
        window.location.href = '/homepage/projects/';
    } else if (section === 'contact') {
        window.location.href = '/homepage/contact/';
    }
}