const sr = ScrollReveal({
    origin: 'top',
    distance: '60px',
    duration: 2500,
    delay: 400,

})

sr.reveal(`.hero__img`, {delay: 800, origin:'bottom'})
sr.reveal(`.hero__title`, {delay: 500})
sr.reveal(`.hero__copy`, {delay: 600})
sr.reveal(`.hero__cta`, {delay: 700})
sr.reveal(`.instructor__img`, {delay: 900, origin:'bottom'})
sr.reveal(`.instructor__name`, {delay: 500})
sr.reveal(`.instructor__tag`, {delay: 600})
sr.reveal(`.instructor__paragraph`, {delay: 600})
sr.reveal(`.title title--border`, {delay: 900, origin:'bottom'})
sr.reveal(`.about__paragraph`, {delay: 700})
sr.reveal(`.cta`, {delay: 600})
sr.reveal(`.about__img`, {origin: 'right'})
sr.reveal(`.title`, {delay: 500})
sr.reveal(`.card__copy`, {delay: 500})
sr.reveal(`.card__item`, {delay: 800})
sr.reveal(`.course__img`, {origin: 'right'})
sr.reveal(`.footer__copy`, {delay: 500})
sr.reveal(`.footer__picture`, {origin: 'right'})
sr.reveal(`.footer__social`, {origin: 'left'})