// SHOW NAVBAR FUNCTION
const showMenu = (togglerId, navId, bodyId, headerId) => {
    const toggler = document.getElementById(togglerId),
    navEl = document.getElementById(navId),
    bodyEl = document.getElementById(bodyId),
    headerEl = document.getElementById(headerId)

    if (toggler && navEl && bodyEl && headerEl) {
        toggler.addEventListener('click', () => {
            navEl.classList.toggle('show')
            toggler.classList.toggle('bx-x')
            bodyEl.classList.toggle('desktop--padding')
            headerEl.classList.toggle('desktop--padding')
        })
    }
}

showMenu('toggler-icon', 'sidebar', 'body', 'header')

// LINK ACTIVE
const linkColor = document.querySelectorAll('.nav--link')

function setActive() {
    if (linkColor) {
        linkColor.forEach(l => l.classList.remove('active'))
        this.classList.add('active')
    }
}

linkColor.forEach(l => l.addEventListener('click', setActive))